# Generated by Django 4.2.7 on 2024-01-13 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('echo9_app', '0017_remove_cointransaction_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cointransaction',
            name='buy_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]