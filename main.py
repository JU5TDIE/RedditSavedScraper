import sys
import praw
import json
import click
from gallery_dl.job import DownloadJob
from prawcore.exceptions import OAuthException
from prawcore.exceptions import ResponseException