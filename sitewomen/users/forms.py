from datetime import datetime

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, \
    PasswordChangeForm


class LoginForm(AuthenticationForm):

    username = forms.CharField(label='Логин/E-mail', widget=forms.TextInput(
        attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class RegisterForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        labels = {'email': 'E-mail', 'last_name': 'Фамилия', 'first_name': 'Имя'}
        widgets = {'email': forms.TextInput(attrs={'class': 'form-input'}),
                   'last_name': forms.TextInput(attrs={'class': 'form-input'}),
                   'first_name': forms.TextInput(attrs={'class': 'form-input'})}

    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    def clean_email(self):
        if get_user_model().objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError('Такой E-mail уже зарегистрирован')
        else:
            return self.cleaned_data['email']

    # def clean_password2(self):
    #     if self.cleaned_data['password'] != self.cleaned_data['password2']:
    #         raise forms.ValidationError('Пароли не совпадают')
    #     else:
    #         return self.cleaned_data['password']


class EditProfileForm(forms.ModelForm):

    username = forms.CharField(disabled=True, widget=forms.TextInput(
        attrs={'class': 'form-input'}), label='Логин')
    email = forms.CharField(disabled=True, widget=forms.EmailInput(
        attrs={'class': 'form-input'}), label='E-mail', required=False)
    today = datetime.now().year
    birth_date = forms.DateField(label='Дата рождения', widget=forms.SelectDateWidget(years=range(today-100, today+1)))


    class Meta:
        model = get_user_model()
        fields = ['photo', 'username', 'email', 'first_name', 'last_name', 'birth_date']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'})
        }


class ChangePasswordForm(PasswordChangeForm):
    new_password1 = forms.CharField(label='Новый пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password2 = forms.CharField(label='Повторите новый пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    old_password = forms.CharField(label='Старый пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
