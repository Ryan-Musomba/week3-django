# Generated by Django 5.2.2 on 2025-06-15 14:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialmediaapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['created']},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-created']},
        ),
        migrations.RemoveField(
            model_name='post',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='user',
            name='followers',
        ),
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='liked_posts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='post',
            name='text',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='post',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='picture',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.DeleteModel(
            name='Notification',
        ),
    ]
