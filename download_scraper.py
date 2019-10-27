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
    for f in os.listdir("downloads/jet_blue_memes"):
        if ".jpg" in f:
            insert_data = {
                'id': f.split(".")[0],
                'date': "",
                'caption': "",
                'url':""
            }
            print(insert_data)
            print(insert_meme_raw(insert_data))
if __name__ == "__main__":
    main()

