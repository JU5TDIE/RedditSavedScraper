# RedditSavedScraper
PRAW based Reddit Media Scraper for saved posts

# Features
- PRAW Based
- CLI
- Unsaves the posts which you downloaded

# Setup
- Download or Clone the repository
- Download and Replace [ffmpeg.exe](https://www.ffmpeg.org/download.html) to the same directory of the repository
- Install the requirements `pip install -r requirements.txt`
- Fill out the informations in `user.json`
- Run `python main.py`

# Used Modules
- `gallery-dl`
- `PRAW`
- `click`
- `sys`
- `json`

# Warning
- `Python 3.8` is recommended version for this repository
- If there are some issues or suggestions, write them on `Issues`
- If the post is `crossposted` or `shared`, it can't be donwloaded.