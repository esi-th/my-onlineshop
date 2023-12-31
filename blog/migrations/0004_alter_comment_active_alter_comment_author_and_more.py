# Generated by Django 4.2.3 on 2023-10-15 12:04

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0003_remove_post_active_post_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='active',
            field=models.BooleanField(default=True, verbose_name='وضعیت کامنت'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='نویسنده نظر'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='body',
            field=models.TextField(verbose_name='متن نظر'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='datetime_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد پست'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='datetime_modified',
            field=models.DateTimeField(auto_now=True, verbose_name='تاریخ تغییر پست'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='blog.post', verbose_name='پست'),
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='نویسنده پست'),
        ),
        migrations.AlterField(
            model_name='post',
            name='cover',
            field=models.ImageField(blank=True, upload_to='post_covers/', verbose_name='کاور پست'),
        ),
        migrations.AlterField(
            model_name='post',
            name='datetime_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد پست'),
        ),
        migrations.AlterField(
            model_name='post',
            name='datetime_modified',
            field=models.DateTimeField(auto_now=True, verbose_name='تاریخ تغییر پست'),
        ),
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.CharField(blank=True, choices=[('pub', 'منتشر شده'), ('drf', 'پیش نویس')], max_length=3, verbose_name='وضعیت پست'),
        ),
        migrations.AlterField(
            model_name='post',
            name='text',
            field=ckeditor.fields.RichTextField(verbose_name='توضیحات پست'),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=250, verbose_name='عنوان پست'),
        ),
    ]
