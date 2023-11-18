from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .forms import *


# домашняя
class HomeView(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, locals())

# регистрация
class RegisterView(TemplateView):
    form_class = UserForm
    success_url = reverse_lazy('home')
    def get(self, request, *args, **kwargs):
        form = self.form_class(None)
        return render(request, self.template_name, locals())

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid(): # проверяем форму регистрации
            user =form.save(commit=False)
            user.first_name = form.cleaned_data['first_name']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)

            if user is not None and user.is_active:
                login(request,user)
                return HttpResponseRedirect("/")

        return render(request, self.template_name, locals())

# логин
class LoginView(TemplateView):
    success_url = reverse_lazy('home')
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, locals())

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            login(request,user)
            return HttpResponseRedirect("/")
        err = "Неправильное имя пользователя или пароль"
        return render(request, self.template_name, locals())

# выход
class LogoutView(TemplateView):
    success_url = reverse_lazy('home')
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect("/")

class ApplicationCreateView(TemplateView, LoginRequiredMixin):
    form_class = ApplicationForm
    def get(self, request, *args, **kwargs):
        form = self.form_class(None)
        return render(request, self.template_name, locals())

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():  # проверяем форму регистрации
            instance = form.save(commit=False)
            instance.applicant = request.user
            instance.save()
            return redirect('profile')

        return render(request, self.template_name, locals())

class ProfileView(TemplateView, LoginRequiredMixin):
    def get(self, request, *args, **kwargs):
        applications = Application.objects.filter(applicant=request.user).order_by('-created')
        context = {'application_list': applications}
        return render(request, self.template_name, context)
