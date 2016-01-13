import os, sys
import spotipy
import spotipy.util as util
from flask import Flask
from flask_slack import Slack
from urlparse import urlparse

app = Flask(__name__)

slack = Slack(app)
app.add_url_rule('/', view_func=slack.dispatch)


client_id = os.getenv('SPOTIPY_CLIENT_ID')
client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
redirect_url = os.getenv('SPOTIPY_REDIRECT_URI')
slack_token = os.getenv('SLACK_TOKEN')
slack_team_id = os.getenv('SLACK_TEAM_ID')
spotify_user = os.getenv('SPOTIFY_USER')
spotify_playlist = os.getenv('SPOTIFY_PLAYLIST')


@slack.command('jam', token=slack_token, team_id=slack_team_id, methods=['POST'])
def grab_track(**kwargs):
    text = kwargs.get('text')
    check_url = urlparse(text)
    track_id = check_url.path.split('/')[2]
    if check_url.netloc == 'open.spotify.com':
        scope = 'playlist-modify-public'
        token = util.prompt_for_user_token('mitchheard', scope, client_id, client_secret, redirect_url)

        if token:
            sp = spotipy.Spotify(auth=token)
            sp.trace = False
            sp.user_playlist_add_tracks(spotify_user, spotify_playlist, [track_id])
            return slack.response("Adding your song to the playlist " + text)
        else:
            return slack.response("something went wrong")
    else:
        return slack.response("Please use a valid spotify url (ex: https://open.spotify.com/track/7iABnSNZciNepqGtjMQxxd)")

@app.route('/callback')
def callback():
    return "test"
