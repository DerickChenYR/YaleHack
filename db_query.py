from db_classes import db_session, start_session, meme_processed, meme_raw


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

}

#status = insert_meme_raw(data1)
#status = get_raw_by_id(101)
#print (status.caption)
'''