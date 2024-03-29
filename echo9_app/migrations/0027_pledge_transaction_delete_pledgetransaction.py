# Generated by Django 4.2.7 on 2024-01-16 03:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('echo9_app', '0026_alter_pledgetransaction_buyer_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pledge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('rejected', 'Rejected')], default='pending', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='echo9_app.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profit', models.DecimalField(decimal_places=2, max_digits=10)),
                ('transaction_date', models.DateTimeField(auto_now_add=True)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions_bought', to='echo9_app.userprofile')),
                ('pledge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='echo9_app.pledge')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions_sold', to='echo9_app.userprofile')),
            ],
        ),
        migrations.DeleteModel(
            name='PledgeTransaction',
        ),
    ]
