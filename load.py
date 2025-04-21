import os
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine, text
from extract import fetch_data_from_api
from transform import clean_data

# --------------------------
# 1. Load environment variables
# --------------------------
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")  # Should be "postgres" in Docker
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# --------------------------
# 2. Extract and Transform
# --------------------------
print("📥 Fetching data from API...")
raw_df = fetch_data_from_api()
print(f"✅ Retrieved {len(raw_df)} raw rows")

print("🧼 Cleaning data...")
df = clean_data(raw_df)
print(f"✅ Cleaned data has {len(df)} rows")

# --------------------------
# 3. Connect to PostgreSQL and load
# --------------------------
print("🔌 Connecting to PostgreSQL...")
try:
    engine = create_engine(DATABASE_URL)

    with engine.connect() as conn:

        conn.execute(text("DROP TABLE IF EXISTS inspections CASCADE"))

        conn.execute(text("""
            CREATE TABLE inspections (
                inspection_id VARCHAR PRIMARY KEY,
                facility_type VARCHAR,
                risk VARCHAR,
                zip INTEGER,
                inspection_date DATE,
                inspection_type VARCHAR,
                result VARCHAR,
                violations TEXT,
                cleaned_inspection_type VARCHAR
            );
        """))

        print("✅ Table 'inspections' created")

        # Insert data using pandas
    df.to_sql("inspections", engine, if_exists="append", index=False, method='multi', chunksize=10000)
    
    #df_small = df.head(50)
    #df_small.to_sql("inspections", engine, if_exists="replace", index=False, method="multi")
    conn.commit()
    print("✅ All rows inserted.")
    print("🚀 Data loaded into PostgreSQL!")

except Exception as e:
    print("❌ Error connecting to database:", e)
