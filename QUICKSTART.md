# ⚡ Quick Start - Frontend Avamud

## 🔥 Começar em 3 minutos

### Terminal 1: Backend
```bash
cd /home/yago/Área\ de\ trabalho/Avamud/fastapi-avamud

# Ativar venv
source venv/bin/activate

# Rodar backend
uvicorn app.main:app --reload

# Saída esperada:
# INFO:     Application startup complete [Press ENTER to quit]
# INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Terminal 2: Frontend
```bash
cd /home/yago/Área\ de\ trabalho/Avamud/avamud-frontend

# Instalar dependências (primeira vez)
npm install

# Rodar desenvolvimento
npm run dev

# Saída esperada:
# ➜  Local:   http://localhost:5173/
```

### Browser
```
http://localhost:5173
```

---

## 🔐 Testar Login

### Precondições:
- Você precisa ter um usuário no banco de dados
- Se ainda não criou, crie via:
  - FastAPI docs: http://localhost:8000/docs
  - POST /api/v1/users

### Credenciais de Teste:
```
Login:    seu_login_aqui
Senha:    sua_senha_aqui
```

### O que acontece:
1. Submete username + password
2. Backend valida e retorna JWT
3. Frontend armazena em localStorage
4. Redireciona para /users
5. Pronto! 🎉

---

## 📁 Estrutura Rápida

```
src/
├── pages/          ← Páginas (Login, Users, Payments, Addresses)
├── components/     ← Componentes reutilizáveis
├── services/       ← Integração com API
├── context/        ← Autenticação global
└── types/          ← TypeScript types
```

---

## 🎯 Funcionalidades Já Implementadas

| Recurso | Implementado | Link |
|---------|-------------|------|
| Login | ✅ | /login |
| Listar Usuários | ✅ | /users |
| Deletar Usuário | ✅ | Click no botão |
| Listar Pagamentos | ✅ | /payments |
| Deletar Pagamento | ✅ | Click no botão |
| Listar Endereços | ✅ | /addresses |
| Deletar Endereço | ✅ | Click no botão |
| Logout | ✅ | Clique na navbar |

---

## 🔧 Comandos Úteis

```bash
# Dev com hot-reload
npm run dev

# Build para produção
npm run build

# Preview do build
npm run preview

# Lint (verificar código)
npm run lint
```

---

## 📱 Acessar de Outro Computador

Se quiser acessar o frontend de outra máquina:

```bash
# Rodar no frontend
npm run dev -- --host

# Seu IP: 192.168.x.x:5173 (mude para seu IP real)

# No outro computador
# Browser: http://192.168.x.x:5173
```

---

## 🐛 Se der erro...

### "Cannot find module"
```bash
npm install
```

### "CORS error"
Adicione ao backend (app/main.py):
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### "Porta 5173 já está em uso"
```bash
npm run dev -- --port 3000
```

---

## 📊 Monitore as Requisições

Abra a aba **Network** do DevTools (F12):
- Vá para /login
- Digite credenciais
- Procure pela requisição POST `/api/v1/auth/login`
- Veja o token retornado

---

## 🎨 Customizar

### Mudar cores (arquivo: src/pages/LoginPage.module.css)
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
/* Mude os valores hex para outras cores */
```

### Mudar URL da API (arquivo: .env.local)
```
VITE_API_URL=http://outro-servidor:8000/api/v1
```

---

## ✨ Próximas Features

Implemente estes para melhorar:

1. **Formulário de Criar Usuário**
   ```typescript
   // src/pages/CreateUserPage.tsx
   // Form com campos: nome, cpf, email, login, senha, etc
   ```

2. **Formulário de Editar Usuário**
   ```typescript
   // src/pages/EditUserPage.tsx
   ```

3. **Busca/Filtro**
   ```typescript
   // Adicione search input antes da tabela
   ```

4. **Paginação**
   ```typescript
   // Divida resultados em páginas
   ```

---

## 📞 Dúvidas?

1. Leia o README.md
2. Verifique SETUP_FRONTEND.md
3. Olhe os comentários nos arquivos

---

**Você está pronto para começar! 🚀**

```
Frontend:   http://localhost:5173 ✅
Backend:    http://localhost:8000 ✅
Status:     Pronto para desenvolvimento ✅
```
