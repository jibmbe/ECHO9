# Generated by Django 4.2.7 on 2024-01-13 22:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('echo9_app', '0016_echocoin_cointransaction'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cointransaction',
            name='user',
        ),
        migrations.AddField(
            model_name='cointransaction',
            name='user_profile',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='echo9_app.userprofile'),
        ),
    ]
