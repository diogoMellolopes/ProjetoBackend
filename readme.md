# Student Core - API RESTful

API para gestão de desempenho acadêmico e envio de redações com autenticação JWT e informações relevantes.

---

## Tecnologias utilizadas:
- Python 3
- Flask
- PostgreSQL
- SQLAlchemy
- Flask-JWT-Extended
- Gunicorn
- Render (Deploy)

---

## Autenticação:

A API utiliza **JWT (JSON Web Token)**
Após login, usar o TOKEN dentro do header

---

## Rotas principais:

### Usuários:
POST  `/users/register`
POST `/users/login`

### Perfil:
PUT `/profiles/update`

### Redações
POST `/essays/user_essay`
GET `/essays/all_essay`
PUT `/essays/rate_essay/<essay_id>`

### Dashboard
GET `/dashboard/stats`

---

## Regras de Negócio:

- Redação deve ter pelo menos **50 caracteres**
- Comparação automática com nota de corte do curso desejado
- Paginação de rankings (10 por página)

--- 

## Deploy:

API publicada em:
https://projetobackend-b5b2.onrender.com

--- 

## Como Rodar Localmente:

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente
venv\Scripts\activate # Windows
source venv/bin/activate # Linux/Mac

# Instalar dependências
pip install -r requirements.txt

# Rodar aplicação
python app/app.py
```

---

## Autor:
Diogo de Mello