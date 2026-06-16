import csv
import random
from datetime import date, timedelta

random.seed(42)

# --- US East Coast states and cities ---
east_coast_locations = [
    ("New York", "NY"), ("Brooklyn", "NY"), ("Queens", "NY"), ("Buffalo", "NY"), ("Albany", "NY"),
    ("Manhattan", "NY"), ("Bronx", "NY"), ("Staten Island", "NY"), ("Syracuse", "NY"), ("Rochester", "NY"),
    ("Boston", "MA"), ("Worcester", "MA"), ("Springfield", "MA"), ("Cambridge", "MA"), ("Lowell", "MA"),
    ("Philadelphia", "PA"), ("Pittsburgh", "PA"), ("Allentown", "PA"), ("Erie", "PA"), ("Reading", "PA"),
    ("Newark", "NJ"), ("Jersey City", "NJ"), ("Trenton", "NJ"), ("Camden", "NJ"), ("Edison", "NJ"),
    ("Miami", "FL"), ("Orlando", "FL"), ("Tampa", "FL"), ("Jacksonville", "FL"), ("Fort Lauderdale", "FL"),
    ("Atlanta", "GA"), ("Savannah", "GA"), ("Augusta", "GA"), ("Columbus", "GA"), ("Macon", "GA"),
    ("Charlotte", "NC"), ("Raleigh", "NC"), ("Durham", "NC"), ("Greensboro", "NC"), ("Winston-Salem", "NC"),
    ("Virginia Beach", "VA"), ("Richmond", "VA"), ("Norfolk", "VA"), ("Arlington", "VA"), ("Alexandria", "VA"),
    ("Baltimore", "MD"), ("Annapolis", "MD"), ("Columbia", "MD"), ("Silver Spring", "MD"), ("Rockville", "MD"),
    ("Washington", "DC"), ("Georgetown", "DC"),
    ("Hartford", "CT"), ("New Haven", "CT"), ("Stamford", "CT"), ("Bridgeport", "CT"),
    ("Providence", "RI"), ("Warwick", "RI"), ("Cranston", "RI"),
    ("Portland", "ME"), ("Bangor", "ME"), ("Lewiston", "ME"),
    ("Burlington", "VT"), ("Montpelier", "VT"),
    ("Manchester", "NH"), ("Concord", "NH"), ("Nashua", "NH"),
    ("Wilmington", "DE"), ("Dover", "DE"),
    ("Charleston", "SC"), ("Columbia", "SC"), ("Greenville", "SC"),
    ("Savannah", "GA"), ("Brunswick", "GA"),
    ("Charleston", "WV"), ("Huntington", "WV"),
    ("St. Petersburg", "FL"), ("Naples", "FL"), ("Tallahassee", "FL"),
    ("Fayetteville", "NC"), ("Wilmington", "NC"),
    ("Hampton", "VA"), ("Chesapeake", "VA"),
    ("Frederick", "MD"), ("Hagerstown", "MD"),
    ("Hoboken", "NJ"), ("Paterson", "NJ"),
    ("Yonkers", "NY"), ("White Plains", "NY"),
    ("Brockton", "MA"), ("Quincy", "MA"),
    ("Scranton", "PA"), ("Bethlehem", "PA"),
    ("Daytona Beach", "FL"), ("Gainesville", "FL"),
    ("Savannah", "GA"), ("Athens", "GA"),
    ("Roanoke", "VA"), ("Lynchburg", "VA"),
]

# --- Generate DIM_STORE (100 stores) ---
stores = []
if len(east_coast_locations) < 100:
    extra_needed = 100 - len(east_coast_locations)
    east_coast_locations += random.sample(east_coast_locations, extra_needed)
used_locations = random.sample(east_coast_locations, 100)
for i, (city, state) in enumerate(used_locations):
    store_name = f"QuickStop #{i+1:03d}"
    address = f"{random.randint(100, 9999)} {random.choice(['Main', 'Oak', 'Elm', 'Maple', 'Pine', 'Cedar', 'Washington', 'Park', 'Lake', 'Hill'])} {random.choice(['St', 'Ave', 'Blvd', 'Rd', 'Dr', 'Ln'])}"
    zip_code = f"{random.randint(10000, 99999)}"
    latitude = round(random.uniform(25.0, 45.0), 6)
    longitude = round(random.uniform(-85.0, -70.0), 6)
    opened_date = date(random.randint(2015, 2023), random.randint(1, 12), random.randint(1, 28)).isoformat()
    stores.append({
        "STORE_NAME": store_name,
        "ADDRESS": address,
        "CITY": city,
        "STATE": state,
        "ZIP_CODE": zip_code,
        "LATITUDE": latitude,
        "LONGITUDE": longitude,
        "OPENED_DATE": opened_date
    })

# --- Generate DIM_ITEM (100 hot food items) ---
hot_food_items = [
    "Classic Hot Dog", "Chili Cheese Dog", "Jalapeño Dog", "Bacon Wrapped Dog", "Veggie Dog",
    "Pepperoni Pizza Slice", "Cheese Pizza Slice", "Supreme Pizza Slice", "BBQ Chicken Pizza Slice", "Margherita Pizza Slice",
    "Buffalo Chicken Wrap", "Grilled Chicken Wrap", "Spicy Bean Burrito", "Beef Burrito", "Chicken Quesadilla",
    "Crispy Chicken Tenders", "Spicy Chicken Tenders", "Popcorn Chicken", "Chicken Wings (6pc)", "Boneless Wings (6pc)",
    "Cheeseburger Slider", "Bacon Cheeseburger Slider", "Mushroom Swiss Slider", "BBQ Pulled Pork Slider", "Veggie Slider",
    "Mac & Cheese Cup", "Loaded Mac & Cheese", "Chili Con Carne Cup", "Beef Stew Cup", "Chicken Noodle Soup Cup",
    "Mozzarella Sticks (4pc)", "Jalapeño Poppers (4pc)", "Onion Rings (6pc)", "Loaded Fries", "Cheese Fries",
    "Breakfast Sausage Biscuit", "Egg & Cheese Biscuit", "Bacon Egg & Cheese Croissant", "Ham & Cheese Croissant", "Breakfast Burrito",
    "Corn Dog", "Mini Corn Dogs (6pc)", "Pretzel Dog", "Tornado (Pepperoni)", "Tornado (Buffalo Chicken)",
    "Fried Chicken Sandwich", "Spicy Chicken Sandwich", "Fish Sandwich", "Philly Cheesesteak", "Meatball Sub",
    "Taquitos (Beef 3pc)", "Taquitos (Chicken 3pc)", "Egg Rolls (2pc)", "Spring Rolls (2pc)", "Samosa (2pc)",
    "Stuffed Breadstick", "Garlic Knots (4pc)", "Cheesy Bread", "Pizza Rolls (8pc)", "Calzone",
    "Chicken Pot Pie", "Beef Pot Pie", "Sausage Roll", "Meat Pie", "Empanada (Beef)",
    "Empanada (Chicken)", "Empanada (Cheese)", "Jamaican Beef Patty", "Curry Chicken Patty", "Spinach Feta Wrap",
    "Grilled Cheese Sandwich", "BLT Sandwich", "Turkey Club Sandwich", "Italian Sub", "Cuban Sandwich",
    "Nashville Hot Chicken Bites", "Teriyaki Chicken Bowl", "Orange Chicken Bowl", "Fried Rice Bowl", "Lo Mein Bowl",
    "Cheese Quesadilla", "Steak Quesadilla", "Nachos Grande", "Loaded Nachos", "Chips & Queso",
    "Soup & Bread Bowl (Tomato)", "Soup & Bread Bowl (Broccoli)", "Clam Chowder Cup", "French Onion Soup Cup", "Chicken Tortilla Soup Cup",
    "Waffle Fries", "Sweet Potato Fries", "Tater Tots", "Hash Brown Patty", "Loaded Potato Wedges",
    "Soft Pretzel", "Soft Pretzel Bites", "Churros (3pc)", "Cinnamon Twists", "Funnel Cake Sticks"
]

categories = {
    "Hot Dogs": range(0, 5),
    "Pizza": range(5, 10),
    "Wraps & Burritos": range(10, 15),
    "Chicken": range(15, 25),
    "Sliders & Burgers": range(25, 30),
    "Soups & Bowls": range(30, 35),
    "Fried Snacks": range(35, 40),
    "Breakfast": range(40, 45),
    "Corn Dogs & Tornados": range(45, 50),
    "Sandwiches": range(50, 55),
    "International": range(55, 60),
    "Breads & Dough": range(60, 65),
    "Pies & Pastries": range(65, 70),
    "Empanadas & Patties": range(70, 75),
    "Deli Sandwiches": range(75, 80),
    "Asian Bowls": range(80, 85),
    "Mexican": range(85, 90),
    "Soups": range(90, 95),
    "Sides": range(95, 100),
}

item_category = {}
for cat, idx_range in categories.items():
    for idx in idx_range:
        item_category[idx] = cat

items = []
for i, item_name in enumerate(hot_food_items):
    category = item_category.get(i, "Other")
    unit_price = round(random.uniform(1.99, 9.99), 2)
    cost_price = round(unit_price * random.uniform(0.3, 0.5), 2)
    calories = random.randint(150, 800)
    is_spicy = item_name.lower().find("spicy") >= 0 or item_name.lower().find("jalapeño") >= 0 or item_name.lower().find("buffalo") >= 0 or item_name.lower().find("nashville") >= 0
    items.append({
        "ITEM_NAME": item_name,
        "CATEGORY": category,
        "UNIT_PRICE": unit_price,
        "COST_PRICE": cost_price,
        "CALORIES": calories,
        "IS_SPICY": is_spicy
    })

# --- Generate FACT_ITEM_SALES (daily sales for 90 days) ---
# Use STORE_NAME and ITEM_NAME as natural keys; Snowflake will generate UUIDs and join on these.
start_date = date(2025, 1, 1)
end_date = date(2025, 3, 31)
num_days = (end_date - start_date).days + 1

sales = []
for day_offset in range(num_days):
    current_date = start_date + timedelta(days=day_offset)
    is_weekend = current_date.weekday() >= 5

    for store in stores:
        num_items_sold = random.randint(40, 80)
        items_sold_today = random.sample(items, num_items_sold)

        for item in items_sold_today:
            base_qty = random.randint(1, 25)
            if is_weekend:
                base_qty = int(base_qty * random.uniform(1.2, 1.8))
            quantity_sold = base_qty
            unit_price = item["UNIT_PRICE"]
            discount_pct = random.choice([0, 0, 0, 0, 5, 10, 15, 20])
            total_sales = round(quantity_sold * unit_price * (1 - discount_pct / 100), 2)

            sales.append({
                "STORE_NAME": store["STORE_NAME"],
                "ITEM_NAME": item["ITEM_NAME"],
                "SALE_DATE": current_date.isoformat(),
                "QUANTITY_SOLD": quantity_sold,
                "UNIT_PRICE": unit_price,
                "DISCOUNT_PCT": discount_pct,
                "TOTAL_SALES": total_sales
            })

# --- Write CSVs ---
import os
output_dir = "/Users/carlosserrano/Documents/HOLs/coco_cowork_agent_hol/Setup/data"
os.makedirs(output_dir, exist_ok=True)

# DIM_STORE (no ID column - Snowflake generates UUID)
with open(f"{output_dir}/dim_store.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["STORE_NAME", "ADDRESS", "CITY", "STATE", "ZIP_CODE", "LATITUDE", "LONGITUDE", "OPENED_DATE"])
    writer.writeheader()
    writer.writerows(stores)

# DIM_ITEM (no ID column - Snowflake generates UUID)
with open(f"{output_dir}/dim_item.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["ITEM_NAME", "CATEGORY", "UNIT_PRICE", "COST_PRICE", "CALORIES", "IS_SPICY"])
    writer.writeheader()
    writer.writerows(items)

# FACT_ITEM_SALES (references natural keys; Snowflake will resolve to UUIDs)
with open(f"{output_dir}/fact_item_sales.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["STORE_NAME", "ITEM_NAME", "SALE_DATE", "QUANTITY_SOLD", "UNIT_PRICE", "DISCOUNT_PCT", "TOTAL_SALES"])
    writer.writeheader()
    writer.writerows(sales)

print(f"DIM_STORE: {len(stores)} rows")
print(f"DIM_ITEM: {len(items)} rows")
print(f"FACT_ITEM_SALES: {len(sales)} rows")
print("CSV files generated successfully.")
