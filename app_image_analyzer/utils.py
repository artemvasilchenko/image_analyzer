from typing import Tuple, Optional

from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image

BLACK_PIXEL = (0, 0, 0)
WHITE_PIXEL = (255, 255, 255)


def get_analysis_result(image_file: InMemoryUploadedFile,
                        hex_code: str = None) -> \
        Tuple[int, int, Optional[int]]:
    """
    Производит анализ цветов в изображении, считает количество пискелей белого,
    черного и искомого цветов

    :param image_file: загруженный файл изображения
    :param hex_code: HEX-код искомого цвета, если не задан,
    то поиск не производится
    :return: количество черных, белых пискселей и количество пикселей искогомо
    цвета, если цвет не был задан то None
    """
    search_color = hex_to_tuple(hex_code) if hex_code else None
    with Image.open(image_file).convert('RGB') as image:
        black_pixel_count: int = 0
        white_pixel_count: int = 0
        search_color_count: int = 0 if search_color else None
        for pixel in image.getdata():
            if search_color and pixel == search_color:
                search_color_count += 1
            if pixel == BLACK_PIXEL:
                black_pixel_count += 1
            elif pixel == WHITE_PIXEL:
                white_pixel_count += 1
        return black_pixel_count, white_pixel_count, search_color_count


def hex_to_tuple(hex_code: str) -> Optional[Tuple[int, int, int]]:
    """
    Переводит HEX-код в decimal-код цвета в виде кортежа (R, G, B)

    :param hex_code: HEX-код цвета в виде строки (#FFFFFF, #FFF)
    :return: decimal-код цвета в виде кортежа (R, G, B)
    """
    hex_code = hex_code[1:]
    if len(hex_code) == 3:
        hex_code = ''.join([2 * ch for ch in hex_code])
    try:
        result = tuple(bytearray.fromhex(hex_code))
    except ValueError:
        result = None
    return result
