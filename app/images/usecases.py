from PIL import Image, ImageEnhance
from common.logger import AppLogger


logger = AppLogger(__name__)


editing_dict = dict(
    # Image Enhancer functions
    bri=lambda img, val: ImageEnhance.Brightness(img).enhance(int(val)),
    col=lambda img, val: ImageEnhance.Color(img).enhance(int(val)),
    con=lambda img, val: ImageEnhance.Contrast(img).enhance(int(val)),
    sharp=lambda img, val: ImageEnhance.Sharpness(img).enhance(int(val)),
)


def edit(img: Image.Image, editing_params: dict):
    for param, val in editing_params.items():
        if param not in editing_dict:
            continue
        img = editing_dict[param](img, val)
    return img
