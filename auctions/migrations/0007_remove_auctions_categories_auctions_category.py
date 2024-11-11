# Generated by Django 4.1.4 on 2023-01-25 23:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_categories_auctions_categories'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auctions',
            name='categories',
        ),
        migrations.AddField(
            model_name='auctions',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='auctions', to='auctions.categories'),
        ),
    ]