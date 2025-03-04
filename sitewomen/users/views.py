from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView

from sitewomen import settings
from users.forms import LoginForm, RegisterForm, EditProfileForm, \
    ChangePasswordForm


class LoginUser(LoginView):
    form_class = LoginForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}



    # def get_success_url(self):
    #     return reverse_lazy('home')


# def login_user(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             q = form.cleaned_data
#             user = authenticate(request, username=q['username'], password=q['password'])
#             if user and user.is_active:
#                 login(request, user)
#                 return redirect('home', permanent=True)
#     else:
#         form = LoginForm()
#
#     return render(request, 'users/login.html', {'form': form, 'title': 'Войти'})


# def logout_user(request):
#     logout(request)
#     return redirect('users:login', permanent=True)

# def register(request):
#     print('POST', request.POST)
#     print('GET', request.GET)
#     if request.method == "POST":
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.set_password(form.cleaned_data['password'])
#             user.save()
#             return render(request, "users/registration_done.html", {'title': 'Регистрация прошла успешно'})
#     else:
#         form = RegisterForm()
#
#     return render(request, "users/register.html", {'form': form, 'title': 'Регистрация'})

class RegisterUser(CreateView):
    template_name = 'users/register.html'
    form_class = RegisterForm
    extra_context = {'title': 'Регистрация'}
    success_url = reverse_lazy('users:login')


class UpdateUser(LoginRequiredMixin, UpdateView):
    template_name = 'users/profile.html'
    success_url = reverse_lazy('home')
    extra_context = {'title': 'Мой профиль', 'default_img': settings.DEFAULT_URL_IMG}
    form_class = EditProfileForm

    def get_object(self, queryset=None):
        return get_object_or_404(get_user_model(), pk=self.request.user.pk)

    def get_success_url(self):
        return reverse_lazy('users:profile')

class PasswordChangeUser(PasswordChangeView):
    form_class = ChangePasswordForm
    success_url = reverse_lazy("users:password_change_done")
    template_name = "users/password_change_form.html"
    title = "Смена пароля"





