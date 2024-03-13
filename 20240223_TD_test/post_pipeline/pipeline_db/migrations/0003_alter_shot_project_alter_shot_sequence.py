# Generated by Django 5.0.2 on 2024-02-28 09:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pipeline_db', '0002_rename_fullname_project_full_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shot',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='shots', to='pipeline_db.project'),
        ),
        migrations.AlterField(
            model_name='shot',
            name='sequence',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='shots', to='pipeline_db.sequence'),
        ),
    ]