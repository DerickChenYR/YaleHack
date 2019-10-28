
import requests
import re
import os

import sqlite3

from db_query import insert_meme_raw

from flask_sqlalchemy import SQLAlchemy

from meme_sentiment import gen_meme_sentiment

DB_LOCAL_PATH = "yhack.db"
SQLALCHEMY_DATABASE_PATH = 'sqlite:///' + DB_LOCAL_PATH


def main():
    for f in os.listdir("jetblue_memes"):
        if ".jpg" in f:
            insert_data = {
                'id': f.split(".")[0],
                'date': "",
                'caption': "",
                'url':""
            }
            #print(insert_data)
            #print(insert_meme_raw(insert_data))
            gen_meme_sentiment(insert_data['id'], "jetblue_memes/"+f, "None")


if __name__ == "__main__":
    main()

