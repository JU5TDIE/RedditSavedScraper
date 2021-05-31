import sys
import praw
import json
import click
from gallery_dl.job import DownloadJob
from prawcore.exceptions import OAuthException
from prawcore.exceptions import ResponseException

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