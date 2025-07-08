#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Instala todas las dependencias listadas en requirements.txt
pip install -r requirements.txt

# 2. Recolecta todos los archivos estáticos (CSS, JS, etc.) en una sola carpeta
python config/manage.py collectstatic --noinput

# 3. Aplica las migraciones de la base de datos
python config/manage.py migrate
