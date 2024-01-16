# Generated by Django 4.2.7 on 2024-01-13 01:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('echo9_app', '0013_alter_referral_referred_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investment',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('rejected', 'Rejected')], default='pending', max_length=20),
        ),
        migrations.AlterField(
            model_name='referral',
            name='referred_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='referrals_received', to='echo9_app.userprofile'),
        ),
        migrations.AlterField(
            model_name='referral',
            name='referring_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='referrals_given', to='echo9_app.userprofile'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='inviter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='invited_users', to='echo9_app.userprofile'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='referred_users',
            field=models.ManyToManyField(blank=True, related_name='referring_users', to='echo9_app.userprofile'),
        ),
    ]