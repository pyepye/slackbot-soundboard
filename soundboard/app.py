import os
import subprocess

from flask import Flask, jsonify, request
from fuzzywuzzy import process

app = Flask(__name__)
app.config['SECRET_KEY'] = 'changeme'
TOKENS = {
    'arnie': 'changeme',
}


@app.route('/', methods=['POST'])
def soundboard():
    sound = request.form['text']
    command = request.form['command'][1:]
    token = request.form['token']

    if token != TOKENS.get(command):
        response = {
            'response_type': 'in_channel',
            'text': 'Bad config - token did not match',
        }
        return jsonify(response)

    audio_dir = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), '../audio'
    )
    audio_dir = os.path.join(audio_dir, command)
    try:
        files = os.listdir(audio_dir)
    except OSError:
        response = {
            'response_type': 'in_channel',
            'text': 'Bad config - No dir in audio/ with the name {0}'.format(
                command
            ),
        }
        return jsonify(response)

    filename = process.extract(sound, files, limit=1)
    if filename[0][1] != 0:
        file_path = os.path.join(audio_dir, filename[0][0])
        subprocess.call(['afplay', file_path])
        response = {
            'response_type': 'in_channel',
            'text': '{0}'.format(sound),
        }
    else:
        phrase_list = '\',  \''.join(files).replace('.wav', '')
        response = {
            'response_type': 'in_channel',
            'text': 'Could not find \'{0}\'. Your choices are:'.format(sound),
            'attachments': [{
                'text': '\'{0}\''.format(phrase_list)
            }]
        }
    return jsonify(response)


if __name__ == '__main__':
    app.run()
