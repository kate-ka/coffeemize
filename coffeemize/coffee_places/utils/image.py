from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile


def crop_image_to_square(img, avatar=False):
    if not avatar:
        THUMB_SIZE = 400, 400
    else:
        THUMB_SIZE = 80, 80
    # create an image from binary data with BytesIO
    img = Image.open(BytesIO(img))
    width, height = img.size

    if width > height:
        delta = width - height
        left = int(delta / 2)
        upper = 0
        right = height + left
        lower = height
    else:
        delta = height - width
        left = 0
        upper = int(delta / 2)
        right = width
        lower = width + upper

    img = img.crop((left, upper, right, lower))
    img.thumbnail(THUMB_SIZE, Image.ANTIALIAS)
    buffer = BytesIO()
    img.save(fp=buffer, format='JPEG')
    buff_val = buffer.getvalue()
    return ContentFile(buff_val)
