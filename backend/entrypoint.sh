#!/bin/bash
set -e

echo "Aguardando banco de dados..."
sleep 5

echo "Inicializando banco de dados..."
python -m app.core.database.init_db

echo "Iniciando aplicação..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
