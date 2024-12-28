from pyBreezeChMS.breeze.breeze import BreezeApi
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Breeze API
breeze_api = BreezeApi(
    breeze_url=os.getenv('breeze_url'),
    api_key=os.getenv('api_key')
)
