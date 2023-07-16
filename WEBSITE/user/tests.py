from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.test import TestCase, Client
from django.urls import reverse


class LoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_get_login_page(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/login.html')
        self.assertIsInstance(response.context['form'], AuthenticationForm)

    def test_login_with_valid_credentials(self):
        response = self.client.post(self.login_url, {'username': self.username, 'password': self.password})
        self.assertRedirects(response, '/')
        self.assertTrue('_auth_user_id' in self.client.session)
        self.assertEqual(int(self.client.session['_auth_user_id']), self.user.id)

    def test_login_with_invalid_credentials(self):
        response = self.client.post(self.login_url, {'username': 'invaliduser', 'password': 'invalidpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/login.html')
        self.assertIsInstance(response.context['form'], AuthenticationForm)
        self.assertContains(response, 'Please enter a correct username and password.')

    def test_login_form_submission(self):
        form_data = {'username': self.username, 'password': self.password}
        form = AuthenticationForm(None, data=form_data)
        self.assertTrue(form.is_valid())
        user = form.get_user()
        self.assertEqual(user.username, self.username)
        self.assertEqual(user.check_password(self.password), True)

