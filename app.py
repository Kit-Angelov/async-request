from flask import Flask, request, Response
import asyncio
import queue
import requests
import json

app = Flask(__name__)

q = queue.PriorityQueue()
init = queue.Queue()

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

@app.route('/data/<path:path>')
def send_json(path):
    with open('data/{}'.format(path), 'r') as json_file:
        data = json.load(json_file)
        def generate():
            for item in data:
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
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run())
    
    def generate():
        start = True
        while start:
            signal = init.get()
            print(signal)
            if signal:
                start = False
        print('gen')
        index = 0
        print(q.empty())
        while not q.empty():
            print('start')
            item = q.get(timeout=2)
            print(item)
            if item[0] == index + 1:
                index += 1
                print(item)
                item_dict = {
                    'id': item[0],
                    'name': item[1]
                }
                yield json.dumps(item_dict) + '\n'
            elif item[0] <= index:
                print('pass')
                print(q.get())
            else:
                print(item)
                q.put(item)
    return Response(generate(), mimetype='application/json')

if __name__ == '__main__':
    app.run()