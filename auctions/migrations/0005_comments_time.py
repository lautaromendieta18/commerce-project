# Generated by Django 4.1.4 on 2022-12-29 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='time',
            field=models.DateTimeField(null=True),
        ),
    ]
