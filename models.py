import sqlite3
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash

DB_NAME = 'database.db'
#pronto banco sema o SQLALCHEMY SO O SQLIT3 PURO, USEI A IA SO PARA REVISAR DIGITEI TUDO A MÃO
def obter_conexao():
    """Abre uma conexão com o banco de dados e ativa as chaves estrangeiras."""
    conexao = sqlite3.connect(DB_NAME)
    conexao.execute("PRAGMA foreign_keys = ON;")
    return conexao



def init_db() -> None:
    """Cria as tabelas no banco de dados SQLite utilizando SQL nativo."""
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        
        #  Tabela de Usuários
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuario (
                id_user INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL,
                funcao TEXT NOT NULL,
                matricula TEXT UNIQUE NOT NULL,
                status_usuario BOOLEAN NOT NULL DEFAULT 1,
                criado_em TEXT NOT NULL
            );
        ''')
        
        # 2. Tabela de Categorias
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categoria (
                id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_categoria TEXT NOT NULL,
                status_categoria BOOLEAN NOT NULL DEFAULT 1,
                criado_em TEXT NOT NULL
            );
        ''')
        
        # Tabela de Estoque
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS estoque (
                id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_produto TEXT NOT NULL,
                quantidade INTEGER NOT NULL DEFAULT 0,
                data_entrada TEXT NOT NULL,
                descricao TEXT,
                marca_produto TEXT,
                status_estoque BOOLEAN NOT NULL DEFAULT 1,
                id_categoria INTEGER NOT NULL,
                id_user INTEGER NOT NULL,
                criado_em TEXT NOT NULL,
                atualizado_em TEXT NOT NULL,
                FOREIGN KEY (id_categoria) REFERENCES categoria(id_categoria) ON DELETE CASCADE,
                FOREIGN KEY (id_user) REFERENCES usuario(id_user) ON DELETE CASCADE
            );
        ''')
        
        # Tabela de Imagens
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS imagem (
                id_imagem INTEGER PRIMARY KEY AUTOINCREMENT,
                id_produto INTEGER NOT NULL,
                caminho_imagem TEXT NOT NULL,
                criado_em TEXT NOT NULL,
                FOREIGN KEY (id_produto) REFERENCES estoque(id_produto) ON DELETE CASCADE
            );
        ''')
        
        conexao.commit()
        print("Banco de dados inicializado com sucesso!")


# ==========================================
# FUNÇÕES DE CADASTRO (CRUD)
# ==========================================

def cadastrar_usuario(nome: str, email: str, senha: str, funcao: str, matricula: str) -> int:
    """Cadastra um novo usuário e retorna o ID gerado."""
    senha_hash = generate_password_hash(senha)
    agora = datetime.now(timezone.utc).isoformat()
    
    sql = '''
        INSERT INTO usuario (nome, email, senha, funcao, matricula, criado_em)
        VALUES (?, ?, ?, ?, ?, ?);
    '''
    
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(sql, (nome, email, senha_hash, funcao, matricula, agora))
        conexao.commit()
        return cursor.lastrowid  # Retorna o id_user gerado pelo banco


def cadastrar_produto(nome_produto: str, quantidade: int, descricao: str, marca_produto: str, id_categoria: int, id_user: int) -> int:
    """Cadastra um produto no estoque e retorna o ID gerado."""
    agora = datetime.now(timezone.utc).isoformat()
    
    sql = '''
        INSERT INTO estoque (nome_produto, quantidade, data_entrada, descricao, marca_produto, id_categoria, id_user, criado_em, atualizado_em)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
    '''
    
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(sql, (nome_produto, quantidade, agora, descricao, marca_produto, id_categoria, id_user, agora, agora))
        conexao.commit()
        return cursor.lastrowid  


def cadastrar_categoria(nome_categoria: str) -> int:
    """Cadastra uma nova categoria de produto."""
    agora = datetime.now(timezone.utc).isoformat()
    
    sql = '''
        INSERT INTO categoria (nome_categoria, criado_em)
        VALUES (?, ?);
    '''
    
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(sql, (nome_categoria, agora))
        conexao.commit()
        return cursor.lastrowid  


def inserir_imagem(id_produto: int, caminho_imagem: str) -> int:
    """Vincula o caminho de uma imagem a um produto do estoque."""
    agora = datetime.now(timezone.utc).isoformat()
    
    sql = '''
        INSERT INTO imagem (id_produto, caminho_imagem, criado_em)
        VALUES (?, ?, ?);
    '''
    
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(sql, (id_produto, caminho_imagem, agora))
        conexao.commit()
        return cursor.lastrowid  