# Goal
Generate synthetic data for 100 Convenience store accross the U.S. east coast. Data will track 100 hot food items sales across all the stores. For a period of 6 months. 

# Ouput
- Individual CSV files for each table
- Main setup.sql script to load each CSV using copy into
- Single loading script to be executed from Snowflake workspaces.

# Specifications
- Database: HOL_COCO_CWORK
- Schemas: Data, Agents, Tools
- Create a Star Schema with the following specs:
    - Dimensions : DIM_STORE, DIM_ITEM
    - Fact: FACT_ITEM_SALES (Item sales per store per day)
- Use UUIDs for every ID field on tables. 
- Any stage created must use Snowflake_SSE encryption.
- Create a dedicated xsmall warehouse for this - Name it HOL_WH.
- Create the necessary file formats for the data load. 
