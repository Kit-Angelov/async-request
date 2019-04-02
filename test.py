import requests
import grequests

def get_data():
    print('start')
    r = requests.get('http://localhost:5000/data/first.json', stream=True)
    print('sending')
    for chunk in r.iter_lines(chunk_size=50, delimiter=b'\n'):
        print('CHUNK')
        yield chunk

for item in get_data():
    print(item)