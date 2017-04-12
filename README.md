# fetcher

curl -i -H "Content-Type: application/json" -X POST -d '{"url":"http://calufornia.github.io"}' http://localhost:5000/create

curl http://localhost:5000/job/


rabbitmq-server
celery worker -A fetcher.celery &
redis-server
