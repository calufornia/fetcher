# fetcher

curl -i -H "Content-Type: application/json" -X POST -d '{"URL":"http://calufornia.github.io"}' http://localhost:5000/create

curl -i http://localhost:5000/job/<key>

PATH=$PATH:/usr/local/sbin
~/.bash_profile

rabbitmq-server
celery worker -A fetcher.celery -n <worker>.%h &
redis-server