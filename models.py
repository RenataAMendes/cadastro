from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, session
from werkzeug.security import generate_password_hash 

DATABASE_URL = 'sqlite:///database.db'
engine = create_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

Base = declarative_base()

class Usuario(Base):
    __tablename__='usuario'
    id_user = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    senha = Column(String(200), nullable=False)
    funcao = Column(String(100), nullable=False)
    matricula = Column(String(100), nullable=False)
    status_usuario = Column(Boolean, default=True)

class Categoria(Base):
    __tablename__= 'categoria'
    id_categoria = Column(Integer, primary_key=True)
    nome_categoria = Column(String(100), nullable=False)
    status_categoria = Column(Boolean, default=True)

    produtos = relationship('Estoque', back_populates='categoria')

class Estoque(Base):
    __tablename__='estoque'
    id_produto = Column(Integer, primary_key=True)
    nome_produto = Column(String(100), nullable=False)
    quantidade = Column(Integer, nullable=False)
    data_entrada = Column(DateTime, default=datetime.now)
    descriçao = Column(String(200), nullable=False)
    marca_produto = Column(String(100), nullable=False)
    status_estoque = Column(Boolean, default=True)
    id_categoria = Column(Integer, ForeignKey('categoria.id_categoria'), nullable=False)

    categoria = relationship('Categoria', back_populates='produtos')
    imagens = relationship('Imagem', back_populates='produto', cascade='all, delete-orphan')

class Imagem(Base):
    __tablename__= 'imagem'
    id_imagem = Column(Integer, primary_key=True)
    id_produto = Column(Integer, ForeignKey('estoque.id_produto'), nullable=False)
    caminho_imagem = Column(String(200), nullable=False)

    produto = relationship('Estoque', back_populates='imagens')


def cadastrar_usuario(nome: str, email: str, senha: str, funcao: str, matricula: str):
    session = SessionLocal()
    try:
        senha_hash = generate_password_hash(senha)
        novo_usuario = Usuario(
            nome=nome,
            email=email,
            senha=senha,
            funcao=funcao,
            matricula=matricula
        )
        session.add(novo_usuario)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e 
    finally:    session.close()

def cadastrar_produto(nome_produto: str, quantidade: int, descricao: str, marca_produto: str, id_categoria: int):
    session = SessionLocal()
    try:
        novo_produto = Estoque(
            nome_produto=nome_produto,
            quantidade=quantidade,
            descricao=descricao,
            marca_produto=marca_produto,
            id_categoria=id_categoria
        )
        session.add(novo_produto)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:    session.close()


def cadastrar_categoria(nome_categoria: str):
    session = SessionLocal()
    try:
        nova_categoria = Categoria(nome_categoria=nome_categoria, status_categoria=True)
        session.add(nova_categoria)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:  session.close()

def inserir_imagem(id_produto: int, caminho_imagem: str):
    session = SessionLocal()
    try:
        nova_imagem = Imagem(id_produto=id_produto, caminho_imagem=caminho_imagem)
        session.add(nova_imagem)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally: session.close()
    

def init_db() -> None:
    """Cria o banco de dados e as tabelas SQLite se não existirem."""
    Base.metadata.create_all(bind=engine)



