from meme_sentiment import gen_meme_sentiment
import sqlite3
import pandas as pd


conn = sqlite3.connect("yhack.db")
df = pd.read_sql_query("select * from meme_raw where id not in(select id from meme_processed);",conn)

print(df)

for index,row in df.iterrows():
    gen_meme_sentiment(row['id'],"images/{}.jpg".format(row['id']),row['date'])
    #print(row['id'])
tagged_df = pd.read_sql_query("select id,comp_score from meme_processed;",conn)
tagged_df['location'] = "//inlaid-rig-257102-vcm/meme_dataset/documents/images/"+tagged_df['id'].astype(str)+".jpg"
tagged_df = tagged_df[['location','comp_score']]
tagged_df.to_csv("scores.csv",index=False)
print(tagged_df)