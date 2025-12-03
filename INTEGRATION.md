Integração Frontend + Backend

Objetivo
- Servir o frontend (SPA) gerado pelo `frontend` externo a partir do backend FastAPI de forma simples e segura.

Abordagem adotada
- O FastAPI agora tenta montar estáticos em runtime procurando (na ordem):
  1. `../frontend/dist` (pasta `frontend/dist` ao lado de `fastapi-avamud`)
  2. `avamud-frontend/dist` (pasta interna do projeto)
- Se encontrar, monta a pasta como `StaticFiles(..., html=True)` em `/`, servindo o SPA na raiz. As rotas da API permanecem em `/api/v1/...`.

Passos para usar localmente
1. Build do frontend externo (repositório raiz `frontend`):

```sh
cd ../frontend
# Instale dependências (Node.js/npm/yarn necessário)
npm install
# Build - gera `dist` (ou `build`) dependendo do setup
npm run build
```

2. Verifique que `../frontend/dist` existe. Em seguida, inicie o backend (na pasta `fastapi-avamud`):

```sh
cd ../fastapi-avamud
# (opcional) configure .env se necessário
/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

3. Acesse `http://127.0.0.1:8000/` — o SPA será servido; as chamadas à API em `/api/v1` continuarão funcionando.

Notas de segurança
- Servir arquivos estáticos a partir do backend é seguro desde que:
  - Você não permita upload de arquivos nessa pasta por usuários não confiáveis.
  - O backend proteja endpoints sensíveis sob `/api/v1` (autenticação/autorização).
- CORS: quando o frontend é servido pela mesma origem (mesmo host/porta) não é preciso configurar CORS para chamadas internas.

Alternativa
- Se preferir, posso copiar o conteúdo de `frontend` para `avamud-frontend` e ajustar `vite.config`/`package.json`, mas isso exige adaptar dependências (JS ↔ TS) e rodar `npm install`/`npm run build` localmente.

Próximo passo
- Se quiser, eu executo a build do `frontend` aqui e valido que `GET /` retorna o `index.html`. Para isso preciso de Node.js/npm disponível neste ambiente. Deseja que eu tente fazer o build aqui (verifico e informo se falta Node)?
