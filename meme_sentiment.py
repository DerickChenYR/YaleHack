from g_ocr import detect_text
from g_textentity import analyze_entities
from g_textsentiment import analyze_sentiment
import os
import sys

CONFIG_FILE = "config/gcloud_credentials.json"

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CONFIG_FILE


def gen_meme_sentiment(id, file_name, caption = None):

	
	img_text = detect_text(file_name)
	
	print("Analysing Entities")
	entities_mentioned = analyze_entities(img_text)

	text_score, text_magnitude = analyze_sentiment(img_text)

	if caption:
		capt_score, capt_magnitude = analyze_sentiment(caption)
	else:
		capt_score = None
		capt_magnitude = None

	print(f"entities: {entities_mentioned}\ntext_score = {text_score}, text_magnitude = {text_magnitude}\ncapt_score = {capt_score}, capt_magnitude = {capt_magnitude}")

	data = {
		"id":id,
		"img_name": file_name,
		"img_sentiment": -999,
		"text_sentiment": text_score,
		"text_magnitude": text_magnitude,
		"capt_sentiment": capt_score,
		"capt_magnitude": capt_magnitude,

	}

	return data


if __name__ == "__main__":

	ret = gen_meme_sentiment(sys.argv[1], sys.argv[2])
	print(ret)