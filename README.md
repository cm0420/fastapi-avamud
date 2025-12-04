# AVAMUD Backend API

Sistema de gerenciamento para Associação de Vendedores Ambulantes de Diamantina.

## 🚀 Quick Start

```bash
# Iniciar backend
./start.sh

# Ou manualmente:
python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8080 --reload
```

## 📚 Documentação

- **STATUS_BACKEND.md** - Status completo e funcionalidades
- **RELATORIO_INTEGRACAO.md** - Relatório de integração frontend/backend
- **QUICKSTART.md** - Guia rápido de instalação
- **INTEGRATION.md** - Instruções de integração

## 🌐 Endpoints

- **API Docs**: http://127.0.0.1:8080/docs
- **ReDoc**: http://127.0.0.1:8080/redoc
- **Frontend**: http://127.0.0.1:8080/

## 🔑 Credenciais de Teste

| Login | Senha | Role |
|-------|-------|------|
| admin | admin123 | ADMIN |
| tesoureiro | tesoureiro123 | TREASURER |
| membro | membro123 | MEMBER |

## 🛠️ Tecnologias

- FastAPI 0.122.0
- SQLModel 0.0.27
- Uvicorn 0.38.0
- JWT Authentication
- SQLite Database

## 📦 Instalação

```bash
pip install -r requirements.txt
```

## ⚙️ Configuração

Edite `.env`:
```env
DATABASE_URL=sqlite:///./avamud_dev.db
JWT_SECRET_KEY=dev-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

## 📖 Leia Mais

Consulte `STATUS_BACKEND.md` para documentação completa.

---

**Status**: ✅ Finalizado e operacional  
**Branch**: branch-yago-1
