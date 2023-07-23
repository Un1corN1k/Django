from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class LoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.home_url = reverse('home')
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_login_successful(self):
        response = self.client.post(self.login_url, {'username': self.username, 'password': self.password})
        self.assertRedirects(response, self.home_url)

    def test_login_failed_invalid_credentials(self):
        response = self.client.post(self.login_url, {'username': self.username, 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please enter a correct username and password.')

    def test_login_template_used(self):
        response = self.client.get(self.login_url)
        self.assertTemplateUsed(response, 'user/login.html')
