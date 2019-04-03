# Generated by Django 2.1.5 on 2019-04-03 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0035_auto_20190314_0625'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserDevices',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('device_os', models.CharField(max_length=10)),
                ('push_key', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('flag', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'user_device',
            },
        ),
    ]