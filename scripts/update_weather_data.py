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
    user_home = os.path.expanduser("~")
    kaggle_dir = os.path.join(user_home, ".kaggle")
    kaggle_json = os.path.join(kaggle_dir, "kaggle.json")
    
    if not os.path.exists(kaggle_json):
        logger.error(f"Kaggle API token not found at {kaggle_json}.")
        logger.error("Please download 'kaggle.json' from your Kaggle account settings and place it in the ~/.kaggle/ directory.")
        return False

    project_root = pathlib.Path(__file__).parent.parent
    raw_data_dir = project_root / "data" / "raw"
    processed_data_dir = project_root / "data" / "processed"
    
    # Ensure directories exist
    raw_data_dir.mkdir(parents=True, exist_ok=True)
    processed_data_dir.mkdir(parents=True, exist_ok=True)
    
    dataset_name = "nelgiriyewithana/global-weather-repository"
    csv_filename = "GlobalWeatherRepository.csv"
    
    try:
        import json
        with open(kaggle_json, 'r') as f:
            creds = json.load(f)
            os.environ['KAGGLE_USERNAME'] = creds['username']
            os.environ['KAGGLE_KEY'] = creds['key']
            
        from kaggle.api.kaggle_api_extended import KaggleApi
        api = KaggleApi()
        api.authenticate()
        logger.info(f"Downloading dataset {dataset_name}...")
        api.dataset_download_files(dataset_name, path=raw_data_dir, unzip=True)
        raw_csv_path = raw_data_dir / csv_filename
        
        if not raw_csv_path.exists():
            logger.error(f"Expected file {csv_filename} not found after download.")
            return False
            
    except Exception as e:
        logger.warning(f"Using cached raw data. Could not fetch from Kaggle: {e}")
        raw_csv_path = raw_data_dir / csv_filename
        if not raw_csv_path.exists():
             logger.error("No cached raw data found either. Aborting.")
             return False

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
        return False

    return True

if __name__ == "__main__":
    download_and_process_data()
