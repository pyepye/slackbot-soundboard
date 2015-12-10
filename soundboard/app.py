import os
import subprocess
from urllib2 import unquote

from flask import Flask, jsonify, request
from fuzzywuzzy import process

app = Flask(__name__)
app.config['SECRET_KEY'] = 'changeme'
BASE_PATH = './audio/'


@app.route('/arnie', methods=['POST'])
def soundboard():
    all_data = unquote(request.data)
    all_data = all_data.split('\n')
    data = {}
    for line in all_data:
        key, value = line.split('=', 1)
        data[key] = value

    command = data['command']
    __, sound = command.split('/arnie ')
    files = os.listdir(BASE_PATH)
    filename = process.extract(sound, files, limit=1)
    if filename[0][1] != 0:
        file_path = os.path.join(BASE_PATH, filename[0][0])
        subprocess.call(['afplay', file_path])
        response = {
            'response_type': 'in_channel',
            'text': 'Playing {0}'.format(sound),
        }
    else:
        response = {
            'response_type': 'in_channel',
            'text': 'Could not find {0}'.format(sound),
            'attachments': [{
                    'text': 'Your choices are {0}'.format(', '.join(files))
            }]
        }
    return jsonify(response)


if __name__ == '__main__':
    app.run()
