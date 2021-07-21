import random
import time

import api.spotify
import app.application


register_module = app.application.Module.module
register_api_method = app.application.API.method


@register_module('session')
class Session:
    def start(app):
        pass

    @staticmethod
    def generate_session_id():
        return ''.join([
            random.choice('0123456789abcdef') for i in range(32)
        ])

    @register_api_method()
    def get(app, request):
        session_id = request.data.get('session_id')
        if not session_id:
            return {'status': 0}
        data = [
            row for row in app.db.session.find({'session_id': session_id})
        ]
        if not data:
            return {'status': 0}
        session = data[0]
        user = [row for row in app.db.user.find(
            {'user_id': session.get('user_id')}
        )][0]
        return {
            'status': 1,
            'user': user.get('user')
        }

    @register_api_method()
    def open(app, request):
        code = request.data.get('code')
        if not code:
            return {'status': 0}
        start_time = int(time.time())
        auth_data = api.spotify.Accounts.token(
            authorization=app.authorization, grant_type='authorization_code',
            code=code, redirect_uri=app.client
        )
        access_token = auth_data.get('access_token')
        expires_in = auth_data.get('expires_in')
        if not access_token or not expires_in:
            return {'status': 0}
        session_id = Session.generate_session_id()
        data = api.spotify.API.me(access_token=access_token)
        user_id = data.get('uri')
        image = data.get('images')[0]['url'] if data.get('images') else None
        existing_user = [row for row in app.db.user.find(
            {'user_id': user_id}
        )]
        accounts = []
        status = {
            'broadcasting': False,
            'song': '',
            'reason': 0,
            'tick': 0
        }
        settings = {
            'enabled': True,
            'mode': 1
        }
        if existing_user:
            accounts = existing_user[0]['user']['accounts']
            status = existing_user[0]['status']
            settings = existing_user[0]['user']['settings']
        app.db.user.delete_one({
            'user_id': user_id
        })
        app.db.user.insert_one({
            'user_id': user_id,
            'access_token': {
                'value': access_token,
                'active_until': start_time + expires_in
            },
            'refresh_token': auth_data.get('refresh_token'),
            'user': {
                'accounts': accounts,
                'display_name': data.get('display_name'),
                'image': image,
                'settings': settings
            },
            'status': status
        })
        app.db.session.insert_one({
            'session_id': session_id,
            'user_id': user_id
        })
        return {
            'status': 1,
            'session_id': session_id
        }
