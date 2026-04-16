import psycopg2
import requests
from pymongo import MongoClient
from app.core.config import settings

def _get_connection():
    """Retorna uma conexão com o PostgreSQL usando as configurações do settings"""
    return psycopg2.connect(
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        database=settings.DB_NAME,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD
    )

def get_mongo_client():
    """Retorna o cliente do MongoDB"""
    return MongoClient(settings.MONGO_URL)

def get_clima(cidade="Embu das Artes"):
    """Busca o clima atual para inteligência de marketing"""
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={settings.WEATHER_KEY}&units=metric&lang=pt_br"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            dados = response.json()
            temp = dados['main']['temp']
            desc = dados['weather'][0]['description']
            return f"{temp}°C e {desc}"
        return "Clima indisponível"
    except:
        return "Erro ao conectar com serviço de clima"

def init_db():
    """Cria a tabela de produtos se ela não existir (útil para o primeiro run)"""
    query = """
    CREATE TABLE IF NOT EXISTS produtos (
        id SERIAL PRIMARY KEY,
        nome VARCHAR(100) NOT NULL,
        categoria VARCHAR(50),
        preco DECIMAL(10,2),
        estoque_sistema INTEGER DEFAULT 0,
        criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    try:
        with _get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
            conn.commit()
            print("✅ Banco de Dados PostgreSQL verificado/inicializado.")
    except Exception as e:
        print(f"❌ Erro ao inicializar banco: {e}")