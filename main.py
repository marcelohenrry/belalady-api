from fastapi import FastAPI

app = FastAPI()

from router.auth_router import auth_router
from router.cliente_router import cliente_router

app.include_router(auth_router)
app.include_router(cliente_router)



# Para rodar a aplicação
# uvicorn main:app --reload

# Para gerar o aquivo requirements.txt
# pip freeze > requirements.txt