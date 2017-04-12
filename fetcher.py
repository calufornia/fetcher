import time
from celery import Celery
import requests
import redis
from flask import Flask, jsonify, request

app = Flask(__name__)
r = redis.StrictRedis(host='localhost', port=6379, db=0)
celery = Celery('fetcher', backend='amqp', broker='amqp://')


@app.route('/create', methods=['POST'])
def add_job():
    url = request.json['url']
    job = url_get.delay(url)
    return jsonify({'key': job.task_id, 'url': url})


@app.route('/job/<key>', methods=['GET'])
def get_job(key):
    job = celery.AsyncResult(key)

    if job is None:
        status = 'Not a valid key'
    elif job.ready():
        status = 'Done'
        results = job.get()
        if r.get(key) is None:
            r.set(key, results)
    else:
        status = 'Not Done'

    return jsonify({'key': key, 'status': status, 'results': r.get(key)})


@celery.task
def url_get(url):
    # time.sleep(60)  # Testing Purposes
    results = requests.get(url)
    return results.text


if __name__ == '__main__':
    app.run(debug=True)