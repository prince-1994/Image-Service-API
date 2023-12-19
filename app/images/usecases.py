from PIL import Image, ImageEnhance, ImageOps
from common.logger import AppLogger


logger = AppLogger(__name__)


editing_dict = dict(
    # Image Enhancer functions
    bri=lambda img, val: ImageEnhance.Brightness(img).enhance(float(val)),
    col=lambda img, val: ImageEnhance.Color(img).enhance(float(val)),
    con=lambda img, val: ImageEnhance.Contrast(img).enhance(float(val)),
    sharp=lambda img, val: ImageEnhance.Sharpness(img).enhance(float(val)),

    # Image operations functions
    rotate=lambda img, val: img.rotate(float(val)),
    mirror=lambda img, val: ImageOps.mirror(img) if bool(val) else img,
    flip=lambda img, val: ImageOps.flip(img) if bool(val) else img

    # Image write text function
)


def edit(img: Image.Image, editing_params: dict):
    for param, val in editing_params.items():
        if param not in editing_dict:
            continue
        img = editing_dict[param](img, val)
    return img
