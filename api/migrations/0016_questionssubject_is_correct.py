# Generated by Django 2.1.5 on 2019-02-21 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_auto_20190221_0950'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionssubject',
            name='is_correct',
            field=models.BooleanField(default=False),
        ),
    ]
