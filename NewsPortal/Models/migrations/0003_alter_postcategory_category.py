# Generated by Django 4.2.4 on 2023-11-14 16:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Models', '0002_subscriptions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postcategory',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='PostCategory', to='Models.category'),
        ),
    ]