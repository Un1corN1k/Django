from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm


class RegisterViewTest(TestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.valid_user_data = {
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }

    def test_register_view_get(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/register.html')
        self.assertIsInstance(response.context['form'], UserCreationForm)

    def test_register_view_post_success(self):
        response = self.client.post(self.register_url, data=self.valid_user_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

        self.assertEqual(User.objects.count(), 1)
        new_user = User.objects.first()
        self.assertEqual(new_user.username, 'testuser')

    def test_register_view_post_invalid_data(self):
        invalid_user_data = {
            'username': '',
            'password1': 'test123',
            'password2': 'test456',
        }
        response = self.client.post(self.register_url, data=invalid_user_data)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(User.objects.count(), 0)
