import requests


class Accounts:
    def token(authorization, **kwargs):
        return requests.post(
            'https://accounts.spotify.com/api/token',
            data=kwargs,
            headers={
                'Authorization': authorization
            }
        ).json()


class API:
    def me(access_token):
        return requests.get(
            'https://api.spotify.com/v1/me',
            headers={
                'Authorization': 'Bearer ' + access_token
            }
        ).json()

    def currently_playing(access_token):
        response = requests.get(
            'https://api.spotify.com/v1/me/player/currently-playing',
            headers={
                'Authorization': 'Bearer ' + access_token
            }
        )
        if not response.text:
            return {}
        return response.json()
