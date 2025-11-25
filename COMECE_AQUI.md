# 🎯 Próximas Ações - Para Você

Aqui está exatamente o que você precisa fazer agora:

---

## ⚡ PASSO 1: Instalar Node.js (Crítico!)

### Por que?
O projeto precisa de Node.js para funcionar. Você recebeu erro que npm não está instalado.

### Como fazer?

#### Opção A: Ubuntu/Debian (Mais fácil)
```bash
# Abra um terminal e execute:
sudo apt update
sudo apt install -y nodejs npm

# Verifique:
node --version  # Deve mostrar v16+
npm --version   # Deve mostrar 8+
```

#### Opção B: Fedora/CentOS
```bash
sudo dnf install -y nodejs npm
```

#### Opção C: Arch Linux
```bash
sudo pacman -S nodejs npm
```

#### Opção D: macOS (Homebrew)
```bash
brew install node
```

#### Opção E: Windows
- Baixe em: https://nodejs.org/
- Escolha versão LTS
- Execute o instalador

---

## ⚡ PASSO 2: Verificar Instalação

```bash
node --version
npm --version

# Saída esperada:
# v18.x.x ou v20.x.x
# 9.x.x ou 10.x.x
```

---

## ⚡ PASSO 3: Instalar Dependências do Frontend

```bash
# Navegue para o projeto
cd "/home/yago/Área de trabalho/Avamud/avamud-frontend"

# Instale as dependências
npm install

# Vai criar pasta node_modules/ (pode levar 1-2 minutos)
# Vai criar package-lock.json
```

---

## ⚡ PASSO 4: Verificar Backend

O backend deve estar **rodando** antes de iniciar o frontend.

```bash
# Em um terminal diferente:
cd "/home/yago/Área de trabalho/Avamud/fastapi-avamud"

# Ativar venv
source venv/bin/activate

# Instalar dependências (se não fez)
pip install -r requirements.txt

# Rodar backend
uvicorn app.main:app --reload

# Saída esperada:
# INFO:     Application startup complete [Press ENTER to quit]
# INFO:     Uvicorn running on http://127.0.0.1:8000
```

⚠️ **IMPORTANTE**: Deixe este terminal aberto!

---

## ⚡ PASSO 5: Rodar Frontend

Em **outro terminal**:

```bash
# Navegue para o frontend
cd "/home/yago/Área de trabalho/Avamud/avamud-frontend"

# Inicie o servidor de desenvolvimento
npm run dev

# Saída esperada:
# ➜  Local:   http://localhost:5173/
# ➜  press h to show help
```

⚠️ **IMPORTANTE**: Deixe este terminal também aberto!

---

## ⚡ PASSO 6: Acessar a Aplicação

1. Abra seu **navegador** (Chrome, Firefox, Safari, etc)
2. Vá para: **http://localhost:5173**
3. Você verá a página de login ✅

---

## 🔐 PASSO 7: Fazer Login

### Precondição: Criar um usuário de teste

Se ainda não criou, acesse: **http://localhost:8000/docs**

1. Procure pela seção `/users` (POST)
2. Clique em "Try it out"
3. Preencha com dados de teste:
```json
{
  "nome": "Teste User",
  "cpf": "12345678901",
  "cnpj": "12345678000190",
  "email": "teste@email.com",
  "login": "testuser",
  "telefone": "11999999999",
  "senha": "123456"
}
```
4. Execute
5. Copie o ID retornado

### Fazer login no frontend

Agora vá para http://localhost:5173 e:
1. **Login**: `testuser`
2. **Senha**: `123456`
3. Clique em "Entrar"

---

## ✅ Checklist de Verificação

```
[ ] Node.js instalado (node --version)
[ ] npm instalado (npm --version)
[ ] Backend rodando em http://localhost:8000
[ ] Frontend rodando em http://localhost:5173
[ ] Consegue acessar http://localhost:5173 no navegador
[ ] Backend tem CORS configurado (veja abaixo)
[ ] Consegue fazer login
[ ] Vê página de usuários após login
```

---

## 🐛 Se der erro de CORS

O backend precisa ter CORS configurado. Adicione em `app/main.py`:

```python
# No começo do arquivo, após imports
from fastapi.middleware.cors import CORSMiddleware

# Após criar o app (depois de app = FastAPI(...))
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Salve o arquivo. O servidor FastAPI vai recarregar automaticamente.

---

## 🎯 Você Terá Uma Tela Assim

### Após Login
```
┌────────────────────────────────────────┐
│        Avamud                 Logout   │
│                                        │
│  Usuários  Pagamentos  Endereços      │
├────────────────────────────────────────┤
│                                        │
│  ID  Nome          Email      Ações   │
│  ─────────────────────────────────────  │
│  1   Teste User    teste@... Editar D │
│  2   Outro User    outro@... Editar D │
│                                        │
│ + Novo Usuário                        │
└────────────────────────────────────────┘
```

---

## 📱 Estrutura de Terminais

Você vai ter **3 terminais abertos**:

```
Terminal 1: Backend (FastAPI)
$ cd fastapi-avamud && source venv/bin/activate && uvicorn app.main:app --reload
→ Rodando em http://localhost:8000

Terminal 2: Frontend (Vite + React)
$ cd avamud-frontend && npm run dev
→ Rodando em http://localhost:5173

Terminal 3: Browser
→ Abra http://localhost:5173
```

---

## 💡 Dicas

- ✅ Use Chrome DevTools (F12) para debugar
- ✅ Verifique a aba "Network" para ver requisições
- ✅ Verifique a aba "Console" para erros
- ✅ O token JWT é armazenado em localStorage (aba "Application")

---

## 📚 Documentação Disponível

Leia nesta ordem:

1. **QUICKSTART.md** ← Comece aqui (3 minutos)
2. **SETUP_FRONTEND.md** ← Se tiver dúvidas de instalação
3. **README.md** (em avamud-frontend/) ← Referência completa
4. **FRONTEND_CRIADO.md** ← Entender arquitetura

---

## 🎓 Se Quiser Entender Melhor

### Fluxo de Login
```
1. User digita login/senha
2. Frontend envia POST /auth/login
3. Backend valida e retorna JWT
4. Frontend armazena token
5. Frontend redireciona para /users
```

### Fluxo de Requisição Autenticada
```
1. User acessa /users
2. ProtectedRoute verifica se tem token
3. Se sim, carrega dados
4. axios.get('/users') é executado
5. Interceptor adiciona header Authorization
6. Backend valida JWT
7. Backend retorna usuários
8. Frontend exibe tabela
```

---

## ✨ Depois que Estiver Funcionando

Você pode:
- ✅ Criar novos usuários via formulário
- ✅ Editar usuários
- ✅ Deletar usuários
- ✅ Mesmo para pagamentos e endereços
- ✅ Modificar UI/UX
- ✅ Adicionar validações
- ✅ Melhorar design
- ✅ Deploy em produção

---

## 🆘 Encontrou um erro?

**Mensagem**: `npm: comando não encontrado`
**Solução**: Instale Node.js (veja PASSO 1)

**Mensagem**: `Cannot find module`
**Solução**: `npm install`

**Mensagem**: `CORS error`
**Solução**: Adicione CORS no backend (veja acima)

**Mensagem**: `POST http://localhost:8000/... 401`
**Solução**: Token expirou, faça login novamente

**Mensagem**: `Porta 5173 já em uso`
**Solução**: `npm run dev -- --port 3000`

---

## 🚀 Resumo em Poucas Linhas

```bash
# Terminal 1: Backend
cd ~/Área\ de\ trabalho/Avamud/fastapi-avamud
source venv/bin/activate
uvicorn app.main:app --reload

# Terminal 2: Frontend
cd ~/Área\ de\ trabalho/Avamud/avamud-frontend
npm install  # Primeira vez
npm run dev

# Browser
http://localhost:5173
```

---

**Bora começar! 🚀**

Se precisar de ajuda, consulte os documentos ou me pergunte!
