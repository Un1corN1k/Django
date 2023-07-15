from django.test import TestCase
from django.urls import reverse
from WEBSITE.post.models import BlogPost


class HomeViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse('home')

    def test_get_with_no_filters(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'post/home.html')
        self.assertContains(response, 'Blogs')

        # Перевірка, що всі пости доступні на сторінці
        blogs = response.context['blogs']
        self.assertEqual(blogs.count(), BlogPost.objects.count())

    def test_get_with_author_filter(self):
        author = 'John Doe'
        # Впишіть тут ім'я автора, для якого ви хочете протестувати фільтрацію

        response = self.client.get(self.url, {'authors': author})
        self.assertEqual(response.status_code, 200)

        blogs = response.context['blogs']
        for blog in blogs:
            self.assertEqual(blog.author, author)

    def test_get_with_search_query(self):
        search_query = 'python'
        # Впишіть тут пошуковий запит, для якого ви хочете протестувати фільтрацію

        response = self.client.get(self.url, {'search': search_query})
        self.assertEqual(response.status_code, 200)

        blogs = response.context['blogs']
        for blog in blogs:
            self.assertIn(search_query, blog.title.lower())
