# Generated by Django 4.0.4 on 2022-05-18 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='avatar.svg', null=True, upload_to=''),
        ),
    ]
