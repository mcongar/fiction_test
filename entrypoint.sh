#!/bin/bash

echo "Esperando a que la base de datos esté lista..."

DB_HOST=${DB_HOST:-db}
DB_PORT=${DB_PORT:-3306}

while ! nc -z $DB_HOST $DB_PORT; do
  echo "Esperando a la base de datos..."
  sleep 1
done

echo "Base de datos lista. Aplicando migraciones..."
python manage.py migrate --noinput

echo "Iniciando el servidor Django..."
exec "$@"
