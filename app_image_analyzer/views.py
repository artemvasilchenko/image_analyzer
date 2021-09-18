import logging

from django.shortcuts import render
from django.views import View

from app_image_analyzer.forms import UploadImageForm
from app_image_analyzer.utils import get_analysis_result

logger = logging.getLogger(__name__)


class UploadAndAnalyzeImageView(View):
    """
    View для загрузки изображения и HEX-кода в html-форму, обработки данных
    и возврата результата анализа на html-страницу.
    """
    upload_image_template = 'app_image_analyzer/upload_image_form.html'
    analysis_result_template = 'app_image_analyzer/analysis_result.html'

    def get(self, request):
        """
        Обработка GET-запроса.
        """
        logger.info('GET request from user')

        form = UploadImageForm()
        context = {
            'form': form,
        }
        return render(request, self.upload_image_template, context=context)

    def post(self, request):
        """
        Обработка POST-запроса.
        """
        logger.info('POST request from user')

        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():

            image = form.cleaned_data.get('image')
            hex_code = form.cleaned_data.get('hex_code')

            logger.info('User upload valid data in form', extra={
                'file_name': image.name,
                'file_size': image.size,
                'hex_code': hex_code,
            })

            black_pixel_count, white_pixel_count, search_color_pixel = \
                get_analysis_result(image_file=image, hex_code=hex_code)
            context = {
                'file_name': image.name,
                'black_pixel_count': black_pixel_count,
                'white_pixel_count': white_pixel_count,
                'search_color': hex_code,
                'search_color_pixel': search_color_pixel,
            }

            logger.info('Return analysis result', extra=context)
            return render(request, self.analysis_result_template,
                          context=context)

        context = {
            'form': form,
        }
        logger.info('User upload not valid data in form')
        return render(request, self.upload_image_template, context=context)
