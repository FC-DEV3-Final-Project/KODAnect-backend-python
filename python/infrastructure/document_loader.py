import aiomysql
from python.infrastructure.database import get_connection
from langchain.schema import Document


async def load_org_documents():
    conn = await get_connection()  # Connection 생성
    async with conn.cursor(aiomysql.DictCursor) as cursor:
        cursor.execute("SELECT hq_name, dept1_name, dept2_name, job_desc, tel_no FROM tb25_840_org_chart")
        org_charts = await cursor.fetchall()  # sql 실행 결과

    await conn.ensure_closed()

    org_descriptions = []  # 각 행을 저장할 리스트
    for org_chart in org_charts:
        hq_name = org_chart["hq_name"]
        dept1_name = org_chart["dept1_name"]
        dept2_name = org_chart["dept2_name"]
        job_desc = org_chart["job_desc"]
        tel_no = org_chart["tel_no"]
        dept_full_name = f"{hq_name}-{dept1_name}-" + (f"{dept2_name}" if dept2_name else "")  # 행마다 보기 쉽게 문자열 포맷팅

        org_descriptions.append(f"부서:{dept_full_name}\n 업무 내용:{job_desc}\n 전화번호:{tel_no}")

    return [Document(page_content=org_description) for org_description in org_descriptions]
