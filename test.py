from g_ocr import detect_text
from g_textentity import analyze_entities
TEST_MEME = "images/img1.jpg"

img_text = detect_text(TEST_MEME)
analyze_entities(img_text)