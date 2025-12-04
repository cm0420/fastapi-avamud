#!/bin/bash
# Script de inicialização do backend AVAMUD

echo "🚀 Iniciando Backend AVAMUD..."
echo ""

# Verificar se porta 8080 está em uso
if lsof -i :8080 > /dev/null 2>&1; then
    echo "⚠️  Porta 8080 já está em uso. Matando processo..."
    pkill -f "uvicorn.*app.main:app"
    sleep 1
fi

# Ativar ambiente virtual se existir
if [ -d ".venv" ]; then
    echo "🔧 Ativando ambiente virtual..."
    source .venv/bin/activate
fi

# Iniciar uvicorn
echo "✅ Iniciando servidor na porta 8080..."
python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8080 --reload

