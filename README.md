# Moviebookz
API for a ticket booking system, where users can check the movies and book tickets

## With a **workflow pipeline** added for the project
check the stats from here
https://github.com/KrishnaManohar1997/moviebookz/runs/602961577?check_suite_focus=true

## Setting up the project
### Installing Django and other requirements
Python 3.6.9 is the version used for creating this project

Open the project folder
and install

```django``` and ```djangorestframework```
directly by using the following command

```
pip3 install -r requirements.txt
```

Creating the Django Project

```
django-admin startproject moviebookz
```

Move into the Project Directory
```cd moviebookz```

Creating necessary tables related to authentications,logentries and other tables

````
python manage.py migrate
````
Creating SuperUser(Admin) for the project
```
python manage.py createsuperuser
```

username -> cawstudio
password -> cawstudio
email -> cawstudio@admin.com

## Creating app and adding it to Django Project

```
python manage.py startapp api
```
This will create 'api' app folder in the project.

Now open moviebookz/settings.py
	Inside Installed Apps list add the created app named ```'api'``` and save the file, this will integrate the api app to the project.

Inside the api app, in models.py file we define Models that are needed for the application

Shows, Theatre, Movie, City

```
python manage.py makemigrations api
python manage.py migrate
```

To start the server use the following command

```
python manage.py runserver
```

## Endpoints

Movie Bookz API provides the following endpoints
```
base_url = http://127.0.0.1
base_url/api/login [POST] -> {username : username, password : password}
base_url/api/logout [GET] [PRIVATE]
base_url/api/registration [POST] -> {username : username, password : password, email : email}
base_url/api/movies [GET]
base_url/api/cities [GET]
base_url/api/movies/<city_name> [GET]
base_url/api/shows/<movie_name>/<city_name> [GET]
base_url/api/book/<city_name>/<movie_name>/<theatre_name>/<show_name> [GET]  [PRIVATE]
```
## Example -> Running Server and Hitting an Endpoint

```
python manage.py runserver
```

### Checking Shows for a movie in the City

http://127.0.0.1/api/shows/Avengers/Hyderabad

Sample Response
```
{
    "id": 1,
    "name": "Avengers",
    "rating": 8,
    "theatres": [
        {
            "id": 1,
            "name": "Inorbit",
            "city": 1,
            "shows": [
                {
                    "id": 1,
                    "name": "Matinee",
                    "start_time": "2020-04-20T12:19:50+05:30",
                    "end_time": "2020-04-20T12:19:50+05:30",
                    "total_seats": 10,
                    "available_seats": 6
                },
                {
                    "id": 2,
                    "name": "Morning",
                    "start_time": "2020-04-20T15:00:50+05:30",
                    "end_time": "2020-04-20T18:19:50+05:30",
                    "total_seats": 20,
                    "available_seats": 20
                }
            ]
        }
    ]
}
```

## Testing Django Unit-Tests
open the App directory, where manage.py exists and run the following command
to Fire the tests

```
python manage.py test
```

## My Sample work for Django Web application integrated with the API
![Django Movie Booking Demo](MovieBookz.gif)

## Added Logging to check invalid response or requests from Users
api.log file is being attached for that
Check that file, to understand how the logs are being stored
