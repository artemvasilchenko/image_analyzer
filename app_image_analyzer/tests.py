import logging

from django.test import SimpleTestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from app_image_analyzer.utils import hex_to_tuple, get_analysis_result

# white(255, 255, 255) - 10 pix, black(0, 0, 0) - 2 pix, red(255, 0, 0) - 3 pix
CONTENT_WHITE_MORE_THAN_BLACK = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x03\x00\x00\x00\x05"
    b"\x08\x06\x00\x00\x00\x80qV\xa2\x00\x00\x00'IDAT\x18W=\x8bA\x0e\x000"
    b"\x0c\x82\xe0\xff\x8fv\xb1m\xe6I\x82\n$\t\x8d\xbf\r@\xa8\xd13\xda\xf1"
    b"\x82\xda#\x0f\xec\xa9\x18\xf4{\xc9b8\x00\x00\x00\x00IEND\xaeB`\x82"
)

# white(255, 255, 255) - 7 pix, black(0, 0, 0) - 7 pix, red(255, 0, 0) - 1 pix
CONTENT_WHITE_EQ_BLACK = (
    b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x03\x00\x00\x00\x05'
    b'\x08\x06\x00\x00\x00\x80qV\xa2\x00\x00\x00#IDAT\x18Wcd``\xf8\xff\xff'
    b'\xff\x7f\x06\x10`\x84\xb3P8\x8c\x8c\x0c\x8c e`5 \x19d\x0e\x00c\xf6\r'
    b'\xfau=\xd4\xc2\x00\x00\x00\x00IEND\xaeB`\x82'
)

# white(255, 255, 255) - 7 pix, black(0, 0, 0) - 7 pix, red(255, 0, 0) - 1 pix
CONTENT_WHITE_LESS_THAN_BLACK = (
    b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x03\x00\x00\x00\x05'
    b'\x08\x06\x00\x00\x00\x80qV\xa2\x00\x00\x00"IDAT\x18Wcd``\xf8\xff\xff'
    b'\xff\x7f\x06\x10`\x84\xb3@\x1c\xb8\x0c##\x84\x03V\x03\x93\x81q\x00X'
    b'\x02\r\xfa\xef0l\xeb\x00\x00\x00\x00IEND\xaeB`\x82'
)

INCORRECT_CONTENT = b'\x00\x00\x00\x00'


def get_image_test_file(file_content: bytes) -> SimpleUploadedFile:
    """
    Создает тестовый файл изображения.

    :return: объект файла класса SimpleUploadedFile
    """
    image_file = SimpleUploadedFile(name='image.png', content=file_content)
    return image_file


class HexToTupleTest(SimpleTestCase):
    """
    Тестирование функции преобразования HEX-кода в RGB-кортеж.
    """
    def setUp(self):
        logging.disable(logging.CRITICAL)

    def tearDown(self):
        logging.disable(logging.NOTSET)

    def test_hex_to_tuple_1(self):
        hex_code = '#FFFFFF'
        self.assertEqual(hex_to_tuple(hex_code), (255, 255, 255))

    def test_hex_to_tuple_2(self):
        hex_code = '#FFF'
        self.assertEqual(hex_to_tuple(hex_code), (255, 255, 255))

    def test_hex_to_tuple_3(self):
        hex_code = '#fff'
        self.assertEqual(hex_to_tuple(hex_code), (255, 255, 255))

    def test_hex_to_tuple_4(self):
        hex_code = '#000'
        self.assertEqual(hex_to_tuple(hex_code), (0, 0, 0))

    def test_hex_to_tuple_5(self):
        hex_code = '#000000'
        self.assertEqual(hex_to_tuple(hex_code), (0, 0, 0))

    def test_hex_to_tuple_6(self):
        hex_code = '000000'
        self.assertIsNone(hex_to_tuple(hex_code))

    def test_hex_to_tuple_7(self):
        hex_code = '#asdf'
        self.assertIsNone(hex_to_tuple(hex_code))


class GetAnalysisResult(SimpleTestCase):
    """
    Тестирование функции подсчета черных, белых пикселей и пикселей
    искомого цвета.
    """
    def setUp(self):
        logging.disable(logging.CRITICAL)

    def tearDown(self):
        logging.disable(logging.NOTSET)

    def test_only_image(self):
        image = get_image_test_file(CONTENT_WHITE_MORE_THAN_BLACK)
        self.assertEqual(get_analysis_result(image), (2, 10, None))

    def test_image_and_short_hex_code_1(self):
        image = get_image_test_file(CONTENT_WHITE_MORE_THAN_BLACK)
        hex_code = '#F00'
        result = get_analysis_result(image_file=image, hex_code=hex_code)
        self.assertEqual(result, (2, 10, 3))

    def test_image_and_short_hex_code_2(self):
        image = get_image_test_file(CONTENT_WHITE_MORE_THAN_BLACK)
        hex_code = '#000'
        result = get_analysis_result(image_file=image, hex_code=hex_code)
        self.assertEqual(result, (2, 10, 2))

    def test_image_and_short_hex_code_3(self):
        image = get_image_test_file(CONTENT_WHITE_MORE_THAN_BLACK)
        hex_code = '#FFF'
        result = get_analysis_result(image_file=image, hex_code=hex_code)
        self.assertEqual(result, (2, 10, 10))

    def test_image_and_full_hex_code_1(self):
        image = get_image_test_file(CONTENT_WHITE_MORE_THAN_BLACK)
        hex_code = '#FF0000'
        result = get_analysis_result(image_file=image, hex_code=hex_code)
        self.assertEqual(result, (2, 10, 3))

    def test_image_and_full_hex_code_2(self):
        image = get_image_test_file(CONTENT_WHITE_MORE_THAN_BLACK)
        hex_code = '#000000'
        result = get_analysis_result(image_file=image, hex_code=hex_code)
        self.assertEqual(result, (2, 10, 2))

    def test_image_and_full_hex_code_3(self):
        image = get_image_test_file(CONTENT_WHITE_MORE_THAN_BLACK)
        hex_code = '#FFFFFF'
        result = get_analysis_result(image_file=image, hex_code=hex_code)
        self.assertEqual(result, (2, 10, 10))

    def test_image_and_incorrect_hex_code(self):
        image = get_image_test_file(CONTENT_WHITE_MORE_THAN_BLACK)
        hex_code = 'asdf'
        result = get_analysis_result(image_file=image, hex_code=hex_code)
        self.assertEqual(result, (2, 10, None))


class UploadAndAnalyzeImageViewTest(SimpleTestCase):
    """
    Тестирование работы приложения.
    """
    def setUp(self):
        logging.disable(logging.CRITICAL)

    def tearDown(self):
        logging.disable(logging.NOTSET)

    def test_get_req_to_analyze_image_url(self):
        """
        Тест url-адреса.
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_get_req_to_analyze_image_template(self):
        """
        Тест на использование шаблона формы загрузки данных.
        """
        response = self.client.get(reverse('analyzer:upload_image'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'app_image_analyzer/upload_image_form.html')

    def test_get_req_to_analyze_image_page(self):
        """
        Тест содержания страницы загрузки файла и указания цвета.
        """
        response = self.client.get(reverse('analyzer:upload_image'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Загрузка файла изображения')
        self.assertContains(response, 'Файл изображения')
        self.assertContains(response, 'HEX-код искомого цвета')
        self.assertContains(response, 'Отправить')

    def test_post_req_to_analyze_image_template(self):
        """
        Тест на использование шаблона результата анализа.
        """
        image = get_image_test_file(CONTENT_WHITE_MORE_THAN_BLACK)
        response = self.client.post(reverse('analyzer:upload_image'),
                                    data={'image': image})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'app_image_analyzer/analysis_result.html')

    def test_post_req_to_analyze_image_page_1(self):
        """
        Тест содержания страницы результата при отправке только файла.
        """
        image = get_image_test_file(CONTENT_WHITE_MORE_THAN_BLACK)
        response = self.client.post(reverse('analyzer:upload_image'),
                                    data={'image': image})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Имя файла: {}'.format(image.name))
        self.assertContains(response, 'Черных пикселей:')
        self.assertContains(response, 'Белых пикселей:')
        self.assertContains(response,
                            'Вернуться на страницу загрузки изображения')
        self.assertContains(response, reverse('analyzer:upload_image'))

        self.assertNotContains(response, 'А пикселей искомого цвета')

    def test_post_req_to_analyze_image_page_2(self):
        """
        Тест содержания страницы результата при отправке файла и HEX-кода.
        """
        image = get_image_test_file(CONTENT_WHITE_MORE_THAN_BLACK)
        hex_code = '#FFFFFF'
        response = self.client.post(
            reverse('analyzer:upload_image'),
            data={'image': image, 'hex_code': hex_code}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Имя файла: {}'.format(image.name))
        self.assertContains(response, 'Черных пикселей:')
        self.assertContains(response, 'Белых пикселей:')
        self.assertContains(response, reverse('analyzer:upload_image'))
        self.assertContains(response, 'А пикселей искомого цвета')
        self.assertContains(response,
                            'Вернуться на страницу загрузки изображения')

    def test_post_req_to_analyze_image_page_incorrect_upload_data(self):
        """
        Тест содержания страницы результата при отправке некорректного файла и
        некорректного HEX-кода.
        """
        file = get_image_test_file(INCORRECT_CONTENT)
        file.name = 'test'
        hex_code = 'asdf'
        response = self.client.post(
            reverse('analyzer:upload_image'),
            data={'image': file, 'hex_code': hex_code}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Загрузка файла изображения')
        self.assertContains(response, 'Загрузите правильное изображение. '
                                      'Файл, который вы загрузили, поврежден '
                                      'или не является изображением.')
        self.assertContains(response, 'Файл изображения')
        self.assertContains(response,
                            'Некорректный HEX-код. '
                            'Примеры: #FFFFFF, #fff, #000')
        self.assertContains(response, 'HEX-код искомого цвета')
        self.assertContains(response, 'Отправить')
        self.assertTemplateUsed(response,
                                'app_image_analyzer/upload_image_form.html')

    def test_post_req_to_analyze_image_page_incorrect_extension(self):
        """
        Тест содержания страницы результата при отправке файла изображения
        неподдерживаемого расширения.
        """
        image = get_image_test_file(CONTENT_WHITE_MORE_THAN_BLACK)
        extension = 'psd'
        image.name = 'image.{}'.format(extension)
        response = self.client.post(
            reverse('analyzer:upload_image'), data={'image': image})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Загрузка файла изображения')
        self.assertContains(response, f'Расширение файлов “{extension}” не '
                                      'поддерживается. Разрешенные расширения:'
                                      ' jpg, jpeg, gif, bmp, png.')
        self.assertContains(response, 'Файл изображения')
        self.assertContains(response, 'HEX-код искомого цвета')
        self.assertContains(response, 'Отправить')
        self.assertTemplateUsed(response,
                                'app_image_analyzer/upload_image_form.html')

    def test_post_req_to_analyze_image_correct_data_1(self):
        """
        Тест анализа результата страницы результата при отправке файла, в
        котором белых пикселей больше количества черных
        и HEX-кода красного цвета.
        """
        image = get_image_test_file(CONTENT_WHITE_MORE_THAN_BLACK)
        hex_code = '#F00'
        response = self.client.post(
            reverse('analyzer:upload_image'),
            data={'image': image, 'hex_code': hex_code}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Белых пикселей больше черных '
                                      'на загруженном изображении')
        self.assertContains(response, 'Имя файла: {}'.format(image.name))
        self.assertContains(response, 'Черных пикселей: 2')
        self.assertContains(response, 'Белых пикселей: 10')
        self.assertContains(response, reverse('analyzer:upload_image'))
        self.assertContains(response,
                            'А пикселей искомого цвета {}: 3'.format(hex_code))
        self.assertContains(response,
                            'Вернуться на страницу загрузки изображения')

    def test_post_req_to_analyze_image_correct_data_2(self):
        """
        Тест анализа результата страницы результата при отправке файла, в
        котором белых пикселей рано количеству черных
        и HEX-кода красного цвета.
        """
        image = get_image_test_file(CONTENT_WHITE_EQ_BLACK)
        hex_code = '#F00'
        response = self.client.post(
            reverse('analyzer:upload_image'),
            data={'image': image, 'hex_code': hex_code}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Одинаковое количество белых и черных '
                                      'пикселей на загруженном изображении')
        self.assertContains(response, 'Имя файла: {}'.format(image.name))
        self.assertContains(response, 'Черных пикселей: 7')
        self.assertContains(response, 'Белых пикселей: 7')
        self.assertContains(response, reverse('analyzer:upload_image'))
        self.assertContains(response,
                            'А пикселей искомого цвета {}: 1'.format(hex_code))
        self.assertContains(response,
                            'Вернуться на страницу загрузки изображения')

    def test_post_req_to_analyze_image_correct_data_3(self):
        """
        Тест анализа результата страницы результата при отправке файла, в
        котором белых пикселей меньше количества черных
        и HEX-кода красного цвета.
        """
        image = get_image_test_file(CONTENT_WHITE_LESS_THAN_BLACK)
        hex_code = '#F00'
        response = self.client.post(
            reverse('analyzer:upload_image'),
            data={'image': image, 'hex_code': hex_code}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Черных пикселей больше белых '
                                      'на загруженном изображении')
        self.assertContains(response, 'Имя файла: {}'.format(image.name))
        self.assertContains(response, 'Черных пикселей: 8')
        self.assertContains(response, 'Белых пикселей: 6')
        self.assertContains(response, reverse('analyzer:upload_image'))
        self.assertContains(response,
                            'А пикселей искомого цвета {}: 1'.format(hex_code))
        self.assertContains(response,
                            'Вернуться на страницу загрузки изображения')
