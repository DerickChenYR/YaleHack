CONFIG_FILE = "config/gcloud_credentials.json"


from google.cloud import vision
import io
import os



def detect_text(path):
    """Detects text in the file."""


    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CONFIG_FILE


    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:')

    for text in texts:
        print('\n"{}"'.format(text.description))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])

        #print('bounds: {}'.format(','.join(vertices)))

    return  texts[0].description
