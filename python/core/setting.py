import os
from dotenv import load_dotenv

load_dotenv()

# ==============================
# 데이터베이스 설정 로딩 클래스
# ==============================
class Setting:
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = int(os.getenv("DB_PORT"))
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")
    CHROMA_DIR = os.path.abspath("../storage/chroma_db")

setting = Setting()
