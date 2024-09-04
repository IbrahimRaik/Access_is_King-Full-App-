# Generated by Django 3.2.6 on 2024-09-04 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AccessIsKing', '0005_newcomments'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewMessages',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=24, unique=True)),
                ('new_message', models.CharField(blank=True, max_length=1024)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
