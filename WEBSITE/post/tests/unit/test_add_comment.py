from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from post.forms import CommentModelForm
from post.models import BlogPost, Comment


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