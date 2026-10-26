import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv("/home/atharv/python/.env")
# try:
#     conn = psycopg.connect(
#         host=os.getenv("DB_HOST"),
#         port=os.getenv("DB_PORT"),
#         dbname=os.getenv("DB_NAME"),
#         user=os.getenv("DB_USER"),
#         password=os.getenv("DB_PASSWORD"),
#         row_factory=dict_row
#     ) 
#     #Because you're using dict_row, each record 
#     #should serialize as a JSON object with column names as keys. 
#     cursor = conn.cursor()
#     print("success")
# except Exception as error:
#     print(f"Connection failed: {error}")
#     time.sleep(10)

# cursor.execute("""
#     CREATE TABLE IF NOT EXISTS posts (
#         id SERIAL PRIMARY KEY,
#         title VARCHAR(255) NOT NULL,
#         content TEXT NOT NULL,
#         rating INTEGER
#     );
# """) 
# conn.commit()
SQLALCHEMY_DATABASE_URL = (
    f"postgresql+psycopg://{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/"
    f"{os.getenv('DB_NAME')}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()