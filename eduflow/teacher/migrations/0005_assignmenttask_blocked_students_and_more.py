# Generated by Django 5.1.6 on 2025-03-10 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0003_alter_assignmentsubmission_file'),
        ('teacher', '0004_alter_assignmenttask_submission_deadline'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignmenttask',
            name='blocked_students',
            field=models.ManyToManyField(related_name='blocked_tasks', to='student.studentprofile'),
        ),
        migrations.AlterField(
            model_name='assignmenttask',
            name='students',
            field=models.ManyToManyField(related_name='assigned_tasks', to='student.studentprofile'),
        ),
    ]
