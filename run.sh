docker run -p 6379:6379 --name REDIS -d redis
celery -A app.celery worker --loglevel=info
python -m app 

