import io
import base64
from PIL import Image


def generate_thumbnail_100(base_image: str):
    try:
        img_b64 = base_image.split(",")[1]
    except:
        img_b64 = base_image
    try:
        image = base64.b64decode(img_b64)
        img = Image.open(io.BytesIO(image))
        resized_img = img.resize((200, 200))
        buffer = io.BytesIO()
        resized_img.save(buffer, format="PNG")
        resized_img_b64 = "data:image/jpg;base64," + base64.b64encode(buffer.getvalue()).decode('utf-8')
    except:
        return "Couldn't decode image: %s" % base_image

    return resized_img_b64
