import queue
import asyncio
import requests
import threading
import time

q = queue.Queue()
loop = asyncio.get_event_loop()
# q.put('1')
# print(q.get())
sources = [
        'http://localhost:5000/data/third.json',
        'http://localhost:5000/data/first.json',
        'http://localhost:5000/data/second.json'
    ]

def func1():
    r = requests.get(sources[1], stream=True)
    print('sending')
    for chunk in r.iter_lines(chunk_size=50, delimiter=b'\n'):
        q.put(chunk)

def func2():
    r = requests.get(sources[2], stream=True)
    print('sending')
    for chunk in r.iter_lines(chunk_size=50, delimiter=b'\n'):
        q.put(chunk)

# async def get_data():
#     loop = asyncio.get_event_loop()
#     def req(source):
#         r = requests.get(source, stream=True)
#         print('sending')
#         for chunk in r.iter_lines(chunk_size=50, delimiter=b'\n'):
#             q.put('2')
#     for source in sources:
#         await loop.run_in_executor(None, req, source)

# loop.run_until_complete(get_data())

threading.Thread(target=func1).start()
threading.Thread(target=func2).start()

while True:
    print(q.get())