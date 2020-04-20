from django.db import models
from django.utils.datetime_safe import datetime


class City(models.Model):
    name = models.CharField(max_length=20, unique=True)


class Show(models.Model):
    name = models.CharField(max_length=20, unique=True)
    start_time = models.DateTimeField(default=datetime.now, blank=False)
    end_time = models.DateTimeField(default=datetime.now, blank=False)
    total_seats = models.IntegerField(default=20)
    available_seats = models.IntegerField(default=20)


class Theatre(models.Model):
    name = models.CharField(max_length=20, unique=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)


class Movie(models.Model):
    name = models.CharField(max_length=20, unique=True)
    rating = models.IntegerField(default=7)


class MovieTheatreShow(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    theatre = models.ForeignKey(Theatre, on_delete=models.CASCADE)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
