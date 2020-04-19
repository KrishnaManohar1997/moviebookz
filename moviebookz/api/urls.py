from django.conf.urls import url
from django.urls import path
from . import views

# We added namespace for our app
app_name = 'api'

urlpatterns = [
    url('login', views.user_login, name="login"),
    url('logout', views.user_logout, name="logout"),
    url('registration', views.user_registration, name="registration"),
]
