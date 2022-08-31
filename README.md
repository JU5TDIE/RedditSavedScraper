# RedditSavedScraper
PRAW based Reddit Media Scraper for saved posts

# Features
- PRAW
- CLI
- Unsaves the posts which you downloaded

# Setup
- Download or Clone the repository
- Download and Replace [ffmpeg.exe](https://www.ffmpeg.org/download.html) to the same directory of the repository
- Install the requirements `pip install -r requirements.txt`
- Fill out the [informations(How to use PRAW)](https://github.com/JU5TDIE/RedditSavedScraper#how-to-use-praw) in `user.json`
- Run `python main.py`

# How to use PRAW
- Visit this url: https://www.reddit.com/prefs/apps/
- Create a new app, name it, select `script`
- `http://localhost:8080` as `redirect url`
- User-agent as `app name`
- Create the app, copy the client key, which is under the app name and the secret key

# Warning
- `Python 3.8` and `ffmpeg` are required for this repository
