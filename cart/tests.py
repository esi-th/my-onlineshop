from django.test import TestCase
from django.shortcuts import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from products.models import Product, Category
from .forms import AddToCartProductForm


class CartTest(TestCase):
    @classmethod
    def setUpTestData(cls):
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

    def test_cart_detail_view(self):
        response = self.client.get(reverse('cart:cart_detail'))
        self.assertEqual(response.status_code, 200)

    def test_cart_detail_view_template_name(self):
        response = self.client.get(reverse('cart:cart_detail'))
        self.assertTemplateUsed(response, 'cart/cart_detail.html')

    def test_cart_detail_view_by_url(self):
        response = self.client.get('/cart/')
        self.assertEqual(response.status_code, 200)

    def test_add_update_remove_cart_view(self):
        # add product to cart
        form_data = {
            'quantity': 1
        }
        response = self.client.post(reverse('cart:cart_add', args=[self.product.id]), form_data)
        self.assertEqual(response.status_code, 302)

        self.client.session.modified = True
        self.assertEqual(self.client.session['cart'][str(self.product.id)]['quantity'], 1)

        # update product quantity
        form_data = {
            'quantity': 2,
            'inplace': True,
        }
        response = self.client.post(reverse('cart:cart_add', args=[self.product.id]), form_data)
        self.assertEqual(response.status_code, 302)

        self.client.session.modified = True
        self.assertEqual(self.client.session['cart'][str(self.product.id)]['quantity'], 2)

        # remove product form cart
        response = self.client.post(reverse('cart:cart_remove', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)
        self.client.session.modified = True
        response = self.client.get(reverse('cart:cart_detail'))
        self.assertNotContains(response, self.product.title)

    def test_cart_clear_view(self):
        form_data = {
            'quantity': 1
        }
        response = self.client.post(reverse('cart:cart_add', args=[self.product.id]), form_data)
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('cart:cart_detail'))
        self.assertContains(response, self.product.title)

        response = self.client.get(reverse('cart:cart_clear'))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('cart:cart_detail'))
        self.assertNotContains(response, self.product.title)
