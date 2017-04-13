from celery import Celery
from flask import Flask, jsonify, request
import requests
import redis
import pickle
import time

app = Flask(__name__)
r = redis.StrictRedis(host='localhost', port=6379, db=0)
celery = Celery('fetcher', backend='amqp', broker='amqp://')


@app.route('/create', methods=['POST'])
def add_job():
    url = request.json['URL']
    job = url_get.delay(url)
    
    return jsonify({'url': url,
                    'key': job.task_id})


@app.route('/job/<key>', methods=['GET'])
def get_job(key):
    job = celery.AsyncResult(key) # Returns job associated with input key, None if no associated job
    url = None
    results = None

    if job.ready():
        status = 'Done'

        if r.get(key) is None: # Performs database insertion on-demand
            url, results = job.get()
            r.set(key, pickle.dumps((url, results)))
        else:
            url, results = pickle.loads(r.get(key))
    else:
        status = 'Not Done'

    return jsonify({'key': key,
                    'status': status,
                    'url': url,
                    'results': results})


@celery.task
def url_get(url):
    # time.sleep(60)  # Testing Purposes
    results = requests.get(url)
    return url, results.text


if __name__ == '__main__':
    app.run(debug=True)