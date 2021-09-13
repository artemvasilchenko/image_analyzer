from django.urls import path

from app_image_analyzer.views import UploadAndAnalyzeImageView

app_name = 'analyzer'
urlpatterns = [
    path('upload_image/', UploadAndAnalyzeImageView.as_view(),
         name='upload_image'),
]
