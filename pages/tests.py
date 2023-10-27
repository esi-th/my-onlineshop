from django.test import TestCase
from django.shortcuts import reverse
from .forms import ContactUsFrom
from .models import Contact


class TestPages(TestCase):
    def test_home_page_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_page_view_by_url(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_contact_page_view(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)

    def test_contact_page_view_by_url(self):
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)

    def test_contact_form(self):
        data_form = {
            'first_name_last_name': 'esi jj',
            'phone_number': '09120000000',
            'email': 'jj@g.com',
            'contact_note': 'contact me',
        }
        form = ContactUsFrom(data_form)
        self.assertTrue(form.is_valid())

        response = self.client.post(reverse('contact'), data_form)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Contact.objects.all()[0].first_name_last_name, 'esi jj')
