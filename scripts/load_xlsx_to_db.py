import pandas as pd
import psycopg2
import yaml
from dotenv import load_dotenv
import os

from sqlalchemy import create_engine

# Load environment variables from .env file
load_dotenv()

def get_config_value(yaml_value, env_var, cast=str):
    # Try to get from environment, else from yaml, else from default in yaml string
    env_val = os.getenv(env_var)
    if env_val is not None:
        return cast(env_val)
    # Try to parse default from ${VAR:default}
    if isinstance(yaml_value, str) and yaml_value.startswith("${") and ":" in yaml_value:
        return cast(yaml_value.split(":", 1)[1].rstrip("}"))
    return cast(yaml_value)

with open('config/database.yaml', 'r') as f:
    db_cfg_raw = yaml.safe_load(f)['database']

db_cfg = {
    'host': get_config_value(db_cfg_raw['host'], 'DB_HOST'),
    'port': get_config_value(db_cfg_raw['port'], 'DB_PORT', int),
    'name': get_config_value(db_cfg_raw['name'], 'DB_NAME'),
    'user': get_config_value(db_cfg_raw['user'], 'DB_USER'),
    'password': get_config_value(db_cfg_raw['password'], 'DB_PASSWORD'),
}

conn = psycopg2.connect(
    dbname=db_cfg['name'],
    user=db_cfg['user'],
    password=db_cfg['password'],
    host=db_cfg['host'],
    port=db_cfg['port']
)
cur = conn.cursor()

# Read Excel file
df = pd.read_excel(
    'data/raw/Corrosion_data_Hereon.xlsx',
    header=7,         # Row 8 is index 7
    usecols="Y:AH",   # Excel columns Y to AH
    nrows=8736        # Number of rows to read (8743 - 8 + 1)
)

# Convert Unix Timestamp to datetime (PostgreSQL expects timestamp)
df['timestamp'] = pd.to_datetime(df['Unix Timestamp (UTC).2'], unit='s', utc=True)

# Prepare DataFrame for DB insert (rename columns if needed)
df_db = df.rename(columns={
    'Unix Timestamp (UTC).2': 'unix_timestamp',
    'Ts (°C).2': 'temperature',
    'RH (%).2': 'relative_humidity',
    'Free Corr (µA) - Gangseo-gu, Korea': 'corrosion_rate'
})

# Only keep the columns needed for the table
df_db = df_db[['timestamp', 'unix_timestamp', 'temperature', 'relative_humidity', 'corrosion_rate']]

# Insert into database
engine = create_engine(
    f"postgresql+psycopg2://{db_cfg['user']}:{db_cfg['password']}@{db_cfg['host']}:{db_cfg['port']}/{db_cfg['name']}"
)
df_db.to_sql('sensor_data', engine, if_exists='append', index=False)