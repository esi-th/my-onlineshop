# Generated by Django 4.2.3 on 2023-10-20 12:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0002_alter_comment_author_alter_comment_product_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_paid', models.BooleanField(default=False, verbose_name='Paid?')),
                ('first_name', models.CharField(max_length=100, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=100, verbose_name='Last Name')),
                ('phone_number', models.CharField(max_length=13, verbose_name='Phone Number')),
                ('address', models.CharField(max_length=500, verbose_name='Address')),
                ('order_note', models.CharField(blank=True, max_length=500, verbose_name='Order Note')),
                ('zarinpal_authority', models.CharField(blank=True, max_length=255, verbose_name='Zarinpal Authority')),
                ('zarinpal_ref_id', models.CharField(blank=True, max_length=150, verbose_name='Zarinpal Ref ID')),
                ('zarinpal_text', models.TextField(blank=True, max_length=700, verbose_name='Zarinpal Response Data')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='Date Created')),
                ('datetime_modified', models.DateTimeField(auto_now=True, verbose_name='Date Modified')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Quantity')),
                ('price', models.PositiveIntegerField(verbose_name='Price')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='Date Created')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='orders.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='products.product', verbose_name='Order Items')),
            ],
        ),
    ]
