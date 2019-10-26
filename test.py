from g_ocr import detect_text
from g_textentity import analyze_entities
import os

CONFIG_FILE = "config/gcloud_credentials.json"
TEST_MEME = "images/img1.jpg"

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CONFIG_FILE

img_text = detect_text(TEST_MEME)
analyze_entities(img_text)