import pandas as pd
import psycopg2
import yaml
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

with open('config/database.yaml', 'r') as f:
    db_cfg = yaml.safe_load(f)

# Connect to PostgreSQL database
conn = psycopg2.connect(
    dbname=db_cfg['dbname'],
    user=db_cfg['user'],
    password=os.getenv('DB_PASSWORD'),
    host=db_cfg['host'],
    port=db_cfg['port']
)
cur = conn.cursor()

# Read Excel file
df = pd.read_excel('data/raw/Corrosion_data_Hereon.xlsx')

conn.close()