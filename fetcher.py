import time
from celery import Celery
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)
celery = Celery('fetcher', backend='amqp', broker='amqp://')


@app.route('/create', methods=['POST'])
def add_job():
    url = request.json['url']
    job = url_get.delay(url)
    return jsonify({'key': job.task_id, 'url': url})


@app.route('/job/<key>', methods=['GET'])
def get_job(key):
    job = celery.AsyncResult(key)

    if job.ready():
        status = 'Done'
        results = job.get()
    else:
        status = 'Not Done'
        results = None

    return jsonify({'key': key, 'status': status, 'results': results})


@celery.task
def url_get(url):
    # time.sleep(60)  # Testing Purposes
    r = requests.get(url)
    return r.text


if __name__ == '__main__':
    app.run(debug=True)