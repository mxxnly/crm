# Generated by Django 4.2.14 on 2025-07-07 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_alter_profile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_img',
            field=models.ImageField(default='avatars/prof.png', upload_to='avatars/'),
        ),
    ]
