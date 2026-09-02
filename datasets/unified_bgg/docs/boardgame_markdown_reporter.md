# Boardgame Markdown Reporter 本地记忆

更新时间：2026-08-26

## 作用

这个本地 skill 用于：

- 查询 `unified_bgg` 中的桌游资料
- 生成中文 Markdown 报告
- 在报告中加入 `核心机制` 解释：提炼 1~3 个最关键、最好玩的机制，并结合规则书文本和评论进行更详细的评价与解析
- 批量生成前 100 个高分桌游的 Markdown 报告
- 汇总游戏简介、规则摘要、机制解释和评论摘选
- 将结果保存到 `D:\OpenViking\research\datasets\unified_bgg\docs\`

## skill 位置

`C:\Users\admin\.codex\skills\boardgame-markdown-reporter`

## 主要输入

- 游戏名或 BGG ID
- 可选中文名
- 可选输出路径

## 主要输出

- 中文 Markdown 报告
- 本地规则/评论/概览召回素材
- `docs\top100_reports\` 下的批量报告集合

## 关联脚本

- `scripts/build_boardgame_report.py`
- `scripts/build_boardgame_reports_batch.py`
- `scripts/report_builder.py`

## 适用场景

- 用户要求“查询某个桌游并写成 Markdown”
- 用户要求“介绍这款桌游的规则、机制、简介、评论”
- 用户要求“把召回结果写到本地文件里”
