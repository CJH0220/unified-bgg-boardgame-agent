<#
  抓取各 Kaggle 数据集的公开元信息（标题/许可/更新时间/官方 description/文件清单），
  存到 _profiles/kaggle_meta.json，供写 DATASET.md 时引用原始许可与作者说明。
  view / list 端点匿名可用，无需 token。
#>
param([string]$Base = (Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)))
$ErrorActionPreference = 'Stop'
$ProgressPreference    = 'SilentlyContinue'

$REFS = @(
  'threnjen/board-games-database-from-boardgamegeek',
  'jvanelteren/boardgamegeek-reviews',
  'mattadamhouser/ranked-board-game-data-from-boardgamegeek',
  'mrpantherson/board-game-data',
  'andrewmvd/board-games',
  'sujaykapadnis/board-games',
  'gabrio/board-games-dataset'
)

$out = @{}
foreach ($ref in $REFS) {
  $rec = @{ ref = $ref }
  try {
    $v = Invoke-RestMethod -Uri "https://www.kaggle.com/api/v1/datasets/view/$ref" -TimeoutSec 40
    $rec.title           = $v.title
    $rec.subtitle        = $v.subtitle
    $rec.licenseName     = $v.licenseName
    $rec.totalBytes      = $v.totalBytes
    $rec.lastUpdated     = $v.lastUpdated
    $rec.downloadCount   = $v.downloadCount
    $rec.voteCount       = $v.voteCount
    $rec.usabilityRating = $v.usabilityRating
    $rec.url             = "https://www.kaggle.com/datasets/$ref"
    $rec.description     = $v.description
  } catch { $rec.view_error = $_.Exception.Message }
  try {
    $l = Invoke-RestMethod -Uri "https://www.kaggle.com/api/v1/datasets/list/$ref" -TimeoutSec 40
    $rec.files = @($l.datasetFiles | ForEach-Object { @{ name = $_.name; totalBytes = $_.totalBytes } })
  } catch { $rec.list_error = $_.Exception.Message }
  $out[$ref] = $rec
  Write-Host "fetched $ref"
}

$dst = Join-Path $Base "_profiles\kaggle_meta.json"
$json = $out | ConvertTo-Json -Depth 6
[System.IO.File]::WriteAllText($dst, $json, (New-Object System.Text.UTF8Encoding($false)))
Write-Host "wrote $dst"
