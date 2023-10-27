from django.test import TestCase
from .models import Category, Comment, Product
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from .forms import NewCommentForm


class ProductTest(TestCase):
    password = 'mypassword'

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='esi1@g.com',
            password=cls.password,
            email='esi1@g.com',
        )
        cls.category = Category.objects.create(
            name='game console',
        )
        image = SimpleUploadedFile(
            "example.jpg",
            b"file_content",
        )
        cls.product = Product.objects.create(
            title='product1',
            short_description='product desc',
            description='product description',
            price=10000,
            category=cls.category,
            cover=image,
            active=True,
        )

    def test_product_list_view(self):
        response = self.client.get(reverse('products_list'))
        self.assertEqual(response.status_code, 200)

    def test_product_list_view_by_url(self):
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)

    def test_product_show(self):
        response = self.client.get(reverse('products_list'))
        self.assertContains(response, self.product.title)

    def test_product_detail_view(self):
        response = self.client.get(reverse('product_detail', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)

    def test_product_not_found(self):
        response = self.client.get(reverse('product_detail', args=[self.product.id+10]))
        self.assertEqual(response.status_code, 404)

    def test_comment_create_form(self):
        self.client.login(
            username=self.user.username,
            password=self.password,
        )
        form_data = {
            'body': 'hello from esi',
            'stars': '1',
        }
        form = NewCommentForm(form_data)
        self.assertTrue(form.is_valid())
        self.client.post(reverse('comment_create', args=[self.product.id]), form_data)
        response = self.client.get(reverse('product_detail', args=[self.product.id]))
        self.assertContains(response, self.product.id)
        self.assertEqual(Comment.objects.all()[0].body, 'hello from esi')
        self.assertEqual(Comment.objects.all().count(), 1)

    def test_search_form(self):
        form_data = {
            'searched': self.product.title,
        }
        response = self.client.post(reverse('product_search'), form_data)
        self.assertEqual(response.status_code, 200)
