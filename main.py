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

def get_saved_posts():
    print('Crawling all saved posts...')

    saved_posts = []

    for item in reddit.user.me().saved(limit=None):
        if isinstance(item, praw.models.Submission):
            saved_posts.append(item)
    print('Got all saved posts!')

    return saved_posts

def get_subreddit_list(saved_posts):
    subreddits_list = []

    for item in saved_posts:
        name = item.subreddit
        if not name in subreddits_list:
            subreddits_list.append(name)

    return subreddits_list

def download_posts(saved_posts, subreddit):
    deleted_posts = []

    for post in saved_posts:
        if subreddit in post.permalink:
            link = "https://www.reddit.com" + post.permalink
            print(link)
            DownloadJob(link).run()
            # post.unsave()
            deleted_posts.append(post)

    for post in deleted_posts:
        saved_posts.remove(post)

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