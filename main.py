from fastapi import FastAPI
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware
import logging

from router.categoria_router import categoria_router
from router.auth_router import auth_router
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



# Para rodar a aplicação
# uvicorn main:app --reload

# Para gerar o aquivo requirements.txt
# pip freeze > requirements.txt