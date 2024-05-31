import os
from dotenv import load_dotenv
load_dotenv()


SECRET_KEY = "secret_key"
ALGORITHM = "HS256"

# Database url configuration
DATABASE_URL = "postgresql+psycopg2://{username}:{password}@{host}:{port}/{db_name}".format(
    host=os.getenv("POSTGRES_HOST",'db'),
    port=os.getenv("POSTGRES_PORT",5432),
    db_name=os.getenv("POSTGRES_DB"),
    username=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
)