from pathlib import Path
import os
import json
import dotenv

BASE_DIR = Path(__file__).resolve().parent

if not os.environ.get('MONGO_URI') or not os.environ.get('GOOGLE_CLOUD_KEY'):
    dotenv.load_dotenv(BASE_DIR / 'credentials.env')

MONGO_URI = os.environ.get('MONGO_URI')
GOOGLE_CLOUD_KEY = json.loads(os.environ.get('GOOGLE_CLOUD_KEY'))