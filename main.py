from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

#Configuraçao do FASTAPI
app = FastAPI(
    title="Teste API",
    description="API para teste de autenticação e gerenciamento de usuários",
)
#Criação da Rota de teste
@app.get("/")
def root():
    return {"message": "Bem-vindo à API de teste!"}
#alterado