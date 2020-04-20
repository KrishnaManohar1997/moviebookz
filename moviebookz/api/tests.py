from django.test import TestCase
from .models import Show, Movie
from django.test.utils import setup_test_environment
from django.test import Client
import json
from .serializer import MovieSerializer
from django.contrib.auth.models import User
from django.urls.base import reverse

class MoviesTest(TestCase):

    def setUp(self):
        Movie.objects.create(name="Avengers", rating=8)
        Movie.objects.create(name="Black Widow")

    def test_movie(self):
        client = Client()
        response = client.get('/api/movies')
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)
        response_avengers_movie = json_response['movies'][0]
        expected_data = MovieSerializer(
            Movie.objects.get(name='Avengers')).data
        self.assertEqual(str(response_avengers_movie), str(expected_data))

    def test_default_rating_movie(self):
        client = Client()
        response = client.get('/api/movies')
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)
        response_avengers_movie = json_response['movies'][1]['rating']
        expected_data = MovieSerializer(
            Movie.objects.get(name='Black Widow')).data['rating']
        self.assertEqual(str(response_avengers_movie), str(expected_data))


class LoginTest(TestCase):

    def setUp(self):
        self.credentials = {
            'username': 'billy',
            'password': 'billy',
            'email' : 'billy@mail.com'
            }
        User.objects.create_user(**self.credentials)

    def test_user_valid_login(self):
        # response = self.client.post('api/login', **self.credentials)
        user_data = {
            'username' : 'billy',
            'password' : 'billy'
        }
        response = self.client.post(reverse('api:login'), user_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(response.content)['status'],True)

    def test_user_invalid_login(self):
        user_data = {
            'username' : 'billy',
            'password' : 'qwerty'
        }
        response = self.client.post(reverse('api:login'), user_data, follow=True)
        self.assertEqual(response.status_code, 401)
        self.assertFalse(json.loads(response.content)['status'],False)