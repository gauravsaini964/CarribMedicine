# Generated by Django 2.1.5 on 2019-02-22 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_auto_20190222_0422'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questionssubject',
            name='is_correct',
        ),
        migrations.AddField(
            model_name='questionschoices',
            name='is_correct',
            field=models.BooleanField(default=False),
        ),
    ]