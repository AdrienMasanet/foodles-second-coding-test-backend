# Generated by Django 4.0 on 2023-03-19 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0002_alter_client_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='session_token',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]