# Generated by Django 4.1.5 on 2023-04-02 15:56

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('connector', '0003_remove_app_shop_id_alter_app_shop__id'),
    ]

    operations = [
        migrations.CreateModel(
            name='user_details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(max_length=99)),
                ('shop_name', models.CharField(max_length=99)),
                ('marketplace', jsonfield.fields.JSONField()),
            ],
        ),
    ]
