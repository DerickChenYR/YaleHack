#!/usr/bin/python3.6
#DB Classes

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

import json


from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.pool import NullPool

DB_LOCAL_PATH = "yhack.db"
SQLALCHEMY_DATABASE_PATH = 'sqlite:///' + DB_LOCAL_PATH

engine = create_engine(SQLALCHEMY_DATABASE_PATH, poolclass=NullPool)
db_session = scoped_session(sessionmaker(bind=engine,expire_on_commit=False))

def start_session():
    engine = create_engine(SQLALCHEMY_DATABASE_PATH, poolclass=NullPool)
    db_session = scoped_session(sessionmaker(bind=engine,expire_on_commit=False))
    return db_session


class meme_processed(db.Model):

	__tablename__ = "meme_processed"

	id = db.Column(db.Integer, primary_key = True)
	img_name = db.Column(db.TEXT)
	img_sentiment = db.Column(db.TEXT)
	text_sentiment = db.Column(db.TEXT)
	text_magnitude = db.Column(db.TEXT)
	capt_sentiment = db.Column(db.TEXT)
	capt_magnitude = db.Column(db.TEXT)

