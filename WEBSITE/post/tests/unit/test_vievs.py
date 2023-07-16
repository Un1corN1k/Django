from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from post.models import BlogPost, Comment
from post.forms import CommentModelForm, PostModelForm



class HomeViewTest(TestCase):
    def setUp(self):
        self.url = reverse('home')  # Впишіть сюди URL для в'юхи home

    def test_get_with_author_filter(self):
        author = 'John Doe'  # Впишіть тут ім'я автора, для якого ви хочете протестувати фільтрацію
        response = self.client.get(self.url, {'authors': author})
        self.assertEqual(response.status_code, 200)

        blogs = response.context['blogs']
        for blog in blogs:
            self.assertEqual(blog.author, author)

    def test_get_with_search_query(self):
        search_query = 'python'  # Впишіть тут пошуковий запит, для якого ви хочете протестувати фільтрацію
        response = self.client.get(self.url, {'search': search_query})
        self.assertEqual(response.status_code, 200)

        blogs = response.context['blogs']
        for blog in blogs:
            self.assertIn(search_query, blog.title.lower())

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


class AddCommentViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.blog = BlogPost.objects.create(
            title='Test Blog',
            content='This is a test blog.',
            slug='test-blog'
        )
        self.url = reverse('add_comment', args=[self.blog.slug])
        self.form_data = {
            'author': self.user.id,
            'content': 'This is a test comment.'
        }

    def test_get_add_comment_page(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'post/add_comment.html')
        self.assertIsInstance(response.context['form'], CommentModelForm)
        self.assertEqual(response.context['blog'], self.blog)

    def test_post_valid_comment(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.url, data=self.form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('view_post', args=[self.blog.slug]))

        comment = Comment.objects.last()
        self.assertEqual(comment.author, self.user)
        self.assertEqual(comment.blog, self.blog)
        self.assertEqual(comment.content, 'This is a test comment.')

    def test_post_invalid_comment(self):
        self.client.login(username='testuser', password='testpassword')
        invalid_form_data = {
            'author': self.user.id,
            'content': ''
        }
        response = self.client.post(self.url, data=invalid_form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'post/add_comment.html')
        self.assertIsInstance(response.context['form'], CommentModelForm)
        self.assertEqual(response.context['blog'], self.blog)
        self.assertContains(response, 'This field is required.')


class CreatePostViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.url = reverse('create_post')
        self.login_url = reverse('user:login')

    def test_get_create_post_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'post/create_post.html')
        self.assertIsInstance(response.context['form'], PostModelForm)

    def test_get_create_post_view_unauthenticated(self):
        response = self.client.get(self.url)

        self.assertRedirects(response, f"{self.login_url}?next={self.url}")

    def test_post_create_post_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        form_data = {
            'title': 'Test Post',
            'topic': 'Test Topic',
            'content': 'This is a test post content.'
        }
        response = self.client.post(self.url, data=form_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.success_url)

        # Check if the post is created in the database
        post = BlogPost.objects.filter(title='Test Post', author=self.user).first()
        self.assertIsNotNone(post)
        self.assertEqual(post.topic, 'Test Topic')
        self.assertEqual(post.content, 'This is a test post content.')

    def test_post_create_post_view_unauthenticated(self):
        form_data = {
            'title': 'Test Post',
            'topic': 'Test Topic',
            'content': 'This is a test post content.'
        }
        response = self.client.post(self.url, data=form_data)

        self.assertRedirects(response, f"{self.login_url}?next={self.url}")

        # Check if the post is not created in the database
        post = BlogPost.objects.filter(title='Test Post', author=self.user).first()
        self.assertIsNone(post)
