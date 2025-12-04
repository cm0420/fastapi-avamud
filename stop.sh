#!/bin/bash
# Script para parar o backend AVAMUD

echo "🛑 Parando Backend AVAMUD..."

pkill -f "uvicorn.*app.main:app"

if [ $? -eq 0 ]; then
    echo "✅ Backend parado com sucesso"
else
    echo "⚠️  Nenhum processo do backend encontrado"
fi

