# Generated by Django 2.2 on 2019-04-09 20:40

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import personal.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('assignment_description', models.CharField(max_length=200)),
                ('optional_notes', models.CharField(blank=True, max_length=200, null=True)),
                ('acceptance_criteria', models.CharField(blank=True, max_length=200, null=True)),
                ('testing_criteria', models.CharField(blank=True, max_length=200, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('due_on', models.DateTimeField(null=True)),
            ],
            options={
                'ordering': ['course_id', 'due_on', 'title'],
            },
        ),
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_crn', models.IntegerField(unique=True, validators=[django.core.validators.MinValueValidator(1)], verbose_name='CRN')),
                ('course_title', models.CharField(max_length=50)),
                ('course_number', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('instructor_username', models.ForeignKey(limit_choices_to={'groups__name': 'Instructor'}, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, to_field='username')),
            ],
            options={
                'verbose_name': 'Course',
                'ordering': ['course_number'],
            },
        ),
        migrations.CreateModel(
            name='Takes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_level', models.CharField(choices=[('g', 'Grader'), ('s', 'Student'), ('i', 'Instructor')], default='s', max_length=1)),
                ('course_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='personal.Courses')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, to_field='username')),
            ],
            options={
                'verbose_name_plural': 'Takes',
                'ordering': ['course_id__course_number'],
            },
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submitted_on', models.DateTimeField(auto_now_add=True)),
                ('submission_number', models.IntegerField(default=1)),
                ('submitted_filename', models.CharField(blank=True, max_length=20, null=True)),
                ('assignment_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='personal.Assignment')),
                ('submitted_user', models.ForeignKey(limit_choices_to={'groups__name': 'Student'}, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, to_field='username')),
            ],
            options={
                'ordering': ['submitted_user', 'assignment_id', 'submitted_on'],
            },
        ),
        migrations.CreateModel(
            name='Invite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_level', models.CharField(choices=[('g', 'Grader'), ('s', 'Student'), ('i', 'Instructor')], default='s', max_length=1)),
                ('expires_on', models.DateField(default=personal.models.one_month_from_today)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('course_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='personal.Courses')),
                ('rec_username', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='receiver', to=settings.AUTH_USER_MODEL, to_field='username', verbose_name='to')),
                ('sender_username', models.ForeignKey(limit_choices_to={'groups__name': 'Instructor'}, on_delete=django.db.models.deletion.DO_NOTHING, related_name='sender', to=settings.AUTH_USER_MODEL, to_field='username', verbose_name='from')),
            ],
            options={
                'ordering': ['-expires_on', 'sender_username'],
            },
        ),
        migrations.AddField(
            model_name='assignment',
            name='course_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='personal.Courses'),
        ),
    ]
