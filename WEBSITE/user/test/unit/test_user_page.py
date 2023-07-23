from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from user.models import UserProfile


class UserPageViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = 'testuser'
        self.password = 'testpass'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.user_profile = UserProfile.objects.create(user=self.user)

    def test_user_page_view_for_authenticated_user(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('user_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/user_page.html')
        self.assertEqual(response.context['user_page'], self.user_profile)
        self.assertContains(response, self.username)
        self.assertContains(response, self.user_profile.user.username)
