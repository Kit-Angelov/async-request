from flask import Flask, request, Response
import grequests
import json
import time

app = Flask(__name__, static_url_path='')

@app.route('/data/<path:path>')
def send_json(path):
    with open('data/{}'.format(path), 'r') as json_file:
        data = json.load(json_file)
        def generate():
            for item in data:
                # time.sleep(0.1)
                yield json.dumps(item) + '\n'
        return Response(generate(), mimetype='application/json')

@app.route('/')
def index():
    sources = [
        'http://localhost:5000/data/third.json',
        'http://localhost:5000/data/first.json',
        'http://localhost:5000/data/second.json'
    ]
    for source in sources:
        responses.append(grequests.get(source))
    return jsonify(result)

if __name__ == '__main__':
    app.run()