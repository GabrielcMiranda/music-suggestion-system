from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.auth_router import auth_router
from app.routers.user_router import user_router
from app.routers.share_router import share_router
from app.routers.user_music_router import user_music_router
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(share_router)
app.include_router(user_music_router) 

@app.get('/')
def home():
    return {'message': 'Backend está funcionando!', 'status': 'ok', 'app': 'Music Suggestion System'}
    
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)