# Generated by Django 2.1.5 on 2019-03-02 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0032_user_is_logged_in'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(max_length=254, null=True, unique=True),
        ),
    ]
