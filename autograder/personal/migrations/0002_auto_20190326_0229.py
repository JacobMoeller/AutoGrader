# Generated by Django 2.1.7 on 2019-03-26 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courses',
            name='course_crn',
            field=models.IntegerField(unique=True, verbose_name='CRN'),
        ),
        migrations.AlterField(
            model_name='invite',
            name='level_of_invite',
            field=models.CharField(choices=[('g', 'Grader'), ('s', 'Student'), ('i', 'Instructor')], default='s', max_length=1),
        ),
    ]
