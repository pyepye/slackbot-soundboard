import os
import subprocess

from flask import Flask, jsonify, request
from fuzzywuzzy import process

app = Flask(__name__)
app.config['SECRET_KEY'] = 'changeme'


@app.route('/arnie', methods=['POST'])
def soundboard():
    sound = request.form['text']
    audio_dir = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        '../audio'
    )
    files = os.listdir(audio_dir)
    filename = process.extract(sound, files, limit=1)
    if filename[0][1] != 0:
        file_path = os.path.join(audio_dir, filename[0][0])
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
                    'text': 'Choices are \'{0}\''.format(',   '.join(files))
            }]
        }
    return jsonify(response)


if __name__ == '__main__':
    app.run()
