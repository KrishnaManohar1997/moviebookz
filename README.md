# Moviebookz
API for a ticket booking system, where users can check the movies and book tickets

## Setting up the project
### Installing Django and other requirements

open the project folder
and install

```django``` and ```djangorestframework```



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