from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.core.files.uploadedfile import SimpleUploadedFile
from django.shortcuts import reverse
from orders.models import Order, OrderItem
from products.models import Product, Category


class DashboardViewTest(TestCase):
    password = 'mypass'

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='esi1@g.com',
            password=cls.password,
            email='esi1@g.com',
        )
        cls.order = Order.objects.create(
            user=cls.user,
            price=10000,
            is_paid=False,
            order_status='processing',
            first_name='esi',
            last_name='jj',
            phone_number='09120000000',
            address='iran',
            order_note='quickly'
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
        cls.order_items = OrderItem.objects.create(
            order=cls.order,
            product=cls.product,
            quantity=1,
            price=cls.product.price,
        )

    def test_signup_page_view(self):
        response = self.client.get('/accounts/signup/')
        self.assertEqual(response.status_code, 200)

    def test_signup_page_view_by_name(self):
        response = self.client.get(reverse('account_signup'))
        self.assertEqual(response.status_code, 200)

    def test_signup_form(self):
        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(get_user_model().objects.all()[0].username, self.user.username)
        self.assertEqual(get_user_model().objects.all()[0].email, self.user.email)

    def test_login_page_view(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

    def test_login_page_view_by_name(self):
        response = self.client.get(reverse('account_login'))
        self.assertEqual(response.status_code, 200)

    def test_login_form(self):
        response = self.client.login(
            username=self.user.username,
            password=self.password,
        )
        self.assertTrue(response)

    def test_dashboard_view(self):
        self.client.login(
            username=self.user.username,
            password=self.password,
        )
        response = self.client.get(reverse('account_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_view_by_url(self):
        self.client.login(
            username=self.user.username,
            password=self.password,
        )
        response = self.client.get('/accounts/dashboard/')
        self.assertEqual(response.status_code, 200)

    def test_dashboard_orders_list_view(self):
        self.client.login(
            username=self.user.username,
            password=self.password,
        )
        response = self.client.get(reverse('account_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.order.order_status)

    def test_dashboard_password_change_form(self):
        self.client.login(
            username=self.user.username,
            password=self.password,
        )
        form_data = {
            'old_password': self.password,
            'new_password1': 'esi123456',
            'new_password2': 'esi123456',
        }
        form = PasswordChangeForm(self.user, form_data)
        self.assertTrue(form.is_valid())
        self.client.post(reverse('account_dashboard'), form_data)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('esi123456'))

    def test_dashboard_logout_view(self):
        self.client.login(
            username=self.user.username,
            password=self.password,
        )
        response = self.client.post(reverse('account_logout'))
        self.assertEqual(response.status_code, 302)

    def test_remove_and_add_to_wishlist_view(self):
        self.client.login(
            username=self.user.username,
            password=self.password,
        )
        self.client.get(reverse('wishlist_add', args=[self.product.id]))
        response = self.client.get(reverse('account_dashboard'))
        self.assertContains(response, self.product.title)
        self.client.get(reverse('wishlist_remove', args=[self.product.id]))
        response = self.client.get(reverse('account_dashboard'))
        self.assertNotContains(response, self.product.title)

    def test_dashboard_order_detail_view(self):
        self.client.login(
            username=self.user.username,
            password=self.password,
        )
        response = self.client.get(reverse('order_detail', args=[self.order.id]))
        self.assertContains(response, self.order_items.product.title)
        self.assertContains(response, self.order.order_status)
