# Generated by Django 2.1.5 on 2019-03-14 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0034_user_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(default=None, max_length=10, null=True),
        ),
    ]