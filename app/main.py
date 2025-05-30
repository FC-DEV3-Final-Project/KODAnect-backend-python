from app.api import endpoints
from app.exception.config.global_exception_handler import not_found_handler
from fastapi import FastAPI
from http import HTTPStatus

app = FastAPI(title="부서 챗봇")
app.include_router(endpoints.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
