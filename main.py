import sys
import praw
import json
import click
from gallery_dl import job, config
from prawcore.exceptions import OAuthException
from prawcore.exceptions import ResponseException

def check_auth():
    try:
        if reddit.user.me() is None:
            print('[*] Empty user.json')
            click.pause()
            sys.exit()
        print(f'[*] Logged as {reddit.user.me()}')
    except OAuthException:
        print('[*] Wrong Username and Password.')
        click.pause()
        sys.exit()
    except ResponseException:
        print('[*] Wrong Client ID and Secret')
        click.pause()
        sys.exit()

def get_saved_posts():
    print('[*] Scraping all saved posts...')
    saved_posts = [item for item in reddit.user.me().saved(limit=None) if isinstance(item, praw.models.Submission)]
    print('[*] Got all saved posts!')

    return saved_posts

def get_subreddit_list(saved_posts):
    print('[*] Scraping all subreddits from saved posts...')
    subreddits_list = []

    for item in saved_posts:
        name = item.subreddit
        if not name in subreddits_list:
            subreddits_list.append(name)

    print('[*] Got all subreddits!')
    return subreddits_list

def download_posts(saved_posts, subreddit):
    config.load()
    config.set(("extractor",), "base-directory", f"./{subreddit}/")
    subredditlink = f'/r/{subreddit}/'

    for post in saved_posts:
        if subredditlink in post.permalink:
            link = "https://www.reddit.com" + post.permalink
            print('- ' + link)

            if post.is_self is False:
                postid = post.id
                if hasattr(post, 'crosspost_parent'):
                    postid = post.crosspost_parent.split("_")[1]
                    r = reddit.submission(id=postid)
                    link = "https://www.reddit.com" + r.permalink
                    print(f'[*] Crossposted! ({link})')
                print('[*] Downloading ' + link)
                job.DownloadJob(link).run()
                post.unsave()
                saved_posts.remove(post)
                    
            elif post.is_self is True:
                print('[*] No images or videos in the post')

            print('\n')

def main():
    check_auth()
    saved_posts = get_saved_posts()

    while True:
        cmd = input('choose the subreddit : ')

        if cmd == '!subreddits':
            subreddit_list = get_subreddit_list(saved_posts)

            print('────────────────────────────────────────────')
            for item in subreddit_list:
                print(item)
            print(f'Total {len(subreddit_list)} subreddits')
            print('────────────────────────────────────────────')

        elif cmd == '!posts':
            print('────────────────────────────────────────────')
            for item in saved_posts:
                print(item.permalink)
            print(f'Total {len(saved_posts)} posts')
            print('────────────────────────────────────────────')
        
        elif cmd == '!all':
            subreddit_list = get_subreddit_list(saved_posts)
            for subreddit in subreddit_list:
                print('────────────────────────────────────────────')
                print(subreddit)
                print('────────────────────────────────────────────')
                download_posts(saved_posts, str(subreddit))

        elif cmd == '!clear':
            click.clear()

        elif cmd == '!exit':
            click.pause() 
            sys.exit()

        elif cmd == '!help':
            print('''
────────────────────────────────────────────
You can download the contents by subreddit
If you want to download more than two subreddits in the same time,
put "+" between subreddits. (Python+learnpython+learnprogramming)

Commands :')
!subreddits : View the subreddits of saved posts
!posts      : View the saved posts link
!clear      : Clear the console screen
!all        : Download all saved posts
!exit       : Exit
────────────────────────────────────────────''')

        else: 
            s = cmd.split('+')

            for subreddit in s:
                subreddit_list = get_subreddit_list(saved_posts)

                if subreddit in subreddit_list:
                    print('────────────────────────────────────────────')
                    print(subreddit)
                    print('────────────────────────────────────────────')
                    download_posts(saved_posts, subreddit)
                else:
                    print('────────────────────────────────────────────')
                    print(subreddit, 'is not in the list. Choose again. ')
                    print('!help to view the commands')
                    print('────────────────────────────────────────────')

if __name__ == '__main__':
    try:
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
        
    except FileNotFoundError as e:
        print(e)
        click.pause()