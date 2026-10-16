"""
Projeto: Cadastro de Clientes Seguro
Práticas do slide "Recursos de Segurança no Armazenamento":
  1. Hashing de senhas (bcrypt + salt)
  2. Princípio do menor privilégio (conecta com app_user, nunca com root)
  3. Mascaramento de dados (cartão aparece como **** **** **** 1234)
  4. Criptografia em repouso (cartão salvo cifrado com Fernet)

Como rodar:
  1. Inicie o MySQL no XAMPP
  2. Rode o setup.sql como root (phpMyAdmin > SQL)
  3. pip install bcrypt cryptography mysql-connector-python
  4. python app.py
"""

import os
import bcrypt
import mysql.connector
from mysql.connector import Error
from cryptography.fernet import Fernet

# ---------------------------------------------------------------
# CONEXÃO: usuário RESTRITO (menor privilégio), nunca o root
# ---------------------------------------------------------------
conn = mysql.connector.connect(
    host="127.0.0.1",
    port=3307,
    user="app_user",
    password="app_senha_123",
    database="seguranca_db",
)
cursor = conn.cursor()

# ---------------------------------------------------------------
# CHAVE DE CRIPTOGRAFIA: fica num arquivo, FORA do banco.
# (Se o banco vazar, o invasor não leva a chave junto.)
# ---------------------------------------------------------------
ARQUIVO_CHAVE = "chave.key"
if not os.path.exists(ARQUIVO_CHAVE):
    with open(ARQUIVO_CHAVE, "wb") as f:
        f.write(Fernet.generate_key())
with open(ARQUIVO_CHAVE, "rb") as f:
    fernet = Fernet(f.read())

usuario_logado = None


# ---------------------------------------------------------------
# 1. HASHING DE SENHAS
# ---------------------------------------------------------------
def cadastrar_usuario():
    nome = input("Novo usuário: ").strip()
    senha = input("Senha: ")
    hash_senha = bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()
    try:
        cursor.execute(
            "INSERT INTO usuarios (nome, senha_hash) VALUES (%s, %s)",
            (nome, hash_senha),
        )
        conn.commit()
        print("Usuário cadastrado! No banco ficou só o hash da senha.")
    except Error as e:
        print("Erro ao cadastrar:", e.msg)


def login():
    global usuario_logado
    nome = input("Usuário: ").strip()
    senha = input("Senha: ")
    cursor.execute("SELECT senha_hash FROM usuarios WHERE nome = %s", (nome,))
    linha = cursor.fetchone()
    if linha and bcrypt.checkpw(senha.encode(), linha[0].encode()):
        usuario_logado = nome
        print(f"Login realizado! Bem-vindo, {nome}.")
    else:
        print("Usuário ou senha incorretos.")


# ---------------------------------------------------------------
# 4. CRIPTOGRAFIA EM REPOUSO (cartão é cifrado antes de ir ao banco)
# ---------------------------------------------------------------
def cadastrar_cliente():
    nome = input("Nome do cliente: ").strip()
    cartao = input("Número do cartão (16 dígitos): ").replace(" ", "")
    if not (cartao.isdigit() and len(cartao) == 16):
        print("Cartão inválido: digite 16 números.")
        return
    cartao_cifrado = fernet.encrypt(cartao.encode()).decode()
    cursor.execute(
        "INSERT INTO clientes (nome, cartao_cifrado) VALUES (%s, %s)",
        (nome, cartao_cifrado),
    )
    conn.commit()
    print("Cliente cadastrado! No banco o cartão ficou cifrado.")


# ---------------------------------------------------------------
# 3. MASCARAMENTO DE DADOS (mostra só os 4 últimos dígitos)
# ---------------------------------------------------------------
def mascarar(cartao):
    return "**** **** **** " + cartao[-4:]


def listar_clientes():
    cursor.execute("SELECT id, nome, cartao_cifrado FROM clientes")
    clientes = cursor.fetchall()
    if not clientes:
        print("Nenhum cliente cadastrado.")
        return
    print("\n--- Clientes (cartão mascarado) ---")
    for id_, nome, cifrado in clientes:
        cartao = fernet.decrypt(cifrado.encode()).decode()
        print(f"{id_} | {nome} | {mascarar(cartao)}")
    print()


# ---------------------------------------------------------------
# 2. MENOR PRIVILÉGIO: mostra que o app_user NÃO pode apagar dados
# ---------------------------------------------------------------
def testar_permissao():
    print("Tentando apagar dados com o usuário restrito (app_user)...")
    try:
        # WHERE id = -1 não apaga nada, mesmo que a permissão existisse
        cursor.execute("DELETE FROM clientes WHERE id = -1")
        conn.commit()
        print("ATENÇÃO: o comando foi permitido (revise as permissões).")
    except Error as e:
        print("BLOQUEADO pelo banco:", e.msg)


# ---------------------------------------------------------------
# MENU
# ---------------------------------------------------------------
while True:
    print("\n=== CADASTRO DE CLIENTES SEGURO ===")
    print("1 - Cadastrar usuário")
    print("2 - Login")
    print("3 - Cadastrar cliente (precisa de login)")
    print("4 - Listar clientes (cartão mascarado, precisa de login)")
    print("5 - Testar menor privilégio (tentar apagar dados)")
    print("0 - Sair")
    opcao = input("Escolha: ").strip()

    if opcao == "1":
        cadastrar_usuario()
    elif opcao == "2":
        login()
    elif opcao in ("3", "4"):
        if not usuario_logado:
            print("Faça login primeiro (opção 2).")
        elif opcao == "3":
            cadastrar_cliente()
        else:
            listar_clientes()
    elif opcao == "5":
        testar_permissao()
    elif opcao == "0":
        break
    else:
        print("Opção inválida.")

cursor.close()
conn.close()
