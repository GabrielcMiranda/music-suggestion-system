from fastapi import FastAPI
from app.routers.auth_router import auth_router
from app.routers.user_router import user_router
import uvicorn

app = FastAPI()
app.include_router(auth_router)
app.include_router(user_router)

@app.get('/')
def home():
    return 'Hello World'

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)