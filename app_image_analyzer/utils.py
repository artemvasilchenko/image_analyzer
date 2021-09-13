from io import BytesIO
from typing import Tuple, Optional

from PIL import Image

BLACK_PIXEL = (0, 0, 0)
WHITE_PIXEL = (255, 255, 255)


def get_analysis_result(image_file: BytesIO, hex_code: str = None) -> \
        Tuple[int, int, Optional[int]]:
    search_color = hex_to_tuple(hex_code) if hex_code else None
    with Image.open(image_file).convert('RGB') as image:
        black_pixel_count: int = 0
        white_pixel_count: int = 0
        search_color_count: int = 0 if search_color else None
        for pixel in image.getdata():
            if pixel == search_color:
                search_color_count += 1
            if pixel == BLACK_PIXEL:
                black_pixel_count += 1
            elif pixel == WHITE_PIXEL:
                white_pixel_count += 1
        return black_pixel_count, white_pixel_count, search_color_count


def hex_to_tuple(hex_code: str) -> Tuple[int, int, int]:
    hex_code = hex_code[1:]
    if len(hex_code) == 3:
        hex_code = ''.join([2 * ch for ch in hex_code])
    return tuple(bytearray.fromhex(hex_code))
