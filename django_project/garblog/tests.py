from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import User, Post, Comment
from .serializers import UserSerializer, PostSerializer, CommentSerializer

class UserViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_user(self):
        url = reverse('register')
        data = {'username': 'testuser', 'password': 'testpassword', 'email': 'test@example.com'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')

class LoginViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_login(self):
        url = reverse('login')
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)

class PostViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='john', password='P@ssword1')
        self.client.force_authenticate(user=self.user)

    def test_create_post(self):
        url = reverse('post-list')
        data = {'title': 'My Blog', 'story': 'This is a test post.'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get().title, 'My Blog')

class BlogViewTestCase(TestCase):
    def setUp(self):
        Post.objects.create(title = 'Post 1', content = 'Test Content 1')
        Post.objects.create(title = 'Post 2', content = 'Test content 2')
    
    def test_blog_list_view(self):
        response = self.client.get(reverse('post-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertContains(response, 'Post 1')
        self.assertContains(response, 'Post 2')

class PostFormTestCase(TestCase):
    def test_valid_post_form(self):
        form_data = {'title':'Test Title', 'content':'Test Content'}
        form = PostForm(data=form_data)
        self.assertTrue(form.is_valid())
    
class UserPermissionsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username = 'john', password = 'P@ssword1')
        self.post = Post.objects.create(title = 'Test Post', content = 'Test content', author = self.user)

        def test_post_author_access(self):
            self.client.login(username = 'john', password = 'P@ssword1')
            response = self.client.get('/blog/post/{}/edit/'.form(self.post.id))
            self.assertEqual(response.status_code, 200)
        
        def test_non_author_access(self):
            new_user = User.objects.create_user(username = 'doe', password = 'P@ssword1')
            response = self.client.get('/blog/post/{}/edit/'.form(self.post.id))
            self.assertEqual(response.status_code, 403)
        
    