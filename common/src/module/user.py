import json
import random
import time

import api.spotify
import api.vkontakte
import app.application


register_module = app.application.Module.module
register_api_method = app.application.API.method


@register_module('user')
class User:
    def start(app):
        pass

    @register_api_method()
    def addAccount(app, request):
        session_id = request.data.get('session_id')
        access_token = request.data.get('access_token')
        if not access_token or not session_id:
            return {'status': 0}
        data = [
            row for row in app.db.session.find({'session_id': session_id})
        ]
        if not data:
            return {'status': 0}
        session = data[0]
        user_id = session.get('user_id')
        response = api.vkontakte.Client(access_token).method(
            'users.get', fields='photo_50'
        ).get('response')
        if not response:
            return {'status': 0}
        user = [row for row in app.db.user.find(
            {'user_id': session.get('user_id')}
        )][0]
        if len(user['user']['accounts']) > 5:
            return {'status': 0}
        for account in user['user']['accounts']:
            if account['user_id'] == response[0].get('id'):
                return {'status': 0}
        account = {
            'user_id': response[0].get('id'),
            'first_name': response[0].get('first_name'),
            'last_name': response[0].get('last_name'),
            'photo': response[0].get('photo_50'),
            'access_token': access_token
        }
        app.db.user.update_one(
            {'user_id': user_id}, {'$push': {'user.accounts': account}}
        )
        return {
            'status': 1,
            'user': account
        }

    @register_api_method()
    def updateSettings(app, request):
        session_id = request.data.get('session_id')
        settings = request.data.get('settings')
        if not settings or not session_id:
            return {'status': 0}
        data = [
            row for row in app.db.session.find({'session_id': session_id})
        ]
        if not data:
            return {'status': 0}
        session = data[0]
        user_id = session.get('user_id')
        app.db.user.update_one(
            {'user_id': user_id},
            {'$set': {'user.settings': json.loads(settings)}}
        )
        return {'status': 1}

    @register_api_method()
    def getStatus(app, request):
        session_id = request.data.get('session_id')
        if not session_id:
            return {'status': 0}
        data = [
            row for row in app.db.session.find({'session_id': session_id})
        ]
        if not data:
            return {'status': 0}
        session = data[0]
        user_id = session.get('user_id')
        status = [
            row for row in app.db.user.find({'user_id': user_id})
        ][0]['status']
        return {'status': 1, 'data': status}

    @register_api_method()
    def removeAccount(app, request):
        session_id = request.data.get('session_id')
        uid = request.data.get('user_id')
        if not uid or not session_id:
            return {'status': 0}
        data = [
            row for row in app.db.session.find({'session_id': session_id})
        ]
        if not data:
            return {'status': 0}
        session = data[0]
        user_id = session.get('user_id')
        app.db.user.update_one(
            {'user_id': user_id},
            {'$pull': {'user.accounts': {'user_id': int(uid)}}}
        )
        return {'status': 1}
