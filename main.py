import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from router.auth_router import auth_router
from router.categoria_router import categoria_router
from router.marca_router import marca_router
from router.usuario_router import usuario_router

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

app = FastAPI()
logger = logging.getLogger(__name__)

origins = [
    "http://localhost:3000",
]
app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])

app.include_router(auth_router)
app.include_router(usuario_router)
app.include_router(categoria_router)
app.include_router(marca_router)

# Para rodar a aplicação
# uvicorn main:app --reload

# Para gerar o aquivo requirements.txt
# pip freeze > requirements.txt
