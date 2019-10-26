from g_ocr import detect_text
from g_textentity import analyze_entities
from g_textsentiment import analyze_sentiment

from db_query import get_raw_by_id, insert_meme_processed

import os
import sys

CONFIG_FILE = "config/gcloud_credentials.json"

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CONFIG_FILE


def gen_meme_sentiment(id, file_name, date_string):

	img = get_raw_by_id(id)
	
	img_text = detect_text(file_name)
	
	print("Analysing Entities")
	entities_mentioned = analyze_entities(img_text)

	text_score, text_magnitude = analyze_sentiment(img_text)

	if img.caption:
		capt_score, capt_magnitude = analyze_sentiment(img.caption)
	else:
		capt_score = 0
		capt_magnitude = 0

	print(f"entities: {entities_mentioned}\ntext_score = {text_score}, text_magnitude = {text_magnitude}\ncapt_score = {capt_score}, capt_magnitude = {capt_magnitude}")


	data = {
		"id":id,
		"date": img.date,
		"entities": " ".join(entities_mentioned),
		"ocr_string": img_text,
		"img_sentiment": -999, #guard value for unclassified meme
		"text_sentiment": round(text_score,5),
		"text_magnitude": round(text_magnitude,5),
		"capt_sentiment": round(capt_score,5),
		"capt_magnitude": round(capt_magnitude,5),

	}

	status = insert_meme_processed(data)
	print(status)


if __name__ == "__main__":

	ret = gen_meme_sentiment(sys.argv[1], sys.argv[2], sys.argv[3])
	print(ret)