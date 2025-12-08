# Marine Corrosion Digital Twin

Digital twin for monitoring and predicting marine corrosion.

## Setup

1. Copy `.env` and set your database password:
```bash
DB_PASSWORD=your_password_here
```

2. Start the database:
```bash
docker compose up -d
```

3. Install Python dependencies (if working locally):
```bash
pip install -r requirements.txt
```

## Database

- **Host:** localhost:5432
- **Database:** marine_corrosion_db
- **Table:** sensor_data (timestamp, temperature, relative_humidity, corrosion_rate)

## Project Structure

```
src/            # Python code
data/           # CSV data files
config/         # Configuration files
docker/         # Database setup
notebooks/      # Jupyter notebooks
scripts/        # Utility scripts
```
