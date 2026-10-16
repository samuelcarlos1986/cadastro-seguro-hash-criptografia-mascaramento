-- Projeto: Cadastro de Clientes Seguro
-- Rode este arquivo UMA VEZ, logado como root (phpMyAdmin > aba SQL, ou terminal).

CREATE DATABASE IF NOT EXISTS seguranca_db CHARACTER SET utf8mb4;
USE seguranca_db;

-- Usuários do sistema (senha guardada só como HASH bcrypt)
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) UNIQUE NOT NULL,
    senha_hash VARCHAR(100) NOT NULL
);

-- Clientes (cartão guardado CRIPTOGRAFADO)
CREATE TABLE IF NOT EXISTS clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cartao_cifrado TEXT NOT NULL
);

-- PRINCÍPIO DO MENOR PRIVILÉGIO:
-- usuário restrito que o programa usa. Só pode LER (SELECT) e INSERIR (INSERT).
-- Não pode apagar, alterar nem dropar tabelas.
CREATE USER IF NOT EXISTS 'app_user'@'localhost' IDENTIFIED BY 'app_senha_123';
GRANT SELECT, INSERT ON seguranca_db.* TO 'app_user'@'localhost';
FLUSH PRIVILEGES;
