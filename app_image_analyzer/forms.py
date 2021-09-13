from django import forms


class UploadImageForm(forms.Form):
    image = forms.ImageField(label='Файл изображения')
    hex_code = forms.CharField(max_length=7, label='HEX-код искомого цвета',
                               required=False)
