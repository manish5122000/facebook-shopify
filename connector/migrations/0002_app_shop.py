# Generated by Django 4.1.5 on 2023-03-29 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('connector', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='app_shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_id', models.IntegerField()),
                ('shop_name', models.CharField(max_length=99)),
                ('access_token', models.CharField(max_length=99)),
            ],
        ),
    ]
