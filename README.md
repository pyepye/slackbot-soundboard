#Slack Soundboard

Play soundbites via slack command

## Install / Run
* Install nodejs
* `npm install -g localtunnel`
* `python soundboard/app.py`
* `lt --port 5000`
* Drop audio files into audio/[command_name]
* Copy the URL provided into a new [Slash Command](https://api.slack.com/slash-commands). The /command must match the folder name within the audio directory
