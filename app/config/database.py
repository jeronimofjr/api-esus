from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError
import time
import os
from dotenv import load_dotenv

load_dotenv()
 
Base = declarative_base()

db = os.environ.get("DB_NAME")
user = os.environ.get("DB_USER")
password = os.environ.get("DB_PASSWORD")
host = os.environ.get("DB_HOST")
port = os.environ.get("DB_PORT")

class DatabaseConfig:
    def __init__(self):
        self.engine = None
        self.SessionLocal = None
        
    def create_engine_with_retry(self, max_retries=10, delay=5):
        
        retries = 0
        while retries < max_retries:
            try:
                self.engine = create_engine(
                    f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}',
                    pool_pre_ping=True
                )
                
                self.engine.connect()
                print("Conexão com banco de dados estabelecida!")
                return self.engine
            except OperationalError as e:
                retries += 1
                print(f"Tentativa {retries}/{max_retries} falhou. Aguardando {delay}s...")
                time.sleep(delay)
        
        raise Exception("Não foi possível conectar ao banco de dados")
    
    def init_database(self):
        self.create_engine_with_retry()
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        return self.engine
    
    def get_session(self):
        if not self.SessionLocal:
            raise Exception("Banco de dados não inicializado")
        return self.SessionLocal()


db_config = DatabaseConfig()

