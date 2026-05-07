# Rapaz - Backend Django

Backend desenvolvido em **Python**, utilizando **Django** e **Django REST Framework**, com integração a um banco de dados **MySQL** hospedado no Railway.

O projeto utiliza uma base de dados já existente. A tabela principal usada na autenticação é a tabela `Usuario`.

---

## Objetivo do projeto

Este backend tem como objetivo fornecer uma API simples para autenticação de usuários.

No momento, o foco principal é:

- Conectar o Django ao banco MySQL do Railway;
- Ler usuários da tabela `Usuario`;
- Realizar login usando `email` e `senha`;
- Gerar um token de autenticação;
- Permitir consulta de perfil usando esse token.

---

## Tecnologias utilizadas

- Python 3.11
- Django
- Django REST Framework
- MySQL
- Railway
- Gunicorn
- Thunder Client para testes de API
- SQLTools para testes diretos no banco

---

## Estrutura do banco utilizada

A autenticação utiliza a tabela existente:

```sql
Usuario
```

Campos principais:

```sql
id
nome
email
senha
tipo
data_criacao
```

O Django não cria essa tabela automaticamente. Ela já existe no banco.

Por isso, no model Django usamos:

```python
managed = False
```

Isso informa ao Django que ele deve apenas acessar a tabela, sem tentar criar, alterar ou remover sua estrutura.

---

## Endpoints disponíveis

### Login

Realiza o login do usuário usando `email` e `senha`.

```http
POST /api/auth/login/
```

Exemplo de URL em produção:

```txt
https://django-auth-backend-production.up.railway.app/api/auth/login/
```

Body esperado:

```json
{
  "email": "teste@teste.com",
  "senha": "123456"
}
```

Resposta esperada:

```json
{
  "mensagem": "Login realizado com sucesso.",
  "token": "TOKEN_GERADO",
  "usuario": {
    "id": 1,
    "nome": "Usuario Teste",
    "email": "teste@teste.com",
    "tipo": "comum",
    "data_criacao": "2026-05-06T..."
  }
}
```

---

### Perfil do usuário

Retorna os dados do usuário autenticado.

```http
GET /api/auth/profile/
```

Exemplo de URL em produção:

```txt
https://django-auth-backend-production.up.railway.app/api/auth/profile/
```

Header obrigatório:

```http
Authorization: Bearer TOKEN_GERADO
```

Resposta esperada:

```json
{
  "usuario": {
    "id": 1,
    "nome": "Usuario Teste",
    "email": "teste@teste.com",
    "tipo": "comum",
    "data_criacao": "2026-05-06T..."
  }
}
```

---

## Como testar se a API está online

Antes de testar o login, é possível verificar se a rota está respondendo.

Faça uma requisição `GET` para:

```txt
https://django-auth-backend-production.up.railway.app/api/auth/login/
```

Como a rota de login aceita apenas `POST`, a resposta esperada é:

```json
{
  "detail": "Método \"GET\" não é permitido."
}
```

Isso significa que:

- O deploy está online;
- O Django está respondendo;
- A rota `/api/auth/login/` existe;
- O backend está acessível publicamente pelo Railway.

---

## Variáveis de ambiente

No Railway, o serviço do backend precisa ter as seguintes variáveis:

```env
SECRET_KEY=sua_chave_secreta
DEBUG=False
ALLOWED_HOSTS=*
DB_NAME=railway
DB_USER=root
DB_PASSWORD=sua_senha_do_mysql
DB_HOST=mysql.railway.internal
DB_PORT=3306
```

### Observação sobre o host do banco

Quando o backend Django está rodando dentro do Railway, deve ser usado o host interno:

```txt
mysql.railway.internal
```

Quando for conectar ao banco pelo VS Code, SQLTools ou outro cliente externo, deve ser usado o host público fornecido pelo Railway, por exemplo:

```txt
trolley.proxy.rlwy.net
```

com a porta pública correspondente.

---

## Rodando o projeto localmente

Clone o repositório:

```bash
git clone https://github.com/Mr3K13/Rapaz.git
cd Rapaz
```

Crie o ambiente virtual:

```bash
python -m venv venv
```

Ative o ambiente virtual.

No Windows:

```bash
venv\Scripts\activate
```

No Linux/macOS:

```bash
source venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Crie um arquivo `.env` na raiz do projeto:

```env
SECRET_KEY=sua_chave_local
DEBUG=True
ALLOWED_HOSTS=*
DB_NAME=railway
DB_USER=root
DB_PASSWORD=sua_senha_do_mysql
DB_HOST=host_publico_do_mysql
DB_PORT=porta_publica_do_mysql
```

Teste se a configuração do Django está correta:

```bash
python manage.py check
```

Se estiver tudo certo, o retorno será parecido com:

```txt
System check identified no issues
```

Depois rode o servidor local:

```bash
python manage.py runserver
```

A API local ficará disponível em:

```txt
http://localhost:8000
```

---

## Rodando no Railway

O projeto está configurado para rodar com Gunicorn.

O start command usado no Railway é:

```bash
sh -c "gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 2 --timeout 120"
```

Esse comando inicia o servidor Django usando a porta definida automaticamente pelo Railway.

---

## Testando com Thunder Client

### 1. Testar se a rota existe

Método:

```txt
GET
```

URL:

```txt
https://django-auth-backend-production.up.railway.app/api/auth/login/
```

Resposta esperada:

```json
{
  "detail": "Método \"GET\" não é permitido."
}
```

Esse erro é esperado, pois o login aceita apenas `POST`.

---

### 2. Testar login

Método:

```txt
POST
```

URL:

```txt
https://django-auth-backend-production.up.railway.app/api/auth/login/
```

Header:

```http
Content-Type: application/json
```

Body:

```json
{
  "email": "teste@teste.com",
  "senha": "123456"
}
```

Se o usuário existir no banco e a senha estiver correta, será retornado um token.

---

### 3. Testar perfil autenticado

Método:

```txt
GET
```

URL:

```txt
https://django-auth-backend-production.up.railway.app/api/auth/profile/
```

Header:

```http
Authorization: Bearer TOKEN_GERADO
```

O token deve ser o valor retornado na rota de login.

---

## Testando o banco com SQLTools

Para testar o banco diretamente pelo VS Code, pode ser usada a extensão SQLTools.

Dados de conexão externa:

```txt
Host: host público do Railway
Porta: porta pública do Railway
Usuário: root
Senha: senha do MySQL
Database: railway
```

Comandos úteis:

```sql
SHOW DATABASES;
```

```sql
USE railway;
```

```sql
SHOW TABLES;
```

```sql
DESCRIBE Usuario;
```

```sql
SELECT id, nome, email, tipo, data_criacao
FROM Usuario
LIMIT 10;
```

Para criar um usuário de teste:

```sql
INSERT INTO Usuario (nome, email, senha, tipo)
VALUES ('Usuario Teste', 'teste@teste.com', '123456', 'comum');
```

Para remover o usuário de teste:

```sql
DELETE FROM Usuario
WHERE email = 'teste@teste.com';
```

---

## Diferença em relação à autenticação padrão do Django

Este projeto não utiliza a tabela padrão `auth_user` do Django para login.

A autenticação foi adaptada para usar a tabela existente `Usuario`.

Por isso, o login usa:

```json
{
  "email": "teste@teste.com",
  "senha": "123456"
}
```

e não:

```json
{
  "username": "joao",
  "password": "senha1234"
}
```

---

## Segurança

Atualmente, a autenticação compara a senha conforme ela está salva na tabela `Usuario`.

Em um sistema real de produção, o ideal é armazenar senhas com hash, usando recursos como:

```python
make_password()
check_password()
```

do próprio Django.

Isso evita que senhas sejam armazenadas em texto puro no banco de dados.

---

## Status atual

- Banco MySQL conectado no Railway;
- Tabela `Usuario` importada e funcionando;
- Leitura, escrita e remoção testadas no banco;
- Backend Django online;
- Gunicorn configurado;
- Porta pública do Railway corrigida;
- Rota de login funcionando;
- Login validando usuário pela tabela `Usuario`;
- Token sendo gerado no login;
- Rota de perfil disponível para teste com token.

---

## Próximos passos

Possíveis melhorias futuras:

- Implementar cadastro de usuário;
- Implementar logout;
- Implementar atualização de perfil;
- Adicionar hash de senha;
- Criar validação de token mais robusta;
- Separar permissões por tipo de usuário, como `comum` e `moderador`;
- Criar documentação Swagger/OpenAPI;
- Adicionar testes automatizados.
