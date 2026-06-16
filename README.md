# Hands-On Lab: Building AI Agents with Cortex Code and CoWork


Build an end-to-end AI-powered analytics agent using Snowflake Cortex Code (CoCo) — from raw data to a production-ready Cortex Agent with evaluations.

>FOR A HTML VERSION OF THIS DOCUMENT -> [CLICK HERE](https://sfc-gh-cserrano.github.io/ml-enablement/coco_cowork_hol/)

## What You Will Build

1. **Star Schema Data Model** — Fact and dimension tables for convenience store hot food sales
2. **Semantic View** — An AI-ready data layer with verified queries for Cortex Analyst
3. **Cortex Agent** — A conversational analytics agent for C-Level executives with server-side skills
4. **Agent Skills** — Anomaly detection and sales report generation skills
5. **Evaluation Framework** — Ground truth dataset and automated agent evaluation

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
│  100 stores   │   2 relationships│   2 skills,          │
│  100 items    │   3 tables)      │   orchestration +    │
│  539K sales   │                  │   response instrs)   │
│               │  Skills Stage:   │                      │
│               │  anomaly_detect  │                      │
│               │  sales_report    │                      │
└───────────────┴──────────────────┴──────────────────────┘
```

## Getting Started: Load the Project into a Workspace

Before running the lab, you need the project files accessible in a Snowflake Workspace. Choose one of these two options:

### Option A: Git Workspace (Recommended)

Connect this public repository directly to a Snowflake Workspace — no SSH keys required.

**1. Create a Git Integration (one-time, run as ACCOUNTADMIN):**

```sql
USE ROLE ACCOUNTADMIN;

CREATE OR REPLACE API INTEGRATION HOL_GIT_INTEGRATION
  API_PROVIDER = GIT_HTTPS_API
  API_ALLOWED_PREFIXES = ('https://github.com/sfc-gh-cserrano/')
  ENABLED = TRUE;
```

**2. Create a Git Repository:**

```sql
CREATE OR REPLACE GIT REPOSITORY HOL_COCO_CWORK.DATA.HOL_REPO
  API_INTEGRATION = HOL_GIT_INTEGRATION
  ORIGIN = 'https://github.com/sfc-gh-cserrano/coco_cowork_agent_hol.git';
```

**3. Create a Workspace from the Git Repository:**

- Go to **Snowsight > Projects > Workspaces**
- Click **+ Workspace** > **Create from Git Repository**
- Select `HOL_COCO_CWORK.DATA.HOL_REPO` and branch `main`
- The workspace opens with all files ready to use

### Option B: Upload Files Manually

If you prefer not to use Git, download the project and upload files directly.

1. Download or clone this repository to your local machine
2. Go to **Snowsight > Projects > Workspaces**
3. Click **+ Workspace** to create a new blank workspace
4. Use the **Upload** button (or drag and drop) to upload the following folder structure:
   - `Setup/` (including `data/` subfolder with CSVs)
   - `Skills/`
   - `Prompts/`
5. Verify all files appear in the workspace file browser

---

## Prerequisites

- Snowflake account with ACCOUNTADMIN access
- Cortex Code (CoCo) desktop application installed
- A Snowflake Workspace (see Getting Started above)

## Lab Steps

> **Steps 2, 3, and 4 are run entirely in Cortex Code Desktop (CoCo).** Open the project folder in CoCo, then use the prompts below in the chat panel. Only Step 1 runs in a Snowflake Workspace.

### Step 1: Setup (Run in Snowflake Workspace)

This is the only step that requires manual execution. Everything else is done through Cortex Code prompts. Open each file directly in the Workspace and run it:

| # | File | Type | What it does |
|---|------|------|--------------|
| 1 | `Setup/01_setup.sql` | SQL | Creates warehouse, database, schemas, stages, tables |
| 2 | `Setup/02_copy_files.py` | Python | Uploads CSVs and skills to stages |
| 3 | `Setup/03_load_data.sql` | SQL | Loads data into tables and verifies counts |

1. In the Workspace file browser, open `Setup/01_setup.sql` and click **Run All**
2. Open `Setup/02_copy_files.py` and click **Run All**
3. Open `Setup/03_load_data.sql` and click **Run All**
4. Verify the final query shows: DIM_STORE = 100, DIM_ITEM = 100, FACT_ITEM_SALES = 539,215

### Step 2: Create Semantic View (Run in Cortex Code Desktop)

In the **Cortex Code Desktop** chat panel, type the following (the `@` attaches the file as context):

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

### Step 3: Create Cortex Agent (Run in Cortex Code Desktop)

In the **Cortex Code Desktop** chat panel, type:

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

### Step 4: Run Evaluations (Run in Cortex Code Desktop)

In the **Cortex Code Desktop** chat panel, type:

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
│   ├── 01_setup.sql                   ← SQL: warehouse, DB, schemas, stages, tables
│   ├── 02_copy_files.py               ← Python: upload CSVs and skills to stages
│   ├── 03_load_data.sql               ← SQL: load data into tables
│   ├── data/
│   │   ├── dim_store.csv              ← 100 convenience stores
│   │   ├── dim_item.csv               ← 100 hot food items
│   │   └── fact_item_sales.csv        ← 539K transactions
│   └── generate_data.py               ← Script that generated the CSVs
├── Skills/
│   ├── anomaly_detection/
│   │   └── SKILL.md                   ← Anomaly detection skill
│   └── sales_report/
│       └── SKILL.md                   ← Sales report generator skill
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
