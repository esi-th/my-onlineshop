from django.test import TestCase
from accounts.models import CustomUser
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Post
from django.shortcuts import reverse


class PostTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = CustomUser.objects.create(
            username='esi',
            password='your_password',
        )
        image = SimpleUploadedFile(
            "example.jpg",
            b"file_content",
        )
        cls.post1 = Post.objects.create(
            author=user,
            title='post1',
            text='abc',
            status='pub',
            cover=image,
        )
        cls.post2 = Post.objects.create(
            author=user,
            title='post2',
            text='xyz',
            status='drf',
            cover=image,
        )

    def test_blog_page_url_by_url(self):
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)

    def test_blog_page_url_by_name(self):
        response = self.client.get(reverse('posts_list'))
        self.assertEqual(response.status_code, 200)

    def test_post_title_text_author(self):
        response = self.client.get(reverse('posts_list'))
        self.assertContains(response, self.post1.title)
        self.assertContains(response, self.post1.author)
        self.assertContains(response, self.post1.text)

    def test_post_not_found_404(self):
        response = self.client.get(reverse('post_detail', args=[self.post1.id+100]))
        self.assertEqual(response.status_code, 404)

    def test_post_detail_page(self):
        response = self.client.get(reverse('post_detail', args=[self.post1.id]))
        self.assertEqual(response.status_code, 200)

    def test_post_detail_page_by_url(self):
        response = self.client.get(f'/blog/{self.post1.id}/')
        self.assertEqual(response.status_code, 200)

    def test_posts_status(self):
        response = self.client.get(reverse('posts_list'))
        self.assertContains(response, self.post1.text)
        self.assertNotContains(response, self.post2.text)

    def test_post_detail_title_text_author(self):
        response = self.client.get(reverse('post_detail', args=[self.post1.id]))
        self.assertContains(response, self.post1.title)
        self.assertContains(response, self.post1.author)
        self.assertContains(response, self.post1.text)

    def test_post_model_str(self):
        post = self.post1
        self.assertEqual(str(post), post.title)

    def test_post_detail(self):
        self.assertEqual(self.post1.title, 'post1')
        self.assertEqual(self.post1.text, 'abc')
