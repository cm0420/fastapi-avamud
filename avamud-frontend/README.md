# Avamud Frontend

Sistema de frontend para o Avamud - aplicação de gerenciamento de pagamentos.

## 🚀 Tecnologias

- **React 18** - Biblioteca UI
- **TypeScript** - Type safety
- **Vite** - Build tool e dev server
- **React Router** - Roteamento
- **Axios** - Cliente HTTP
- **Context API** - Gerenciamento de estado (autenticação)

## 📋 Pré-requisitos

- Node.js 16+ (LTS)
- npm ou yarn

## 🔧 Setup Inicial

### 1. Instalar dependências

```bash
cd avamud-frontend
npm install
```

### 2. Configurar variáveis de ambiente

Crie/edite o arquivo `.env.local`:

```bash
VITE_API_URL=http://localhost:8000/api/v1
```

### 3. Iniciar o servidor de desenvolvimento

```bash
npm run dev
```

A aplicação estará disponível em `http://localhost:5173`

## 📁 Estrutura do Projeto

```
src/
├── components/          # Componentes reutilizáveis
│   ├── Layout.tsx
│   ├── ProtectedRoute.tsx
│   └── LoadingSpinner.tsx
├── pages/               # Páginas da aplicação
│   ├── LoginPage.tsx
│   ├── UsersPage.tsx
│   ├── PaymentsPage.tsx
│   └── AddressesPage.tsx
├── services/            # Integração com API
│   ├── api.ts           # Configuração Axios
│   ├── authService.ts
│   ├── userService.ts
│   ├── paymentService.ts
│   └── addressService.ts
├── context/             # Context API
│   └── AuthContext.tsx
├── types/               # TypeScript types
│   ├── user.ts
│   ├── payment.ts
│   ├── address.ts
│   └── auth.ts
├── hooks/               # Custom hooks
│   ├── useAuth.ts
│   └── useFetch.ts
├── App.tsx              # Componente principal
├── main.tsx             # Entry point
└── index.css            # Estilos globais
```

## 🔐 Fluxo de Autenticação

1. Usuário acessa `/login`
2. Submete credenciais (username + password)
3. Backend retorna JWT token
4. Token é armazenado em `localStorage`
5. Intercepador axios adiciona token em todas as requisições
6. Se token expirar (401), usuário é redirecionado para login

## 🛣️ Rotas Disponíveis

- `/login` - Página de login (pública)
- `/users` - Gerenciamento de usuários (protegida)
- `/payments` - Gerenciamento de pagamentos (protegida)
- `/addresses` - Gerenciamento de endereços (protegida)
- `/` - Redireciona para `/users`

## 🔌 Comunicação com Backend

### Exemplo: Listar usuários

```typescript
import { userService } from './services/userService';

const users = await userService.getAll();
```

### Exemplo: Fazer login

```typescript
import { authService } from './services/authService';

const token = await authService.login('username', 'password');
```

## 🏗️ Build para Produção

```bash
npm run build
```

Os arquivos compilados estarão em `dist/`

## 🐛 Troubleshooting

### CORS Error
Certifique-se de que o backend possui CORS configurado:

```python
# app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Token não persistindo
O token é armazenado em `localStorage`. Se não está persistindo, verifique:
- Se o navegador permite localStorage
- Se há erro de CORS prevenindo a requisição de login

### Rodas protegidas não funcionando
Certifique-se de que o `AuthProvider` está envolvendo todo o app em `App.tsx`

## 📝 Próximos Passos

- [ ] Implementar forms de criação/edição de usuários
- [ ] Implementar forms de criação/edição de pagamentos
- [ ] Implementar forms de criação/edição de endereços
- [ ] Adicionar paginação nas tabelas
- [ ] Adicionar filtros/busca
- [ ] Adicionar validação de formulários com Zod
- [ ] Adicionar notificações (toast)
- [ ] Melhorar UI com Tailwind CSS ou Material-UI
- [ ] Implementar testes unitários
- [ ] Adicionar PWA (Progressive Web App)

## 📞 Suporte

Para dúvidas ou problemas, consulte a documentação do projeto principal.
