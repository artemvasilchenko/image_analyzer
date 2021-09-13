from io import BytesIO
from typing import Tuple

from PIL import Image

BLACK_PIXEL = (0, 0, 0)
WHITE_PIXEL = (255, 255, 255)


def get_analysis_result(image_file: BytesIO) -> Tuple[int, int]:
    with Image.open(image_file).convert('RGB') as image:
        black_pixel_count: int = 0
        white_pixel_count: int = 0
        for pixel in image.getdata():
            if pixel == BLACK_PIXEL:
                black_pixel_count += 1
            elif pixel == WHITE_PIXEL:
                white_pixel_count += 1
        return black_pixel_count, white_pixel_count
