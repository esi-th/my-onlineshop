# Generated by Django 4.2.3 on 2023-10-19 09:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='Created Date')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('short_description', models.TextField(verbose_name='Product Description')),
                ('description', models.TextField(verbose_name='Product Short Description')),
                ('price', models.PositiveIntegerField(verbose_name='Price')),
                ('cover', models.ImageField(upload_to='covers/product_covers/', verbose_name='Product Cover')),
                ('active', models.BooleanField(default=True, verbose_name='Show Product')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='Created Date')),
                ('datetime_modified', models.DateTimeField(auto_now=True, verbose_name='Modified Date')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='products.category', verbose_name='Category')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.CharField(max_length=1000, verbose_name='Comment Text')),
                ('stars', models.CharField(choices=[('1', 'Very Bad'), ('2', 'Bad'), ('3', 'Normal'), ('4', 'Good'), ('5', 'Perfect')], max_length=10, verbose_name='Product Stars')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='Created Date')),
                ('datetime_modified', models.DateTimeField(auto_now=True, verbose_name='Modified Date')),
                ('active', models.BooleanField(default=True, verbose_name='Show Comment')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Comment Author')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product', verbose_name='Product')),
            ],
        ),
    ]
