from django.shortcuts import render
from django.views import View

from app_image_analyzer.forms import UploadImageForm
from app_image_analyzer.utils import get_analysis_result


class UploadAndAnalyzeImageView(View):
    upload_image_template = 'app_image_analyzer/upload_image_form.html'
    analysis_result_template = 'app_image_analyzer/analysis_result.html'

    def get(self, request):
        form = UploadImageForm()
        context = {
            'form': form,
        }
        return render(request, self.upload_image_template, context=context)

    def post(self, request):
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data.get('image')
            hex_code = form.cleaned_data.get('hex_code')
            context = {
                'file_name': image.name,
                'analysis_result': get_analysis_result(image),
            }
            return render(request, self.analysis_result_template,
                          context=context)

        context = {
            'form': form,
        }
        return render(request, self.upload_image_template, context=context)
