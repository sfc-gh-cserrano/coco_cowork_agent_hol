# Assets

This folder contains images and source files referenced in the quickstart guide.

## Screenshots Needed

| Filename | Description |
|----------|-------------|
| `architecture.png` | Architecture diagram showing the HOL_COCO_COWORK database with DATA, TOOLS, and AGENTS schemas |
| `semantic_view_created.png` | Screenshot showing the semantic view successfully created in CoCo |
| `agent_created.png` | Screenshot showing the agent successfully deployed in CoCo |
| `evaluation_results.png` | Screenshot showing evaluation scores (~93% correctness, 100% consistency) |
| `cowork_chat.png` | Screenshot showing the agent responding to a question in Snowflake CoWork |

## Source Files

| Folder | Contents |
|--------|----------|
| `Setup/01_setup.sql` | SQL: warehouse, database, schemas, stages, tables |
| `Setup/02_copy_files.py` | Python: upload CSVs and skills to stages |
| `Setup/03_load_data.sql` | SQL: load data into tables |
| `Setup/data/` | CSV files (dim_store, dim_item, fact_item_sales) |
| `Skills/anomaly_detection/SKILL.md` | Anomaly detection skill definition |
| `Skills/sales_report/SKILL.md` | Sales report generator skill definition |
| `Prompts/semantic_view.md` | Prompt for CoCo `/semantic-view` command |
| `Prompts/agent.md` | Prompt for CoCo `/cortex-agent` command |
| `Prompts/evaluations.md` | Prompt for agent evaluation |

## Image Guidelines (from sfquickstarts)

- File size must be less than 1MB
- Use lowercase names with underscores
- Optimize for web (recommended: tinypng.com)
- No additional subfolders within assets/ (source file subfolders are an exception for this guide)
