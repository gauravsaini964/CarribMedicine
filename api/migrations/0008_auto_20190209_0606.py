# Generated by Django 2.1.5 on 2019-02-09 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_authkey'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_phone_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='phone_no',
            field=models.IntegerField(null=True),
        ),
    ]