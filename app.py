from flask import Flask, request, Response
import asyncio
import queue
import requests
import json

app = Flask(__name__, static_url_path='')

q = queue.PriorityQueue()
init = queue.Queue()


@app.route('/data/<path:path>')
def send_json(path):
    with open('data/{}'.format(path), 'r') as json_file:
        data = json.load(json_file)
        def generate():
            for item in data:
                # time.sleep(0.1)
                yield json.dumps(item) + '\n'
        return Response(generate(), mimetype='application/json')


def producer(source):
    r = requests.get(source['url'], stream=True, timeout=2)
    if r.status_code != 200:
        return
    
    sended_start = False
    for chunk in r.iter_lines(chunk_size=20, delimiter=b'\n'):
        if chunk:
            chunk_dict = json.loads(chunk)
            q.put((chunk_dict['id'], chunk_dict['name']))
            if source.get('init') and not sended_start:
                init.put('start')
                sended_start = True


async def run():
    loop = asyncio.get_event_loop()
    for source in sources:
        loop.run_in_executor(None, producer, source)


@app.route('/')
def index():
    sources = [
        {
            'url': 'http://localhost:5000/data/third.json',
        },
        {   
            'init': True,
            'url': 'http://localhost:5000/data/first.json',
        },
        {
            'url': 'http://localhost:5000/data/second.json',
        }
    ]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
    start = True
    while start:
        signal = init.get()
        print(signal)
        if signal:
            start = False
    
    def generate():
            while True:
                print(q.get())
                yield json.dumps(item) + '\n'
    return jsonify(result)

if __name__ == '__main__':
    app.run()