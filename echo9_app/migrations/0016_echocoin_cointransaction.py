# Generated by Django 4.2.7 on 2024-01-13 21:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('echo9_app', '0015_alter_userprofile_referred_users'),
    ]

    operations = [
        migrations.CreateModel(
            name='EchoCoin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('symbol', models.CharField(max_length=10)),
                ('current_price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='CoinTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('transaction_type', models.CharField(max_length=10)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('coin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='echo9_app.echocoin')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]