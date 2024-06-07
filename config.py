from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()

# Defina o caminho do banco de dados local
db_path = os.path.join(os.path.dirname(__file__), 'uruk.db')

class Config:
    
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{db_path}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
engine       = create_engine(Config.SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

# Defina seus modelos e tabelas aqui
from sqlalchemy import Column, Integer, Float, String

class Treino(Base):
    __tablename__  = 'Treino'
    ID_TREINO      = Column(Integer, primary_key=True)
    semana         = Column(String, nullable=False)
    agachamento    = Column(Float, nullable=False)
    supino         = Column(Float, nullable=False)
    lev_terra      = Column(Float, nullable=False)
    #exercicios = Base.relationship('Exercicio', backref='treino', lazy=True)

# Inicialize o banco de dados
init_db()

# Crie uma sessão e adicione dados
session = SessionLocal()

session.commit()
