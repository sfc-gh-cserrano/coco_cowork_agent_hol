# Hands-On Lab: Building AI Agents with Cortex Code and CoWork


Build an end-to-end AI-powered analytics agent using Snowflake Cortex Code (CoCo) — from raw data to a production-ready Cortex Agent with evaluations.

## What You Will Build

1. **Star Schema Data Model** — Fact and dimension tables for convenience store hot food sales
2. **Semantic View** — An AI-ready data layer with verified queries for Cortex Analyst
3. **Cortex Agent** — A conversational analytics agent for C-Level executives
4. **Evaluation Framework** — Ground truth dataset and automated agent evaluation

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  HOL_COCO_CWORK Database                 │
├───────────────┬──────────────────┬──────────────────────┤
│  DATA Schema  │  TOOLS Schema    │  AGENTS Schema       │
│               │                  │                      │
│  DIM_STORE    │  Semantic View:  │  Cortex Agent:       │
│  DIM_ITEM     │  HOT_FOOD_SALES  │  HOT_FOOD_SALES     │
│  FACT_ITEM    │  _ANALYTICS      │  _AGENT             │
│  _SALES       │                  │                      │
│               │  (8 VQRs,        │  (text-to-SQL tool,  │
│  100 stores   │   2 relationships│   orchestration +    │
│  100 items    │   3 tables)      │   response instrs)   │
│  539K sales   │                  │                      │
└───────────────┴──────────────────┴──────────────────────┘
```

## Prerequisites

- Snowflake account with SYSADMIN and ACCOUNTADMIN access
- Cortex Code (CoCo) desktop application installed
- A Snowflake Workspace (notebook) for running the setup script

## Lab Steps

### Step 1: Setup (Run in Snowflake Workspace)

This is the only step that requires manual SQL execution. Everything else is done through Cortex Code prompts.

1. Open a **Snowflake Workspace** (notebook)
2. Create a **SQL cell** and paste the contents of `Setup/setup.sql`
3. Run the SQL cell to create the warehouse, database, schemas, and tables
4. Create a **Python cell** and run the following to upload the CSV files:

```python
from snowflake.snowpark.context import get_active_session
session = get_active_session()
session.file.put("data/dim_store.csv", "@HOL_STAGE/dim_store", auto_compress=True, overwrite=True)
session.file.put("data/dim_item.csv", "@HOL_STAGE/dim_item", auto_compress=True, overwrite=True)
session.file.put("data/fact_item_sales.csv", "@HOL_STAGE/fact_item_sales", auto_compress=True, overwrite=True)
```

5. Run the remaining SQL statements (steps 7-9 in setup.sql) to load data into tables
6. Verify the load shows: DIM_STORE = 100, DIM_ITEM = 100, FACT_ITEM_SALES = 539,215

### Step 2: Create Semantic View (Cortex Code)

Open the file `Prompts/semantic_view.md` in Cortex Code and run the `/semantic-view` skill with the file attached:

```
/semantic-view @semantic_view.md
```

**What CoCo will do:**
- Discover all tables in HOL_COCO_CWORK.DATA
- Generate a semantic model with dimensions, facts, and relationships
- Create 8 verified queries (VQRs) for common sales analytics questions
- Validate the YAML against Snowflake
- Deploy the semantic view to HOL_COCO_CWORK.TOOLS

**Expected result:** Semantic view `HOL_COCO_CWORK.TOOLS.HOT_FOOD_SALES_ANALYTICS` created with 3 tables, 2 relationships, and 8 verified queries.

### Step 3: Create Cortex Agent (Cortex Code)

Open the file `Prompts/agent.md` in Cortex Code and run the `/cortex-agent` skill with the file attached:

```
/cortex-agent @agent.md
```

**What CoCo will do:**
- Create a workspace directory for the agent
- Build the agent specification with:
  - Orchestration instructions (role, context, tool selection, boundaries, business rules)
  - Response instructions (assertive tone, chart generation, multilingual)
  - Tool configuration pointing to the semantic view
- Deploy the agent to HOL_COCO_CWORK.AGENTS

**Expected result:** Agent `HOL_COCO_CWORK.AGENTS.HOT_FOOD_SALES_AGENT` created and ready to answer questions.

### Step 4: Run Evaluations (Cortex Code)

Open the file `Prompts/evaluations.md` in Cortex Code and paste the content as a prompt:

```
@evaluations.md
```

**What CoCo will do:**
- Query the underlying tables to build ground truth answers
- Create an evaluation dataset with 10 questions across 5 categories:
  - Basic metrics (total revenue, transaction count, avg value)
  - Dimensional analysis (by state, by category, by discount)
  - Trend analysis (monthly revenue)
  - Rankings (top store, top item)
  - Filter analysis (spicy items)
- Register the dataset with Snowflake's evaluation framework
- Run the evaluation measuring `answer_correctness` and `logical_consistency`
- Present results with per-question scores

**Expected result:** Evaluation scores of ~93% answer correctness and 100% logical consistency.

## Project Structure

```
coco_cowork_agent_hol/
├── README.md                          ← You are here
├── Setup/
│   ├── setup.sql                      ← Run this first (Step 1)
│   ├── data/
│   │   ├── dim_store.csv              ← 100 convenience stores
│   │   ├── dim_item.csv               ← 100 hot food items
│   │   └── fact_item_sales.csv        ← 539K transactions
│   ├── generate_data.py               ← Script that generated the CSVs
│   └── upload_to_stage.py             ← Helper for uploading to stage
└── Prompts/
    ├── semantic_view.md               ← Step 2: Semantic view prompt
    ├── agent.md                       ← Step 3: Agent creation prompt
    └── evaluations.md                 ← Step 4: Evaluation prompt
```

Cortex Code will auto-generate workspace directories (e.g., `semantic_view_*/`, `HOL_COCO_CWORK_AGENTS_*/`) as it works through each step.

## Data Model

### DIM_STORE (100 rows)
| Column | Type | Description |
|--------|------|-------------|
| STORE_ID | VARCHAR(36) | UUID primary key |
| STORE_NAME | VARCHAR(100) | Store identifier (e.g., QuickStop #060) |
| ADDRESS | VARCHAR(200) | Street address |
| CITY | VARCHAR(100) | City |
| STATE | VARCHAR(2) | US state code (18 East Coast states) |
| ZIP_CODE | VARCHAR(10) | ZIP code |
| LATITUDE | FLOAT | Geo coordinate |
| LONGITUDE | FLOAT | Geo coordinate |
| OPENED_DATE | DATE | Store opening date |

### DIM_ITEM (100 rows)
| Column | Type | Description |
|--------|------|-------------|
| ITEM_ID | VARCHAR(36) | UUID primary key |
| ITEM_NAME | VARCHAR(200) | Item name |
| CATEGORY | VARCHAR(100) | Food category (19 categories) |
| UNIT_PRICE | NUMBER(10,2) | Standard price |
| COST_PRICE | NUMBER(10,2) | Cost to store |
| CALORIES | INTEGER | Calorie count |
| IS_SPICY | BOOLEAN | Spicy flag |

### FACT_ITEM_SALES (539,215 rows)
| Column | Type | Description |
|--------|------|-------------|
| SALE_ID | VARCHAR(36) | UUID primary key |
| STORE_ID | VARCHAR(36) | FK → DIM_STORE |
| ITEM_ID | VARCHAR(36) | FK → DIM_ITEM |
| SALE_DATE | DATE | Transaction date (Jan-Mar 2025) |
| QUANTITY_SOLD | INTEGER | Units sold |
| UNIT_PRICE | NUMBER(10,2) | Price at time of sale |
| DISCOUNT_PCT | INTEGER | Discount applied (0-15%) |
| TOTAL_SALES | NUMBER(12,2) | Revenue after discount |

## Cleanup

To remove all objects created by this lab:

```sql
DROP DATABASE IF EXISTS HOL_COCO_CWORK;
DROP WAREHOUSE IF EXISTS HOL_WH;
DROP COMPUTE POOL IF EXISTS HOL_COMPUTE_POOL;
```
