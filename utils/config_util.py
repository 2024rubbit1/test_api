# utils/config_util.py
from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    BASE_URL = os.getenv("BASE_URL", "https://api.example.com")
    TOKEN = os.getenv("API_TOKEN")