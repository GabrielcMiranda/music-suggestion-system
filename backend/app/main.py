from fastapi import FastAPI
from app.routers.auth_router import auth_router
from app.routers.user_router import user_router
from app.routers.share_router import share_router
from app.routers.user_music_router import user_music_router
import uvicorn

app = FastAPI()
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(share_router)
app.include_router(user_music_router) 

@app.get('/')
def home():
    return 'Hello World'
    
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)