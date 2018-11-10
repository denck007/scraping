
import os
import re
import praw
from datetime import datetime
reddit = praw.Reddit("bot1",user_agent='bot1 user agent')
reddit.read_only=True

for submission in reddit.subreddit('hardwareswap').stream.submissions():
    print(submission.title)