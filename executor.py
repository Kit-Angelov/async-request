import asyncio
import queue
import requests
import json

q = queue.PriorityQueue()
init = queue.Queue()

sources = [
        {
            'init': False,
            'url': 'http://localhost:5000/data/third.json',
        },
        {
            'init': True,
            'url': 'http://localhost:5000/data/first.json',
        },
        {
            'init': False,
            'url': 'http://localhost:5000/data/second.json',
        }
]

def producer(source):
    r = requests.get(source['url'], stream=True, timeout=2)
    if source['init']:
        init.put('start')
    for chunk in r.iter_lines(chunk_size=20, delimiter=b'\n'):
        if chunk:
            chunk_dict = json.loads(chunk)
            q.put((chunk_dict['id'], chunk_dict['name']))


async def run():
    stopping = True
    loop = asyncio.get_event_loop()
    for source in sources:
        loop.run_in_executor(None, producer, source)
    while True:
        signal = init.get()
        if signal:
            print(signal)
            break
    while True:
        print('234')
        print(q.get())

loop = asyncio.get_event_loop()
loop.run_until_complete(run())