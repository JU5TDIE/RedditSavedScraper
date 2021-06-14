import sys
import praw
import json
import click
from gallery_dl import job, config
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
    config.load()
    config.set(("extractor",), "base-directory", "./%s/" % subreddit)
    
    deleted_posts = []
    
    subreddit = '/r/%s/' % subreddit
    for post in saved_posts:
        if subreddit in post.permalink:
            link = "https://www.reddit.com" + post.permalink
            print(link)
            if not post.is_self:
                job.DownloadJob(link).run()
                post.unsave()
                deleted_posts.append(post)
            else:
                print('no images or videos')

    for post in deleted_posts:
        saved_posts.remove(post)

def main():
    check_auth()
    saved_posts = get_saved_posts()

    while True:
        cmd = input('choose the subreddit : ')

        if cmd == '!subreddits':
            subreddit_list = get_subreddit_list(saved_posts)

            print('--------------------------------------------')
            for item in subreddit_list:
                print(item)
            print('Total %s subreddits' % len(subreddit_list))
            print('--------------------------------------------')

        elif cmd == '!posts':
            print('--------------------------------------------')
            for item in saved_posts:
                print(item.permalink)
            print('Total %s posts' % len(saved_posts))
            print('--------------------------------------------')

        elif cmd == '!clear':
            click.clear()

        elif cmd == '!exit':
            click.pause() 
            sys.exit()

        elif cmd == '!help':
            print('--------------------------------------------')
            print('You can download the contents by selecting subreddit')
            print('If you wanna download more than two subreddits in same time,')
            print('put "+" between subreddits. (Python+learnpython+learnprogramming)')
            print('')
            print('Commands :')
            print('!subreddits : View the subreddits of saved posts')
            print('!posts      : View the saved posts link')
            print('!clear      : Clear the console screen')
            print('!exit       : Exit')
            print('--------------------------------------------')

        else: 
            s = cmd.split('+')

            for subreddit in s:
                subreddit_list = get_subreddit_list(saved_posts)

                if subreddit in subreddit_list:
                    print('--------------------------------------------')
                    print(subreddit)
                    print('--------------------------------------------')
                    download_posts(saved_posts, subreddit)
                else:
                    print('--------------------------------------------')
                    print(subreddit, 'is not in the list. Choose again. ')
                    print('!help to view the commands')
                    print('--------------------------------------------')

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

    main()