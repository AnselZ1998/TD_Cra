# Generated by Django 3.2.25 on 2024-03-10 15:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CXS_db', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='fullname',
            new_name='full_name',
        ),
    ]
