# Generated by Django 4.2.7 on 2024-01-12 02:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('echo9_app', '0002_userprofile_level_one_bonus_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='referral_link',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]
