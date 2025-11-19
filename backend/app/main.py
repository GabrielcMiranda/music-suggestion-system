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
    allow_origins=[
        "http://localhost:4200",  # Angular dev
        "http://localhost:3000",  # Alternativo
        "http://localhost",       # Frontend Docker (porta 80)
        "http://localhost:80",    # Frontend Docker explícito
        "https://rhythmate.onrender.com",  # Produção Render
        "https://rhythmate-web.onrender.com"  # Alternativa
    ],
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
    return {'message': 'Backend está funcionando!', 'status': 'ok', 'app': 'Rhythmate'}

@app.get('/health')
def health_check():
    return {'status': 'healthy'}
    
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)