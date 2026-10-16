# Cadastro de Clientes Seguro — Roteiro

## Preparação (antes da aula)
1. Abra o **XAMPP** e inicie o **MySQL** (e o Apache, se quiser usar o phpMyAdmin).
2. No phpMyAdmin, aba **SQL**, cole o conteúdo de `setup.sql` e execute (como root).
3. No terminal: `pip install bcrypt cryptography mysql-connector-python`
4. Teste: `python app.py` (na pasta do projeto).

## Introdução (30 segundos)
"Meu projeto é um cadastro de clientes que aplica as 4 práticas de segurança do slide: hashing de senhas, menor privilégio, mascaramento de dados e criptografia em repouso."

## Demonstração (uns 7 minutos)

**1. Hashing de senhas (opção 1)**
- Cadastre dois usuários com a MESMA senha (ex.: `ana` e `bia`, senha `123456`).
- No phpMyAdmin, abra a tabela `usuarios`: os hashes são diferentes. Isso é o **salt**.
- Fale: "Se o banco vazar, ninguém vê a senha real. E o hash é de mão única."

**2. Login (opção 2)**
- Tente com senha errada (falha) e depois com a certa (funciona).
- Fale: "O sistema compara a senha digitada com o hash, sem precisar desfazer ele."

**3. Criptografia em repouso (opção 3)**
- Cadastre um cliente com cartão `1234 5678 9012 3456`.
- No phpMyAdmin, abra a tabela `clientes`: o cartão aparece como texto ilegível.
- Fale: "Quem copiar o banco só leva texto cifrado. A chave fica num arquivo separado (`chave.key`), fora do banco."

**4. Mascaramento de dados (opção 4)**
- Liste os clientes: aparece `**** **** **** 3456`.
- Fale: "Quem só precisa consultar o cliente não precisa ver o cartão inteiro."

**5. Menor privilégio (opção 5)**
- O programa tenta apagar dados e o banco bloqueia (`DELETE command denied`).
- Fale: "O sistema conecta com o `app_user`, que só pode SELECT e INSERT. Se alguém explorar uma falha, não consegue apagar nada."
- Se quiser reforçar: no phpMyAdmin (logado como root), mostre que o root consegue apagar. É essa diferença que o slide explica.

## Fechamento (30 segundos)
"Cada prática protege uma parte diferente: a senha, o acesso ao banco, a exibição do dado e o armazenamento em disco. Juntas, formam camadas de proteção."

## Se o professor perguntar...
- **"Por que o hash não é criptografia?"** Hash é de mão única (não dá para voltar à senha). Criptografia tem chave e dá para descriptografar. Por isso senha usa hash, e o cartão (que precisa ser recuperado) usa criptografia.
- **"A criptografia em repouso é de verdade?"** É uma versão simplificada para demonstrar o conceito: cifrei o campo pelo programa. Em produção, também se criptografa o disco ou o próprio banco (ex.: TDE).
- **"Onde fica a chave?"** Num arquivo separado do banco. Em produção ficaria em um cofre de chaves.
- **"Por que o app_user não é root?"** Para limitar o estrago se o sistema for invadido.
