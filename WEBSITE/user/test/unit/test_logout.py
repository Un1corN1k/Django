from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.test import TestCase
from django.urls import reverse


class LogoutViewTest(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.login_url = reverse('login')
        self.logout_url = reverse('logout_view')

    def test_logout_view(self):
        user = authenticate(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)
        self.assertTrue(user.is_authenticated)

        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)
