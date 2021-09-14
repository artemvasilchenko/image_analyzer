from django import forms
from django.core.validators import RegexValidator, FileExtensionValidator


class UploadImageForm(forms.Form):
    image = forms.ImageField(
        label='Файл изображения',
        validators=[
            FileExtensionValidator(allowed_extensions=(
                'jpg', 'jpeg', 'gif', 'bmp', 'png',
            ))])
    hex_code = forms.CharField(
        max_length=7,
        label='HEX-код искомого цвета',
        required=False,
        validators=[
            RegexValidator(regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')
        ],
        error_messages={
            'invalid': 'Некорректный HEX-код. Примеры: #FFFFFF, #fff, #000'
        },
    )
