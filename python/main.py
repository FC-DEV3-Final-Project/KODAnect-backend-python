from python.application.api import endpoints
from fastapi import FastAPI

app = FastAPI(title="부서 챗봇")
app.include_router(endpoints.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("python.main:app", host="127.0.0.1", port=8000, reload=True)
