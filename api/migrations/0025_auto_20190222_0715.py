# Generated by Django 2.1.5 on 2019-02-22 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0024_auto_20190222_0528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='flag',
            field=models.IntegerField(default=True),
        ),
    ]