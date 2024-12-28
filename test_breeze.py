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

# Test connection by getting people
try:
    people = breeze_api.get_people()
    print(f"Successfully connected to Breeze!")
    print(f"Found {len(people)} people in the database")
except Exception as e:
    print(f"Error connecting to Breeze: {str(e)}")
