from db_classes import db_session, start_session, meme_processed


def insert_meme_processed(data, db_session = db_session):

	#To-Do handle repetition 

	#create new instance for db
	new_processed = meme_processed(
						id = data['id'],
						img_name = data['img_name'],
						img_sentiment = data['img_sentiment'],
						text_sentiment = data['text_sentiment'],
						text_magnitude = data['text_magnitude'],
						capt_sentiment = data['capt_sentiment'],
						capt_magnitude = data['capt_magnitude'],

						)

	#push to db
	db_session.add(new_processed)
	db_session.commit()


	#success
	return True




'''
data = {
	"id":101,
	"img_name": "test1",
	"img_sentiment": 1.1,
	"text_sentiment": 1.2,
	"text_magnitude": 1.3,
	"capt_sentiment": 1.5,
	"capt_magnitude": 1.6,

}

status = insert_meme_processed(data)

print (status)
'''