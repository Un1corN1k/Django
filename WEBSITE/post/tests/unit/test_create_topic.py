from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from post.models import Topic
from post.forms import TopicModelForm


class CreateTopicViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.login_url = reverse('login')
        self.create_topic_url = reverse('create_topic')

    def test_create_topic_view_returns_form_if_user_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.create_topic_url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], TopicModelForm)

    def test_create_topic_view_creates_topic_and_redirects_to_home_on_form_submission(self):
        self.client.login(username='testuser', password='testpassword')
        data = {
            'topic': 'Test Topic',
            'description': 'This is a test topic.',
        }
        response = self.client.post(self.create_topic_url, data=data)
        self.assertRedirects(response, reverse('home'))
        self.assertEqual(Topic.objects.count(), 1)
        new_topic = Topic.objects.first()
        self.assertEqual(new_topic.topic, 'Test Topic')
        self.assertEqual(new_topic.description, 'This is a test topic.')
        self.assertEqual(new_topic.author, self.user)
