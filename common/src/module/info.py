import app.application


register_module = app.application.Module.module
register_api_method = app.application.API.method


@register_module('info')
class Info:
    def start(app):
        pass

    @staticmethod
    def format_link(app):
        return (
            f'https://accounts.spotify.com/authorize'
            f'?client_id={app.config.get("SPOTIFY_APP_ID")}'
            f'&response_type=code'
            f'&redirect_uri={app.client}'
            f'&scope=user-read-currently-playing,user-read-playback-state'
        )

    @register_api_method()
    def getAuthLink(app, request):
        return {
            'status': 1,
            'link': Info.format_link(app)
        }
