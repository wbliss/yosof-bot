import requests
import json
from datetime import datetime as d

baseURL = 'https://discordapp.com/api'

r = requests.Session()
r.headers['Authorization'] = 'Bot Njk3MTg2MDE4NjY3MDAzOTY0.Xoz6fA.VDA2rD8FrmxHWgu0N5BZwJiStYo'
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
        if timeDifference > 30:
            # PURGE
            continue