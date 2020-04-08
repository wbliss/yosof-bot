import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import dateparser


class Discord():

    def __init__(self, token):
        self.BASE = 'https://discordapp.com/api'
        self.client = requests.Session()
        self.client.headers['Authorization'] = 'Bot ' + str(token)
        
        
    def _request(self, url):
        response = self.client.get(self.BASE + url)
        if response.status_code != 200:
            print(response.text)
            return # raise error
        return response

    def get_guilds(self):

        return self._request('/users/@me/guilds').json()

    def get_channels(self, guild_id):

        return self._request('/guilds/'+str(guild_id)+'/channels').json()

    def get_messages(self, channel, last_message=False):

        if last_message:
            return self._request('/channels/' + channel['id']+'/messages/'+channel['last_message_id']).json()
        return self._request('/channels/'+str(channel['id'])+'/messages').json()

    def get_channels_to_archive(self, guild_id):

        channels = self.get_channels(guild_id)

        for channel in channels:
            if channel['type'] == 0:
                last_message = self.get_messages(channel, last_message=True)
                last_message_time = dateparser.parse(last_message['timestamp'], settings={'TIMEZONE': 'UTC', 'RETURN_AS_TIMEZONE_AWARE': True})

                if dateparser.parse('now', settings={'TIMEZONE': 'UTC', 'RETURN_AS_TIMEZONE_AWARE': True}) > timedelta(days=30) + last_message_time:
                    print(channel['id'])






if __name__ == '__main__':

    load_dotenv()

    d = Discord(os.getenv('DISC_BOT_TOKEN'))
    print(d.get_channels_to_archive('167448036212080640'))
        