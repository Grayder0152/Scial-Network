from .models import Post

from django.test import TestCase
from django.contrib.auth.models import User


class NetworkTests(TestCase):

    @classmethod
    def setUp(cls):
        test_user = User.objects.create_user(
            username='Tom', password='abc123')
        test_user.save()

        test_post1 = Post.objects.create(
            author=test_user, title='Blog title', body='Body content')
        test_post2 = Post.objects.create(
            author=test_user, title='Blog title2', body='Body content2')
        test_post1.save()
        test_post2.save()

    def test_post_content(self):
        post = Post.objects.get(id=1)
        author = f'{post.author}'
        title = f'{post.title}'
        body = f'{post.body}'
        self.assertEqual(author, 'Tom')
        self.assertEqual(title, 'Blog title')
        self.assertEqual(body, 'Body content')

    def test_post_like(self):
        user = User.objects.get(username='Tom')
        post = Post.objects.get(id=1)
        post.liked_by.add(user)
        post.liked_by.add(user)
        self.assertEqual(1, post.liked_by.count())
