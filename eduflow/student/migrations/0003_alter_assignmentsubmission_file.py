# Generated by Django 5.1.6 on 2025-03-05 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0002_assignmentsubmission'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignmentsubmission',
            name='file',
            field=models.FileField(null=True, upload_to='submissions/'),
        ),
    ]
