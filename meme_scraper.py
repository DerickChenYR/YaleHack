import praw
import requests
import re
import os
from bs4 import BeautifulSoup
import sqlite3
import shutil
from db_query import insert_meme_raw
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

DB_LOCAL_PATH = "yhack.db"
SQLALCHEMY_DATABASE_PATH = 'sqlite:///' + DB_LOCAL_PATH


def main():
    if os.path.exists("images"):
        shutil.rmtree("images")
        os.mkdir("images")
    subreddits = ["memes","advice_animals"]
    counter = 0
    for subreddit in subreddits:
        reddit = praw.Reddit(client_id="V8avVeCeT782mQ",client_secret="MHBenrhwZSeqW2mY4pUD74OkNwM",user_agent="meme_crawler")
        sub_memes = reddit.subreddit(subreddit).top(limit=500,time_filter='month')
        for meme in sub_memes:
            if ".jpg" in meme.url:
                r = requests.get(meme.url,stream=True)
                with open("images/{}.jpg".format(counter),'wb') as f:
                    shutil.copyfileobj(r.raw,f)
                del r
                insert_data = {
                    'id': counter,
                    'date': str(datetime.utcfromtimestamp(meme.created_utc)),
                    'caption': meme.title,
                    'url':meme.url
                }
                print(insert_data)
                print(insert_meme_raw(insert_data))
                counter+=1
if __name__ == "__main__":
    main()

