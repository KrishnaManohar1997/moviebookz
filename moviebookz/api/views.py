from django.http.response import JsonResponse
from django.contrib.auth import authenticate, logout, login
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from rest_framework import status
from .models import Theatre, Show, Movie, MovieTheatreShow, City
from .serializer import MovieSerializer, TheatreSerializer, ShowSerializer, CitySerializer, MovieTheatreShowSerializer

# Since we have to add Cross-Site Request Forgery value everytime in Postman, just excluded
# This is generally send from FORM while submitting data
@csrf_exempt
@require_http_methods(['POST'])
def user_login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user:
        if user.is_active:
            login(request, user)
            return JsonResponse({'status': True, 'message': 'Login Successful'})
        else:
            return JsonResponse({'status': False, 'message': 'Account is disabled'})
    else:
        return JsonResponse({'status': False, 'message': 'Invalid Credentials, You can register from Registration endpoint'}, status=status.HTTP_401_UNAUTHORIZED)


@login_required
def user_logout(request):
    logout(request)
    return JsonResponse({'status': 'disconnected', 'message': 'You have been logged out successfully'})


@csrf_exempt
def user_registration(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        print(username, password, email)
        user = User.objects.create_user(username, email, password)
        user.save()
        return JsonResponse({"status": "Registration Successful"}, status=status.HTTP_201_CREATED)
    else:
        return JsonResponse({"status": "Only POST method is allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

# Helper method


def get_theatre_shows_json(list_of_theatre_and_show):
    theatre_shows = [{'theatre_id': id, 'show_id': [d['show_id'] for d in list_of_theatre_and_show if d['theatre_id'] == id]}
                     for id in set(map(lambda d: d['theatre_id'], list_of_theatre_and_show))]
    theatres_list = []
    for theatre_show in theatre_shows:
        theatre = Theatre.objects.filter(pk=theatre_show['theatre_id']).first()
        theatre_shows_json = TheatreSerializer(theatre).data
        shows_list_json = []
        for show_id in theatre_show['show_id']:
            show = Show.objects.filter(pk=show_id).first()
            shows_list_json.append(ShowSerializer(show).data)
        theatre_shows_json["shows"] = shows_list_json
        theatres_list.append(theatre_shows_json)
    return theatres_list


def available_shows_for_movie(request, movie_name, city_name):
    movie_name = movie_name.title()
    city_name = city_name.title()
    requested_city = City.objects.filter(name=city_name).first()
    requested_movie = Movie.objects.filter(name=movie_name).first()
    if requested_city and requested_movie:
        shows_for_requested_movie_in_city = MovieTheatreShow.objects.filter(
            city=requested_city, movie=requested_movie).values('show_id', 'theatre_id')
        theatre_show_list = []
        for show_in_theatre in shows_for_requested_movie_in_city:
            theatre_show_list.append(show_in_theatre)
        theatre_shows_json = get_theatre_shows_json(theatre_show_list)
        movie_details_json = MovieSerializer(requested_movie).data
        movie_details_json["theatres"] = theatre_shows_json
        return JsonResponse(movie_details_json, safe=False)
    elif requested_city is None:
        return JsonResponse({"message": "%s is not registered" % city_name})
    elif requested_movie is None:
        return JsonResponse({"message": "%s movie is not available" % movie_name})
    return JsonResponse({"message": "Sorry we are facing issues from our side"})


def all_movies(request):
    movies = Movie.objects.all()
    movie_list = []
    for movie in movies:
        movie_list.append(MovieSerializer(movie).data)
    print(movie_list)
    return JsonResponse(movie_list, safe=False)


def all_cities(request):
    cities = City.objects.all()
    city_list = []
    for city in cities:
        city_list.append(CitySerializer(city).data)
    print(city_list)
    return JsonResponse(city_list, safe=False)


def book_ticket(request, city_name, movie_name, theatre_name, show_name):
    if request.user.is_authenticated:
        # Normalizing user input data
        city_name, movie_name, theatre_name, show_name = city_name.title(
        ), movie_name.title(), theatre_name.title(), show_name.title()
        city = City.objects.filter(name=city_name).first()
        movie = Movie.objects.filter(name=movie_name).first()
        theatre = Theatre.objects.filter(name=theatre_name).first()
        show = Show.objects.filter(name=show_name).first()
        movie_show = MovieTheatreShow.objects.filter(
            city=city, movie=movie, theatre=theatre, show=show).first()
        if(movie_show):
            if(movie_show.show.available_seats >= 1):
                movie_show.show.available_seats -= 1
                movie_show.show.save()
                return JsonResponse({"message": "You have successfully booked ticket for this show"})
            else:
                return JsonResponse({"message": "There are no Seats available for this Show"})

            return JsonResponse({"message": "Booking In process"})
        else:
            return JsonResponse({"message": "Booking failed as the selected preferences are incorrect/in valid"})
    return JsonResponse({"message": "Kindly login to continue booking for your favorite movie now"}, status=status.HTTP_401_UNAUTHORIZED)


def available_shows_for_movie(request, movie_name, city_name):
    movie_name = movie_name.title()
    city_name = city_name.title()
    requested_city = City.objects.filter(name=city_name).first()
    requested_movie = Movie.objects.filter(name=movie_name).first()
    if requested_city and requested_movie:
        shows_for_requested_movie_in_city = MovieTheatreShow.objects.filter(
            city=requested_city, movie=requested_movie).values('show_id', 'theatre_id')
        theatre_show_list = []
        for show_in_theatre in shows_for_requested_movie_in_city:
            theatre_show_list.append(show_in_theatre)
        theatre_shows_json = get_theatre_shows_json(theatre_show_list)
        movie_details_json = MovieSerializer(requested_movie).data
        movie_details_json["theatres"] = theatre_shows_json
        return JsonResponse(movie_details_json, safe=False)
    elif requested_city is None:
        return JsonResponse({"message": "%s is not registered" % city_name})
    elif requested_movie is None:
        return JsonResponse({"message": "%s movie is not available" % movie_name})

    return JsonResponse({"message": "Sorry we are facing issues from our side"})


def movies_in_city(request, city_name):
    city_name = city_name.title()
    requested_city = City.objects.filter(name=city_name).first()
    if(requested_city):
        movies_in_requested_city = MovieTheatreShow.objects.filter(
            city=requested_city).values('movie_id').distinct()
        print(movies_in_requested_city)
        movies_list_json = []
        for movie_in_requested_city in movies_in_requested_city:
            movies = Movie.objects.filter(
                pk=movie_in_requested_city['movie_id'])
            for movie in movies:
                movies_list_json.append(MovieSerializer(movie).data)
        return JsonResponse(movies_list_json, safe=False)
    else:
        return JsonResponse({"message": "Currently %s is not registered in our cities" % city_name})
