import io
import base64

from PIL import Image

from app.exceptions.invalid_b64_image_exception import InvalidB64ImageException


def generate_thumbnail_100(base_image: str) -> str:
    try:
        image = base64.b64decode(base_image)
        img = Image.open(io.BytesIO(image))
    except:
        raise InvalidB64ImageException
    img.thumbnail((100, 100), Image.ANTIALIAS)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    resized_img_b64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return resized_img_b64

