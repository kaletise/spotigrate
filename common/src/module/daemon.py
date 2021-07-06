import json
import time
import traceback

import api.spotify
import api.vkontakte
import app.application
import utils.utils


register_module = app.application.Module.module
cache = {}


class UserLifeCycle:
    def __init__(self, app, user):
        self.app = app
        self.user = user

        self.status = self.user['status'].copy()
        self.settings = self.user['user']['settings']
        self.tokens = [
            account['access_token'] for account in user['user']['accounts']
        ]

    def check_token(self):
        if self.user['access_token']['active_until'] - 5 < int(time.time()):
            start_time = int(time.time())
            auth_data = api.spotify.Accounts.token(
                authorization=self.app.authorization,
                grant_type='refresh_token',
                refresh_token=self.user['refresh_token']
            )
            self.user['access_token']['value'] = auth_data.get('access_token')
            expires_in = auth_data.get('expires_in')
            if not self.user['access_token']['value'] or not expires_in:
                return self.drop()
            self.user[
                'access_token'
            ]['active_until'] = start_time + expires_in
            self.app.db.user.update_one(
                {'user_id': self.user['user_id']},
                {'$set': {'access_token': self.user['access_token']}}
            )
        return self.user['access_token']['value']

    def drop(self):
        if self.status['broadcasting']:
            self.status['broadcasting'] = False
            for token in self.tokens:
                if self.settings['mode'] == 1:
                    api.vkontakte.Client(token).method('account.setOffline')
                api.vkontakte.Client(token).method('audio.setBroadcast')
        self.update()

    def update(self):
        if self.status != self.user['status']:
            self.app.db.user.update_one(
                {'user_id': self.user['user_id']},
                {'$set': {'status': self.status}}
            )

    def start(self):
        access_token = self.check_token()
        track = api.spotify.API.currently_playing(access_token)
        if not track:
            self.status['song'] = ''
            self.status['reason'] = 0
            return self.drop()
        not_ad = track['currently_playing_type'] != 'ad'
        broadcastable = not_ad and track['is_playing']
        if not broadcastable:
            self.status['song'] = ''
            self.status['reason'] = 0
            return self.drop()
        song = (
            f'{track["item"]["artists"][0]["name"]} - '
            f'{track["item"]["name"]}'
        )
        if not self.settings['enabled']:
            self.status['song'] = song
            self.status['reason'] = 1
            return self.drop()
        if self.settings['mode'] == 2:
            for token in self.tokens.copy():
                online = bool(api.vkontakte.Client(token).method(
                    'users.get', fields='online'
                )['response'][0]['online'])
                if not online:
                    self.tokens.remove(token)
            if not self.tokens:
                self.status['song'] = song
                self.status['reason'] = 2
                return self.drop()
        if self.status['broadcasting'] and self.status['song'] == song:
            if self.settings['mode'] == 1:
                for token in self.tokens:
                    api.vkontakte.Client(token).method('account.setOnline')
            return
        if song in cache and cache[song] == 0:
            self.status['song'] = song
            self.status['reason'] = 3
            return self.drop()
        if song in cache:
            self.status['song'] = song
            self.status['broadcasting'] = True
            if self.tokens:
                self.status['reason'] = 5
            else:
                self.status['reason'] = 4
            for token in self.tokens:
                api.vkontakte.Client(token).method(
                    'audio.setBroadcast', audio=cache[song]
                )
                if self.settings['mode'] == 1:
                    api.vkontakte.Client(token).method('account.setOnline')
            return self.update()
        if not self.tokens:
            self.status['song'] = song
            self.status['reason'] = 4
            return self.drop()
        result = api.vkontakte.Client(self.tokens[0]).method(
            'audio.search', q=song
        )['response']['items']
        if not result:
            self.status['song'] = song
            self.status['reason'] = 3
            cache[song] = 0
            return self.drop()
        song_id = f'{result[0]["owner_id"]}_{result[0]["id"]}'
        cache[song] = song_id
        self.status['song'] = song
        self.status['broadcasting'] = True
        if self.tokens:
            self.status['reason'] = 5
        else:
            self.status['reason'] = 4
        for token in self.tokens:
            api.vkontakte.Client(token).method(
                'audio.setBroadcast', audio=cache[song]
            )
            if self.settings['mode'] == 1:
                api.vkontakte.Client(token).method('account.setOnline')
        return self.update()


@register_module('daemon')
class Daemon:
    @utils.utils.asynchronous
    def start(app):
        while app.running:
            start_time = int(time.time() * 1000)
            for user in app.db.user.find({}):
                # async?
                try:
                    UserLifeCycle(app, user).start()
                except Exception:
                    exc = traceback.format_exc()
                    app.logger.error(
                        'Error during executing daemon: ' + exc
                    )
            time_spend = int(time.time() * 1000) - start_time
            app.logger.debug(f'Full life cycle took {time_spend}ms.')
            if time_spend < 5000:
                time.sleep((5000 - time_spend) / 1000)
