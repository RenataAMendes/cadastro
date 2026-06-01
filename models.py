from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, create_engine, Text
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from werkzeug.security import generate_password_hash

DATABASE_URL = 'sqlite:///database.db'
engine = create_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuario'
    id_user = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True, index=True)
    senha = Column(String(200), nullable=False)
    funcao = Column(String(100), nullable=False)
    matricula = Column(String(100), nullable=False, unique=True, index=True)
    status_usuario = Column(Boolean, default=True)
    criado_em = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    produtos = relationship('Estoque', back_populates='usuario', cascade='all, delete-orphan')

class Categoria(Base):
    __tablename__= 'categoria'
    id_categoria = Column(Integer, primary_key=True)
    nome_categoria = Column(String(100), nullable=False)
    status_categoria = Column(Boolean, default=True)

    criado_em = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    produtos = relationship('Estoque', back_populates='categoria')

class Estoque(Base):
    __tablename__='estoque'
    id_produto = Column(Integer, primary_key=True)
    nome_produto = Column(String(100), nullable=False)
    quantidade = Column(Integer, nullable=False, default=0)
    data_entrada = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    descricao = Column(Text, nullable=True)
    marca_produto = Column(String(100), nullable=True)
    status_estoque = Column(Boolean, default=True)
    id_categoria = Column(Integer, ForeignKey('categoria.id_categoria'), nullable=False)
    id_user = Column(Integer, ForeignKey('usuario.id_user'), nullable=False)
    criado_em = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    atualizado_em = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    categoria = relationship('Categoria', back_populates='produtos')
    imagens = relationship('Imagem', back_populates='produto', cascade='all, delete-orphan')
    usuario = relationship('Usuario', back_populates='produtos')

class Imagem(Base):
    __tablename__= 'imagem'
    id_imagem = Column(Integer, primary_key=True)
    id_produto = Column(Integer, ForeignKey('estoque.id_produto'), nullable=False)
    caminho_imagem = Column(String(300), nullable=False)
    criado_em = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    produto = relationship('Estoque', back_populates='imagens')


def cadastrar_usuario(nome: str, email: str, senha: str, funcao: str, matricula: str):
    session = SessionLocal()
    try:
        senha_hash = generate_password_hash(senha)
        novo_usuario = Usuario(
            nome=nome,
            email=email,
            senha=senha_hash,
            funcao=funcao,
            matricula=matricula
        )
        session.add(novo_usuario)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e 
    finally:
        session.close()

def cadastrar_produto(nome_produto: str, quantidade: int, descricao: str, marca_produto: str, id_categoria: int, id_user: int):
    session = SessionLocal()
    try:
        novo_produto = Estoque(
            nome_produto=nome_produto,
            quantidade=quantidade,
            descricao=descricao,
            marca_produto=marca_produto,
            id_categoria=id_categoria,
            id_user=id_user
        )
        session.add(novo_produto)
        session.commit()
        session.refresh(novo_produto)
        return novo_produto
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def cadastrar_categoria(nome_categoria: str):
    session = SessionLocal()
    try:
        nova_categoria = Categoria(nome_categoria=nome_categoria, status_categoria=True)
        session.add(nova_categoria)
        session.commit()
        return nova_categoria
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def inserir_imagem(id_produto: int, caminho_imagem: str):
    session = SessionLocal()
    try:
        nova_imagem = Imagem(id_produto=id_produto, caminho_imagem=caminho_imagem)
        session.add(nova_imagem)
        session.commit()
        return nova_imagem
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
    

def init_db() -> None:
    """Cria o banco de dados e as tabelas SQLite se não existirem."""
    Base.metadata.create_all(bind=engine)



