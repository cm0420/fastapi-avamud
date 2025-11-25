# Guia de Instalação - Node.js e Frontend Avamud

## 🖥️ Instalando Node.js

### Linux (Ubuntu/Debian)

```bash
# Atualizar o gerenciador de pacotes
sudo apt update
sudo apt upgrade -y

# Instalar Node.js e npm
sudo apt install -y nodejs npm

# Verificar instalação
node --version
npm --version
```

### Linux (Fedora/CentOS)

```bash
# Atualizar
sudo dnf install -y nodejs npm

# Verificar
node --version
npm --version
```

### Linux (Arch)

```bash
sudo pacman -S nodejs npm
```

### macOS (Homebrew)

```bash
# Se não tiver Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instalar Node.js
brew install node

# Verificar
node --version
npm --version
```

### Windows

1. Baixe de https://nodejs.org/
2. Escolha a versão LTS (recomendado)
3. Siga o instalador
4. Verifique no PowerShell:
   ```
   node --version
   npm --version
   ```

---

## 🚀 Rodando o Frontend

### 1. Navegar até a pasta do projeto

```bash
cd "/home/yago/Área de trabalho/Avamud/avamud-frontend"
```

### 2. Instalar dependências

```bash
npm install
```

Isso irá:
- Baixar React, Vite, TypeScript e outras dependências
- Criar a pasta `node_modules/`
- Gerar `package-lock.json`

### 3. Certificar-se que o backend está rodando

O backend (FastAPI) deve estar rodando em `http://localhost:8000`:

```bash
# Em outro terminal, na pasta do backend
cd "/home/yago/Área de trabalho/Avamud/fastapi-avamud"

# Ativar virtual environment
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt

# Rodar backend
uvicorn app.main:app --reload
```

### 4. Rodar o servidor de desenvolvimento

```bash
npm run dev
```

Você verá algo como:

```
  VITE v5.0.8  ready in 234 ms

  ➜  Local:   http://localhost:5173/
  ➜  press h to show help
```

### 5. Acessar a aplicação

- Abra http://localhost:5173 no navegador
- Use as credenciais criadas no backend para fazer login
- Pronto! 🎉

---

## 📦 Scripts Disponíveis

```bash
# Desenvolvimento (com hot reload)
npm run dev

# Build para produção
npm run build

# Preview do build
npm run preview

# Lint (verificar código)
npm run lint
```

---

## 🔧 Troubleshooting

### Erro: "npm: comando não encontrado"

Node.js não está instalado ou não está no PATH. Reinstale usando os passos acima.

### Erro: CORS quando tenta fazer login

Certifique-se de que o backend tem CORS configurado. No `app/main.py`:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Erro: "Cannot find module"

Execute `npm install` novamente:

```bash
rm -rf node_modules package-lock.json
npm install
```

### Porta 5173 já está em uso

Use outra porta:

```bash
npm run dev -- --port 3000
```

---

## 🎯 Estrutura Mínima de Trabalho

Para ter tudo funcionando:

```
Terminal 1: Backend
$ cd fastapi-avamud
$ source venv/bin/activate
$ uvicorn app.main:app --reload

Terminal 2: Frontend
$ cd avamud-frontend
$ npm run dev

Browser: http://localhost:5173
```

---

## 📚 Links Úteis

- [Node.js Docs](https://nodejs.org/docs/)
- [npm Docs](https://docs.npmjs.com/)
- [Vite Docs](https://vitejs.dev/)
- [React Docs](https://react.dev/)
- [TypeScript Docs](https://www.typescriptlang.org/docs/)

---

Qualquer dúvida, chame! 🚀
