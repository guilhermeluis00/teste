import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv
import os

# Configuração da conexão com o banco de dados
load_dotenv(encoding='utf-8')

# Função para obter uma conexão com o banco de dados
def get_connection():
    return psycopg.connect(
        os.getenv("DATABASE_URL"),
        row_factory=dict_row
    )
