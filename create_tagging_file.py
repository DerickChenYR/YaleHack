from meme_sentiment import gen_meme_sentiment
import sqlite3
import pandas as pd


conn = sqlite3.connect("yhack.db")
df = pd.read_sql_query("select * from meme_raw",conn)

output_df = ""

print(df)

for index,row in df.iterrows():
    gen_meme_sentiment(row['id'],"images/{}.jpg".format(row['id']),row['date'])
    #print(row['id'])
tagged_df = pd.read_sql_query("select * from meme_processed")
print(tagged_df)