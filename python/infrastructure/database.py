import aiomysql
from python.core.setting import setting

# ==============================
# MySQL Connection 생성 함수
# ==============================
async def get_connection():
    return await aiomysql.connect(
        host=setting.DB_HOST,
        port=setting.DB_PORT,
        user=setting.DB_USER,
        password=setting.DB_PASSWORD,
        db=setting.DB_NAME,
        charset="utf8mb4",
        autocommit=True
    )
