import sqlite3
from datetime import datetime, timezone

DB_NAME = 'database.db'

def obter_conexao():
    """Abre uma conexão com o banco de dados e ativa as chaves estrangeiras."""
    conexao = sqlite3.connect(DB_NAME)
    conexao.execute("PRAGMA foreign_keys = ON;")
    return conexao


def init_db() -> None:
    """Cria as tabelas no banco de dados SQLite utilizando SQL nativo."""
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        
        # Tabela de Usuários
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
        
        # Tabela de Categorias
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categoria (
                id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_categoria TEXT NOT NULL,
                status_categoria BOOLEAN NOT NULL DEFAULT 1,
                criado_em DATETIME NOT NULL
            );
        ''')
        
        # Tabela de Estoque
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS estoque (
                id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_produto TEXT NOT NULL,
                quantidade INTEGER NOT NULL DEFAULT 0,
                data_entrada DATETIME NOT NULL,
                descricao TEXT,
                marca_produto TEXT,
                status_estoque BOOLEAN NOT NULL DEFAULT 1,
                id_categoria INTEGER NOT NULL,
                id_user INTEGER NOT NULL,
                criado_em DATETIME NOT NULL,
                atualizado_em DATETIME NOT NULL,
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
                criado_em DATETIME NOT NULL,
                FOREIGN KEY (id_produto) REFERENCES estoque(id_produto) ON DELETE CASCADE
            );
        ''')


        conexao.commit()
        print("Banco de dados inicializado com sucesso!")


# ==========================================
# FUNÇÕES DE CADASTRO (CRUD)
# ==========================================

def cadastrar_usuario(nome: str, email: str, senha: str, funcao: str, matricula: str) -> int:
    """Cadastra um novo usuário com senha em texto puro e retorna o ID gerado."""
    agora = datetime.now(timezone.utc).isoformat()
    
    # Sintaxe corrigida (removidos os textos fixos que estavam poluindo a query)
    sql = '''
        INSERT INTO usuario (nome, email, senha, funcao, matricula, criado_em)
        VALUES (?, ?, ?, ?, ?, ?);
    '''
    
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        # Passando a variável 'senha' diretamente sem criptografia
        cursor.execute(sql, (nome, email, senha, funcao, matricula, agora))
        conexao.commit()
        return cursor.lastrowid


def cadastrar_produto(nome_produto: str, quantidade: int, descricao: str, marca_produto: str, id_categoria: int, id_user: int) -> int:
    """Cadastra um produto no estoque e retorna o ID gerado."""
    agora = datetime.now(timezone.utc).isoformat()
    
    sql = '''
        INSERT INTO estoque (nome_produto, quantidade, data_entrada, descricao, marca_produto, id_categoria, id_user, criado_em, updated_em)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
    '''
    
    # Nota: Caso sua coluna se chame 'atualizado_em' no banco, alterei o SQL abaixo para bater certinho com seu CREATE TABLE:
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
    

def realizar_login(email_digitado, senha_digitada):
    sql = "SELECT id_user, nome FROM usuario WHERE email = ? AND senha = ?;"
    
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        cursor.execute(sql, (email_digitado, senha_digitada))
        usuario = cursor.fetchone()
        
    if usuario:
        print(f"Bem-vindo de volta, {usuario[1]}!")
        return usuario # Retorna (id_user, nome)
    else:
        print("E-mail ou senha incorretos.")
        return None
    
    # ==========================================
# BLOCO DE TESTE DA INSERÇÃO E LOGIN
# ==========================================

if __name__ == "__main__":
    print("--- 1. Inicializando o Banco de Dados ---")
    init_db()  # Cria as tabelas se não existirem

    # Dados fakes para o teste
    nome_teste = "Carlos Silva"
    email_teste = "carlos@email.com"
    senha_teste = "estoque2026"
    funcao_teste = "Operador"
    matricula_teste = "MAT-999"

    print("\n--- 2. Testando a inserção de usuário ---")
    try:
        # Chama a sua função de cadastro
        id_gerado = cadastrar_usuario(
            nome=nome_teste,
            email=email_teste,
            senha=senha_teste,
            funcao=funcao_teste,
            matricula=matricula_teste
        )
        print(f"[SUCESSO] Usuário cadastrado! ID gerado no banco: {id_gerado}")

    except sqlite3.IntegrityError:
        # Como o e-mail e matrícula são UNIQUE, se você rodar o teste 2 vezes vai cair aqui
        print("[AVISO] O usuário de teste já estava cadastrado no banco de dados.")

    print("\n--- 3. Testando o Login (Dados Corretos) ---")
    # Tenta logar com o e-mail e a senha que acabamos de cadastrar
    usuario_logado = realizar_login(email_teste, senha_teste)
    
    if usuario_logado:
        print(f"[SUCESSO] Retorno da função: {usuario_logado}")  # Deve printar (id, nome)
    else:
        print("[ERRO] O login deveria ter funcionado!")

    print("\n--- 4. Testando o Login (Senha Errada) ---")
    # Força um erro de senha para ver se a função bloqueia corretamente
    realizar_login(email_teste, "senha_errada_123")