# Fetcher

Fetcher is a bare bones asynchronous job queue written in Python, implemented using Celery as the task queue, RabbitMQ as the message broker, and Redis as the database. It fetches data from an input url by exposing a REST API. Celery performs an optimization where a job returned from a call to AsyncResult using an invalid key is still given a status of "Pending", so invalid keys will also return a status of "Not Done".

Requirements:

1. Run `git clone https://github.com/calufornia/fetcher.git` in an appropriate directory.

2. Set up a Python virtual environment by first running `pip install virtualenv`, and then `virtualenv -p /usr/bin/python2.7 venv`.

3. Enter the virtual environment by execeuting `source venv/bin/activate`, and run `pip install -r requirements.txt`.

To run the app, execute the following in different terminal tabs:

1. Start a RabbitMQ instance by running `rabbitmq-server`. This may require adding the line `PATH=$PATH:/usr/local/sbin` to `~/.bash_profile`.

2. Start a redis server by running `redis-server`. The application assumes redis is running on port 6379.

3. A new worker can be added by running `celery worker -A fetcher.celery -n <worker>.%h &`, where `<worker>` is the name of the new worker. It is a bit complicated to stop a specific worker process, but `pkill -f "celery worker"` can be used to end all current celery workers.

4. Finally, to start the application, run `python fetcher.py`.

During the execution of the app, two commands can be run:

POST: `curl -i -H "Content-Type: application/json" -X POST -d '{"URL":"<url>"}' http://localhost:5000/create`

This assigns to the job queue the task of fetching data from `<url>`.

GET: `curl -i http://localhost:5000/job/<key>`

This returns the result and/or status of the job associated with job key `<key>` returned from the earlier POST call.
