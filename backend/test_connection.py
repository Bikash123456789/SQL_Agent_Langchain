import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import pandas as pd

# Load environment variables
load_dotenv()

# Get credentials from .env
user = os.getenv("SNOWFLAKE_USER")
password = os.getenv("SNOWFLAKE_PASSWORD")
account = os.getenv("SNOWFLAKE_ACCOUNT")
database = os.getenv("SNOWFLAKE_DATABASE")
schema = os.getenv("SNOWFLAKE_SCHEMA")
warehouse = os.getenv("SNOWFLAKE_WAREHOUSE")


# Build Snowflake SQLAlchemy URI
uri = (
    f"snowflake://{user}:{password}@{account}/{database}/{schema}?warehouse={warehouse}"
)

print(uri)

# Test connection and fetch data
try:
    engine = create_engine(uri)
    with engine.connect() as conn:
        df = pd.read_sql("SELECT * FROM ORDERS LIMIT 5", conn)
        print("✅ Connection successful. Sample data:")
        print(df)
except Exception as e:
    print(f"❌ Connection failed: {e}")
