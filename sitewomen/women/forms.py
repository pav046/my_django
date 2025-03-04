from captcha.fields import CaptchaField
from django import forms
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible

from .models import Category, Husband, Women, UploadFiles
from django.core.validators import MinLengthValidator, MaxLengthValidator


# @deconstructible
# class RussianValidator:
#     ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыъэюя0123456789- "
#     code = 'russian'
#
#     def __init__(self, message=None):
#         self.message = message if message else "В заголовке должны использоваться только русские буквы, цифры, символы дефиса и пробела!"
#
#     def __call__(self, value, *args, **kwargs):
#         if set(value).difference(set(self.ALLOWED_CHARS)) != set():
#             raise ValidationError(self.message, code=self.code, params={'value': value})


# class AddMyPostForm(forms.Form):
#     title = forms.CharField(
#         max_length=255,
#         label='Имя, Фамилия',
#         widget=forms.TextInput(attrs={'class': 'form-input'}),
#         min_length=5,
#         error_messages={'min_length': 'Слишком короткий заголовок',
#                         'max_length': 'Слишком длинный заголовок'},)
#     slug = forms.SlugField(
#         max_length=255,
#         label='URL',
#         min_length=5,
#         validators=[
#         MaxLengthValidator(255, message='Слишком длинный URL'),
#         MinLengthValidator(5, message='Слишком короткий URL')])
#     content = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 5}), required=False, label='Общаяя информация')
#     is_published = forms.BooleanField(required=False, label='Опубликовано', initial=True)
#     cat = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория', empty_label='Категория не выбрана')
#     husband = forms.ModelChoiceField(queryset=Husband.objects.all(), required=False, label='Муж', empty_label='Нет мужа')
#
#
#     def clean_title(self):
#         ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыъэюя0123456789- "
#         value = self.cleaned_data['title']
#         if set(value).difference(set(ALLOWED_CHARS)) != set():
#             raise ValidationError("В заголовке должны использоваться только русские буквы, цифры, символы дефиса и пробела!")
#         return value

class AddMyPostForm(forms.ModelForm):
    cat = forms.ModelChoiceField(queryset=Category.objects.all(),
                                 label='Категория',
                                 empty_label='Категория не выбрана')

    husband = forms.ModelChoiceField(queryset=Husband.objects.all(), required=False, label='Муж', empty_label='Нет мужа')

    slug = forms.SlugField(
        max_length=255,
        label='URL',
        min_length=5,)

    class Meta:
        model = Women
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat', 'husband', 'my_tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 5})
        }
        labels = {'slug': 'URL'}

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError('Длина превышает 50 символов')
        return title


class AddFilesForm(forms.ModelForm):
    # file = forms.FileField(label='Файл')
    class Meta:
        model = UploadFiles
        fields = ['file']


class ContactForm(forms.Form):
    name = forms.CharField(label="Имя", max_length=255)
    email = forms.EmailField(label="Email")
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
    captcha = CaptchaField()

