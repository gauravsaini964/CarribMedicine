# Generated by Django 2.1.5 on 2019-02-09 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_auto_20190209_0717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_no',
            field=models.CharField(max_length=20, null=True, unique=True),
        ),
    ]