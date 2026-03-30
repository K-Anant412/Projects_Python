import os
from dotenv import load_dotenv


load_dotenv()

class config:
    db_user=os.getenv("DB_USER")
    db_host=os.getenv("DB_HOST")
    db_password=os.getenv("DB_PASSWORD")
    db_port=os.getenv("DB_PORT")
    db_database=os.getenv("DB_NAME")
    
    sqlalchemy_database_url = (f"mysql//{db_user}:{db_password}@{db_host}:{db_port}/{db_database}")
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    