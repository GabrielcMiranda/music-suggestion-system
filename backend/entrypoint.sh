#!/bin/bash
set -e

echo "Aguardando banco de dados..."
sleep 5

echo "Inicializando banco de dados..."
python -m app.core.database.init_db

echo "Iniciando aplicação..."
# Usa PORT do ambiente (Render) ou 8000 como padrão (Docker local)
PORT=${PORT:-8000}
exec gunicorn app.main:app --bind 0.0.0.0:$PORT --worker-class uvicorn.workers.UvicornWorker --workers 1
