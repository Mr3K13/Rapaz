# django-auth-backend

Backend de autenticação construído com **Django 4.2** e **Django REST Framework**, utilizando **MySQL** como banco de dados.

---

## Endpoints disponíveis

| Método | Rota | Descrição | Autenticação |
|--------|------|-----------|--------------|
| POST | `/api/auth/register/` | Cadastro de novo usuário | Não |
| POST | `/api/auth/login/` | Login e obtenção do token | Não |
| POST | `/api/auth/logout/` | Logout (invalida o token) | Token |
| GET | `/api/auth/profile/` | Retorna o perfil do usuário | Token |
| PUT | `/api/auth/profile/update/` | Atualiza o perfil do usuário | Token |
| GET | `/api/auth/user/<id>/` | Detalhes de um usuário por ID | Token |

---

## Variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=False
ALLOWED_HOSTS=*

DB_NAME=railway
DB_USER=raiz
DB_PASSWORD=sua-senha
DB_HOST=trolley.proxy.rlwy.net
DB_PORT=35780
```

---

## Executando localmente

### Pré-requisitos

- Python 3.11+
- MySQL 8+ ou acesso ao banco Railway
- `libmysqlclient-dev` instalado no sistema

### Instalação

```bash
# Clone o repositório
git clone <url-do-repositorio>
cd django-auth-backend

# Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente
cp .env.example .env
# Edite o .env com suas credenciais

# Execute as migrações
python manage.py migrate

# Crie um superusuário (opcional)
python manage.py createsuperuser

# Inicie o servidor de desenvolvimento
python manage.py runserver
```

---

## Executando com Docker

```bash
docker build -t django-auth-backend .
docker run -p 8000:8000 --env-file .env django-auth-backend
```

---

## Exemplos de uso

### Cadastro

```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "joao",
    "email": "joao@exemplo.com",
    "password": "senha1234",
    "password_confirm": "senha1234",
    "first_name": "João",
    "last_name": "Silva"
  }'
```

### Login

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "joao", "password": "senha1234"}'
```

### Perfil (autenticado)

```bash
curl http://localhost:8000/api/auth/profile/ \
  -H "Authorization: Token <seu-token>"
```

---

## Tecnologias

- [Django 4.2](https://docs.djangoproject.com/en/4.2/)
- [Django REST Framework 3.14](https://www.django-rest-framework.org/)
- [django-cors-headers 4.0](https://github.com/adamchainz/django-cors-headers)
- [mysqlclient 2.2](https://github.com/PyMySQL/mysqlclient)
- [Gunicorn 20.1](https://gunicorn.org/)
- [python-decouple 3.8](https://github.com/HBNetwork/python-decouple)
