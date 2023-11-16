from django.urls import path

from cabinet.views import *

urlpatterns = [
    path('', HomeView.as_view(template_name="home.html"), name="home"),
    path('login/', LoginView.as_view(template_name="login.html"), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('register/', RegisterView.as_view(template_name="register.html"), name="register"),

]