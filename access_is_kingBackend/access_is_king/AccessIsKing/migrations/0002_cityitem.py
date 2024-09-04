# Generated by Django 3.2.6 on 2024-09-03 11:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AccessIsKing', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CityItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='AccessIsKing.city')),
            ],
        ),
    ]
