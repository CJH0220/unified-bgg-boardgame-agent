<#
.SYNOPSIS
  下载「桌游机制 Agent」调研中所有【带评分属性】的公开数据集到本地 raw/ 目录。

.DESCRIPTION
  Kaggle 的 /api/v1/datasets/download 端点会 302 到 storage.googleapis.com 的签名 URL，
  **匿名即可下载**（2026-08-17 实测），无需 kaggle.json / kaggle CLI。
  单文件下载返回的是 zip，需解压；整包下载返回 archive.zip。

  幂等：目标 csv 已存在则跳过。想强制重下用 -Force。
  默认跳过 jvanelteren 的历史评论快照（15m/19m，共 ~2.9GB，已被 26m 取代），
  需要做时序对比时加 -IncludeHistoricalReviews。

.EXAMPLE
  powershell -ExecutionPolicy Bypass -File download.ps1
  powershell -ExecutionPolicy Bypass -File download.ps1 -IncludeHistoricalReviews
#>
param(
  [string]$Base = (Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)),
  [switch]$Force,
  [switch]$IncludeHistoricalReviews,
  # 只下指定的数据集目录（可多个），用于跟大文件并行跑，例如：-Only bgg-mrpantherson,bgg-andrewmvd
  [string[]]$Only
)

$ErrorActionPreference = 'Stop'
$ProgressPreference    = 'SilentlyContinue'

# powershell.exe -File 传参时 "-Only a,b,c" 会整体作为一个字符串进来（不会被拆成数组），
# 这里统一按逗号/空格拆开，两种调用方式都能用。
if ($Only) { $Only = @($Only | ForEach-Object { $_ -split '[,\s]+' } | Where-Object { $_ }) }

# ---- 清单：dir = Base 下的子目录名；ref = Kaggle 数据集 ref；files = 空则整包下载 ----
$MANIFEST = @(
  @{ dir='bgg-threnjen';            ref='threnjen/board-games-database-from-boardgamegeek';
     files=@('games.csv','user_ratings.csv','ratings_distribution.csv','mechanics.csv','themes.csv',
             'subcategories.csv','artists_reduced.csv','designers_reduced.csv','publishers_reduced.csv',
             'bgg_data_documentation.txt') }

  @{ dir='bgg-reviews-jvanelteren'; ref='jvanelteren/boardgamegeek-reviews';
     files=@('bgg-26m-reviews.csv','games_detailed_info2025.csv','games_detailed_info.csv',
             '2020-08-19.csv','2022-01-08.csv') }

  @{ dir='bgg-ranked-mattadamhouser'; ref='mattadamhouser/ranked-board-game-data-from-boardgamegeek'; files=@() }
  @{ dir='bgg-mrpantherson';          ref='mrpantherson/board-game-data';                            files=@() }
  @{ dir='bgg-andrewmvd';             ref='andrewmvd/board-games';                                   files=@() }
  @{ dir='bgg-sujaykapadnis';         ref='sujaykapadnis/board-games';                               files=@() }
  @{ dir='bgg-gabrio';                ref='gabrio/board-games-dataset';                              files=@() }
)

$HISTORICAL = @('bgg-15m-reviews.csv','bgg-19m-reviews.csv')

function Expand-Into($zip, $outDir) {
  # Expand-Archive 在中文路径 + 大文件上偶发失败，直接用 .NET
  Add-Type -AssemblyName System.IO.Compression.FileSystem -ErrorAction SilentlyContinue
  $za = [System.IO.Compression.ZipFile]::OpenRead($zip)
  try {
    foreach ($e in $za.Entries) {
      if ([string]::IsNullOrEmpty($e.Name)) { continue }
      $target = Join-Path $outDir $e.Name
      [System.IO.Compression.ZipFileExtensions]::ExtractToFile($e, $target, $true)
    }
  } finally { $za.Dispose() }
}

function Get-KaggleFile($ref, $file, $outDir) {
  $target = Join-Path $outDir $file
  if ((Test-Path $target) -and -not $Force) { Write-Host "  skip  $file (exists)"; return }
  $tmp = Join-Path $outDir "$file.zip.part"
  $url = "https://www.kaggle.com/api/v1/datasets/download/$ref/$file"
  Write-Host "  GET   $file"
  $code = & curl.exe -s -L --retry 3 --retry-delay 3 -o $tmp -w "%{http_code}" $url
  if ($code -ne '200') { Remove-Item $tmp -Force -ErrorAction SilentlyContinue; throw "HTTP $code for $ref/$file" }
  # 单文件端点恒返回 zip；万一直接给了原文件（magic 非 PK）就改名
  $fs = [IO.File]::OpenRead($tmp); $m = New-Object byte[] 2; $fs.Read($m,0,2) | Out-Null; $fs.Close()
  if ($m[0] -eq 0x50 -and $m[1] -eq 0x4B) { Expand-Into $tmp $outDir; Remove-Item $tmp -Force }
  else { Move-Item $tmp $target -Force }
  Write-Host ("  ok    {0}  {1:N1} MB" -f $file, ((Get-Item $target).Length/1MB))
}

function Get-KaggleBundle($ref, $outDir) {
  $marker = Join-Path $outDir '.bundle-ok'
  if ((Test-Path $marker) -and -not $Force) { Write-Host "  skip  bundle (exists)"; return }
  $tmp = Join-Path $outDir 'archive.zip.part'
  Write-Host "  GET   <bundle>"
  $code = & curl.exe -s -L --retry 3 --retry-delay 3 -o $tmp -w "%{http_code}" "https://www.kaggle.com/api/v1/datasets/download/$ref"
  if ($code -ne '200') { Remove-Item $tmp -Force -ErrorAction SilentlyContinue; throw "HTTP $code for $ref bundle" }
  Expand-Into $tmp $outDir
  Remove-Item $tmp -Force
  Set-Content -Path $marker -Value (Get-Date -Format o) -Encoding utf8
  Write-Host "  ok    bundle extracted"
}

foreach ($d in $MANIFEST) {
  if ($Only -and ($Only -notcontains $d.dir)) { continue }
  $outDir = Join-Path $Base "$($d.dir)\raw"
  New-Item -ItemType Directory -Force -Path $outDir | Out-Null
  Write-Host "== $($d.ref)"
  $files = @($d.files)
  if ($d.dir -eq 'bgg-reviews-jvanelteren' -and $IncludeHistoricalReviews) { $files += $HISTORICAL }
  if ($files.Count -eq 0) { Get-KaggleBundle $d.ref $outDir }
  else { foreach ($f in $files) { Get-KaggleFile $d.ref $f $outDir } }
}

Write-Host "`nDONE. 落盘统计："
Get-ChildItem $Base -Directory | ForEach-Object {
  $raw = Join-Path $_.FullName 'raw'
  if (Test-Path $raw) {
    $s = (Get-ChildItem $raw -File | Measure-Object Length -Sum)
    "{0,-28} {1,3} files {2,9:N1} MB" -f $_.Name, $s.Count, ($s.Sum/1MB)
  }
}
