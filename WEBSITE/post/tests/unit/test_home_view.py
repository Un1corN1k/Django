from django.test import TestCase
from django.urls import reverse


class HomeViewTest(TestCase):
    def setUp(self):
        self.url = reverse('home')

    def test_get_with_author_filter(self):
        author = 'John Doe'
        response = self.client.get(self.url, {'authors': author})
        self.assertEqual(response.status_code, 200)

        blogs = response.context['blogs']
        for blog in blogs:
            self.assertEqual(blog.author, author)

    def test_get_with_search_query(self):
        search_query = 'python'
        response = self.client.get(self.url, {'search': search_query})
        self.assertEqual(response.status_code, 200)

        blogs = response.context['blogs']
        for blog in blogs:
            self.assertIn(search_query, blog.title.lower())
