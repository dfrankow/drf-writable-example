# Generated by Django 2.2 on 2019-04-18 21:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0002_auto_20190418_2132'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='ExampleUser',
        ),
    ]