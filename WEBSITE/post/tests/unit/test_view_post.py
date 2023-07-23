from django.test import TestCase, Client
from django.urls import reverse
from post.models import BlogPost



class ViewPostViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.post = BlogPost.objects.create(
            title='Test Post',
            content='This is a test post.',
            slug='test-post'
        )
        self.url = reverse('view_post', args=[self.post.slug])

    def test_get_existing_post(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'post/view_post.html')
        self.assertEqual(response.context['post'], self.post)

    def test_get_nonexistent_post(self):
        non_existent_slug = 'non-existent-post'
        url = reverse('view_post', args=[non_existent_slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)