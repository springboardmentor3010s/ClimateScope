import os
import pathlib
import pandas as pd
import logging
import zipfile
import shutil

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def download_and_process_data():
    """
    Downloads the Global Weather Repository dataset from Kaggle,
    processes it according to the established schema, and saves it.
    """
    project_root = pathlib.Path(__file__).parent.parent
    user_home = os.path.expanduser("~")
    kaggle_dir = os.path.join(user_home, ".kaggle")

    # Check for environment variables first (Cloud Deployment Safe)
    if 'KAGGLE_USERNAME' in os.environ and 'KAGGLE_KEY' in os.environ:
        logger.info("Using Kaggle credentials from environment variables.")
    else:
        # Check project root first, then ~/.kaggle/ for local development
        project_kaggle_json = project_root / "kaggle.json"
        home_kaggle_json = pathlib.Path(kaggle_dir) / "kaggle.json"
        
        if project_kaggle_json.exists():
            kaggle_json = str(project_kaggle_json)
        elif home_kaggle_json.exists():
            kaggle_json = str(home_kaggle_json)
        else:
            logger.error("Kaggle credentials not found in environment variables.")
            logger.error(f"Also, 'kaggle.json' not found at {project_kaggle_json} or {home_kaggle_json}.")
            logger.error("Please ensure 'kaggle.json' is present or environment variables are set.")
            import sys; sys.exit(1)
            
        import json
        with open(kaggle_json, 'r') as f:
            creds = json.load(f)
            os.environ['KAGGLE_USERNAME'] = creds['username']
            os.environ['KAGGLE_KEY'] = creds['key']

    raw_data_dir = project_root / "data" / "raw"
    processed_data_dir = project_root / "data" / "processed"
    
    # Ensure directories exist
    raw_data_dir.mkdir(parents=True, exist_ok=True)
    processed_data_dir.mkdir(parents=True, exist_ok=True)
    
    dataset_name = "nelgiriyewithana/global-weather-repository"
    csv_filename = "GlobalWeatherRepository.csv"
    
    try:
        from kaggle.api.kaggle_api_extended import KaggleApi
        api = KaggleApi()
        api.authenticate()
        logger.info(f"Downloading dataset {dataset_name}...")
        api.dataset_download_files(dataset_name, path=raw_data_dir, unzip=True)
        raw_csv_path = raw_data_dir / csv_filename
        
        if not raw_csv_path.exists():
            logger.error(f"Expected file {csv_filename} not found after download.")
            import sys; sys.exit(1)
            
    except Exception as e:
        logger.warning(f"Using cached raw data. Could not fetch from Kaggle: {e}")
        raw_csv_path = raw_data_dir / csv_filename
        if not raw_csv_path.exists():
             logger.error("No cached raw data found either. Aborting.")
             import sys; sys.exit(1)

    logger.info("Processing data...")
    try:
        # Load raw data
        df = pd.read_csv(raw_csv_path)
        
        # 1. Drop nulls
        df = df.dropna()
        
        # 2. Extract datetime features
        df['last_updated'] = pd.to_datetime(df['last_updated'])
        df['year'] = df['last_updated'].dt.year
        df['month'] = df['last_updated'].dt.month
        df['day'] = df['last_updated'].dt.day
        df['hour'] = df['last_updated'].dt.hour
        
        # Save processed data
        processed_csv_path = processed_data_dir / "climate_data.csv"
        df.to_csv(processed_csv_path, index=False)
        logger.info(f"Successfully processed and saved {len(df)} records to {processed_csv_path}")
        
    except Exception as e:
        logger.error(f"Error processing dataset: {e}")
        import sys; sys.exit(1)

    return True

if __name__ == "__main__":
    download_and_process_data()
