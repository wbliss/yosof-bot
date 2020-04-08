import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime as d

load_dotenv()

baseURL = 'https://discordapp.com/api'

r = requests.Session()
r.headers['Authorization'] = 'Bot ' + str(os.getenv('DISC_BOT_KEY'))
response = r.get(baseURL + '/users/@me/guilds')

print(response.text)

jsonResponse = json.loads(response.text)

guildID = jsonResponse[0]['id']

channelResponse = r.get(baseURL + '/guilds/' + str(guildID) + '/channels')

channels = json.loads(channelResponse.text)

for channel in channels:
    if channel['type'] == 0:
        lastMessage = json.loads(r.get(baseURL + '/channels/' + channel['id'] + '/messages/' + channel['last_message_id']).text)
        lastMessageTime = lastMessage['timestamp'].replace('+00:00', '')
        dateWritten = d.strptime(lastMessageTime, '%Y-%m-%dT%H:%M:%S.%f')
        timeDifference = d.utcnow() - dateWritten
        