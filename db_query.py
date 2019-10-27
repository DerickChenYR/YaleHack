from db_classes import db_session, start_session, meme_processed, meme_raw
import base64

def insert_meme_processed(data, db_session = db_session):

	#create new instance for db
	new_processed = meme_processed(

						id = data['id'],
						date = data['date'],
						entities = data['entities'],
						ocr_string = data['ocr_string'],
						img_sentiment = data['img_sentiment'],
						text_sentiment = data['text_sentiment'],
						text_magnitude = data['text_magnitude'],
						capt_sentiment = data['capt_sentiment'],
						capt_magnitude = data['capt_magnitude'],
						comp_score = data['comp_score']
						)

	#push to db

	db_session.add(new_processed)
	db_session.commit()



	

def insert_meme_raw(data, db_session = db_session):

	#create new instance for db
	new_raw = meme_raw(

						id = data['id'],
						date = data['date'],
						caption = data['caption'],
						url = data['url']
						)

	#push to db
	try:

		db_session.add(new_raw)
		db_session.commit()
		#success
		return True
	except:
		return False



def get_raw_by_id(id, db_session = db_session):

	existing = db_session.query(meme_raw).filter_by(id=id).first()

	return existing




import pandas as pd
from sqlalchemy.inspection import inspect
from collections import defaultdict

#PASSED
#Helper method to turn sqlalchemy objects to dict
#https://gist.github.com/garaud/bda10fa55df5723e27da
def query_to_dict(rset):
    result = defaultdict(list)
    for obj in rset:
        instance = inspect(obj)
        for key, x in instance.attrs.items():
            result[key].append(x.value)
    return result


#PASSED
#Reads SQLAlchemy query objects into pandas
def sqlalchemy_to_df(db_table, db_session = db_session):
    rset = db_session.query(db_table).all()
    df = pd.DataFrame(query_to_dict(rset))
    pd.to_datetime(df['date'])
    df_sorted_date = df.sort_values(by=['date'])

    db_session.close()

    return df_sorted_date


def prepare_entities_freq(df, top = 10):


	entities = []

	for i in list(df['entities']):
		if " " in i:
			entities.extend(i.split(" "))
		else:
			entities.append(i)

	from collections import Counter

	freq = Counter(entities).most_common(top)

	return dict(freq)


def prepare_gallery_memes(df_sorted_comp, top = 5):

	top_ids = list(df_sorted_comp['id'].head(top))
	images_folder = "images/"
	encoded_imgs = []

	for id in top_ids:
		encoded_img = base64.b64encode(open(images_folder + str(id) + ".jpg", 'rb').read())
		encoded_imgs.append(encoded_img)

	return encoded_imgs


def prepare_gallery_memes_jetblue(df_sorted_comp, top = 5):

	top_ids = list(df_sorted_comp['id'].head(top))
	images_folder = "downloads/jet_blue_memes/"
	encoded_imgs = []

	for id in top_ids:
		encoded_img = base64.b64encode(open(images_folder + str(id) + ".jpg", 'rb').read())
		encoded_imgs.append(encoded_img)

	return encoded_imgs


'''
data1 = {
	"id":101,
	"date": "SampleTime",
	'caption': "CAPTION HERE"
	'url': "URL"
}



data2 = {
	"id":101,
	"date": "SampleTime",
	'entities': "ENTITIES ONE TWO THREE",
	"ocr_string": "OCR ONE TWO THREE",
	"img_sentiment": 1.1,
	"text_sentiment": 1.2,
	"text_magnitude": 1.3,
	"capt_sentiment": 1.5,
	"capt_magnitude": 1.6,
	"comp_score":[avg of capt and text]

}

#status = insert_meme_raw(data1)
#status = get_raw_by_id(101)
#print (status.caption)
'''