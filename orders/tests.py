from django.test import TestCase
from products.models import Product, Category
from django.core.files.uploadedfile import SimpleUploadedFile
from .forms import OrderForm
from .models import Order, OrderItem
from django.shortcuts import reverse
from django.contrib.auth import get_user_model


class OrderTest(TestCase):
    password = 'mypass'

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

    def test_create_order_view(self):
        self.client.login(
            username=self.user.username,
            password=self.password,
        )
        response = self.client.get(reverse('account_dashboard'))
        self.assertEqual(response.status_code, 200)

        form_data = {
            'quantity': 1
        }
        self.client.post(reverse('cart:cart_add', args=[self.product.id]), form_data)
        self.client.session.modified = True

        response = self.client.get(reverse('orders:create_order'))
        self.assertEqual(response.status_code, 200)

        form_data = {
            'first_name': 'esi',
            'last_name': 'jj',
            'phone_number': '09120000000',
            'address': 'iran',
            'order_note': 'hi',
        }

        form = OrderForm(form_data)
        self.assertTrue(form.is_valid())
        response = self.client.post(reverse('orders:create_order'), form_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Order.objects.all().count(), 1)
        self.assertEqual(Order.objects.all()[0].last_name, 'jj')
        self.assertEqual(OrderItem.objects.all()[0].product.title, self.product.title)
