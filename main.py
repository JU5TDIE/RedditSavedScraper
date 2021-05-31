import sys
import praw
import json
import click
from gallery_dl.job import DownloadJob
from prawcore.exceptions import OAuthException
from prawcore.exceptions import ResponseException

def check_auth():
    try:
        print('Logined as %s' % reddit.user.me())
    except OAuthException:
        print('Wrong Username and Password.')
        click.pause()
        sys.exit()
    except ResponseException:
        print('Wrong Client ID and Secret')
        click.pause()
        sys.exit()

if __name__ == '__main__':
    with open('user.json') as f:
        data = json.load(f)

    reddit = praw.Reddit(
        client_id=data['client_id'],
        client_secret=data['client_secret'],
        user_agent=data['user_agent'],
        username=data['username'],
        password=data['password']
    )