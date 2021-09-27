source venv/bin/activate

export DB_NAME=envio
export DB_PASS=postgres
export DB_USER=postgres
export DB_HOST=localhost
export DB_PORT=5432
export DJANGO_SETTINGS_MODULE=config.settings

if [[ $1 == "run" ]]; then
    python manage.py runserver 0.0.0.0:8000
fi

if [[ $1 == "install" ]]; then
    pip install -r ./requirements.txt
fi