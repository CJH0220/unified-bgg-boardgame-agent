# unified_bgg Unified Schema Draft

## Goals

The unified dataset supports two downstream products:

- Fine-tuning samples: structured QA, mechanism explanations, recommendation rationales, review summaries, and information extraction.
- Retrieval corpus: stable game entities, taxonomy labels, review text, and metadata-rich RAG chunks.

All derived facts should be traceable through `source_dataset`, `source_file`, `snapshot_date`, and transform version.

## Key convention

| Field | Type | Meaning |
|---|---:|---|
| `game_id` | string | Stable internal key, formatted as `bgg:{bgg_id}` |
| `bgg_id` | int64 | Official BGG game ID, the primary cross-dataset join key |
| `source_game_id` | string | Raw source ID, such as `BGGId`, `ID`, `game_id`, or `game.id` |
| `source_dataset` | string | Source dataset directory name |
| `snapshot_date` | string/date | Dataset or file snapshot date |

## Target tables

### `games`

One row per game entity.

| Field | Type | Notes | Suggested priority |
|---|---:|---|---|
| `game_id` | string | `bgg:{bgg_id}` | derived |
| `bgg_id` | int64 | Official BGG ID | all |
| `primary_name` | string | Main title | jvanelteren_2025 > threnjen > gabrio |
| `alternate_names` | list[string] | Alternate names | jvanelteren_2025 > gabrio |
| `game_type` | string | `boardgame` or `boardgameexpansion` | jvanelteren_2025 > gabrio |
| `year_published` | int16/null | 0 means unknown; negative years are valid for ancient games | jvanelteren_2025 > threnjen |
| `min_players` | int16/null | 0 becomes null | jvanelteren_2025 > threnjen |
| `max_players` | int16/null | 99/999 should become null or unbounded marker | jvanelteren_2025 > threnjen |
| `min_playtime` | int32/null | Minutes | jvanelteren_2025 > threnjen |
| `max_playtime` | int32/null | Minutes | jvanelteren_2025 > threnjen |
| `min_age` | int16/null | 0 becomes null | jvanelteren_2025 > threnjen |
| `description` | string/null | Natural-language description | jvanelteren_2025 > gabrio; avoid threnjen stemmed text |
| `image_url` | string/null | Image URL | jvanelteren_2025 |
| `thumbnail_url` | string/null | Thumbnail URL | jvanelteren_2025 |

### `game_stats`

Snapshot table for ratings, ranks, popularity, and complexity. A game can have many rows.

| Field | Type | Notes |
|---|---:|---|
| `game_id` | string | FK to `games` |
| `snapshot_date` | string/date | Snapshot date |
| `average_rating` | float32/null | Arithmetic average |
| `bayes_average` | float32/null | Geek Rating / Bayesian average; source zeroes become null |
| `users_rated` | int64/null | Rating count; do not mix incompatible snapshots |
| `rank_overall` | int32/null | Overall rank; sentinel values become null |
| `rank_domain` | string/null | Sub-rank domain, e.g. `strategygames` |
| `rank_domain_position` | int32/null | Sub-rank position; sentinel values become null |
| `weight_average` | float32/null | Complexity average; null if too few votes |
| `weight_votes` | int32/null | Complexity vote count |
| `stddev_rating` | float32/null | Rating standard deviation |
| `source_dataset` | string | Source dataset |
| `source_file` | string | Source file |

### `game_taxonomy`

Long-form table for mechanics, categories, themes, subdomains, families, and domains.

| Field | Type | Notes |
|---|---:|---|
| `game_id` | string | FK to `games` |
| `taxonomy_type` | string | `mechanic`, `category`, `theme`, `subdomain`, `family`, or `domain` |
| `taxonomy_name_raw` | string | Raw label from source |
| `taxonomy_name_canonical` | string/null | Canonical label, preferably mapped to the 2025 vocabulary |
| `taxonomy_snapshot` | string | Vocabulary snapshot, e.g. `2017-06`, `2021-12`, `2025-02` |
| `mapping_confidence` | string | `exact`, `alias`, `manual_review`, or `unmapped` |
| `source_dataset` | string | Source dataset |
| `source_file` | string | Source file |

### `ratings`

User-level ratings. This is a large table and should be stored as partitioned Parquet later.

| Field | Type | Notes |
|---|---:|---|
| `rating_id` | string | Derived from source and row/hash |
| `game_id` | string | FK to `games` |
| `user_id` | string | Always string; numeric-looking usernames exist |
| `rating` | float32 | Prefer valid 1-10 ratings; anomalies go to QA report |
| `has_comment` | bool | Whether this rating has review text |
| `source_dataset` | string | `bgg-reviews-jvanelteren` or `bgg-threnjen` |
| `source_file` | string | Source file |
| `source_row_id` | int64/null | Raw row/index if available |

### `reviews`

Review text table. Do not assume every rating has text.

| Field | Type | Notes |
|---|---:|---|
| `review_id` | string | Stable review ID |
| `game_id` | string | FK to `games` |
| `user_id` | string | Always string |
| `rating` | float32/null | Rating attached to review |
| `comment_text` | string | Raw comment text |
| `language` | string/null | Optional detected language |
| `text_length` | int32 | Character count |
| `source_dataset` | string | Source dataset |
| `source_file` | string | Source file |

### `id_map`

Entity alignment table.

| Field | Type | Notes |
|---|---:|---|
| `game_id` | string | Internal key |
| `bgg_id` | int64/null | Official BGG ID |
| `source_dataset` | string | Source dataset |
| `source_file` | string | Source file |
| `source_game_id` | string/null | Raw source ID |
| `source_name` | string/null | Raw source title |
| `match_method` | string | `bgg_id_exact`, `name_year_fuzzy`, or `manual` |
| `match_confidence` | float32 | 0-1 |
| `needs_review` | bool | Manual review flag |

### `dataset_lineage`

Source and transform tracking.

| Field | Type | Notes |
|---|---:|---|
| `source_dataset` | string | Source dataset |
| `source_file` | string | Raw source file |
| `license` | string | License |
| `snapshot_date` | string | Snapshot date |
| `row_count_raw` | int64/null | Raw row count |
| `row_count_cleaned` | int64/null | Cleaned row count |
| `processing_version` | string | Transform version |
| `known_issues` | list[string] | Known caveats |

## RAG output draft

```json
{
  "doc_id": "game:bgg:174430:overview",
  "game_id": "bgg:174430",
  "title": "Gloomhaven",
  "doc_type": "game_overview",
  "mechanics": ["Campaign / Battle Card Driven", "Cooperative Game"],
  "categories": ["Adventure", "Fantasy"],
  "source_datasets": ["bgg-reviews-jvanelteren"],
  "text": "..."
}
```

## Fine-tuning output draft

```json
{"messages":[{"role":"user","content":"..."},{"role":"assistant","content":"..."}],"metadata":{"game_id":"bgg:...","task_type":"game_qa","source":"unified_bgg"}}
```
