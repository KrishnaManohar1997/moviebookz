from django.conf.urls import url
from django.urls import path
from . import views

# We added namespace for our app
app_name = 'api'

urlpatterns = [
    path('movies/<city_name>', views.movies_in_city, name="movies_in_city"),
    url('movies', views.all_movies, name="movies"),
    path('book/<city_name>/<movie_name>/<theatre_name>/<show_name>', views.book_ticket, name="book_ticket"),
    path('shows/<movie_name>/<city_name>',views.available_shows_for_movie,name="shows_of_movie_in_city"),
    url('cities', views.all_cities, name="cities"),
    url('login', views.user_login, name="login"),
    url('logout', views.user_logout, name="logout"),
    url('registration', views.user_registration, name="registration"),
]
