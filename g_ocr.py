from google.cloud import vision
import io
from wordsegment import load, segment


def detect_text(path):
    """Detects text in the file."""


    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:')

    load()

    for text in texts:
        print('\n"{}"'.format(text.description))

        #vertices = (['({},{})'.format(vertex.x, vertex.y)
                    #for vertex in text.bounding_poly.vertices])

        #print('bounds: {}'.format(','.join(vertices)))
    try:
        segmented_words = " ".join(segment(texts[0].description))
    except:
        segmented_words = ""

    return segmented_words.upper()
