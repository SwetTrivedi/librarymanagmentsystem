# Generated by Django 5.1.6 on 2025-03-10 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0009_remove_favourite_favbook_alter_favourite_book'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='book_cate',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='publish_year',
            field=models.DateField(blank=True, null=True),
        ),
    ]
