# Generated by Django 3.2.18 on 2023-02-15 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField(max_length=500)),
                ('status', models.CharField(blank=True, choices=[('New', 'New'), ('Replied', 'Replied')], default='New', max_length=100)),
            ],
            options={
                'verbose_name': 'Visitor Message',
            },
        ),
    ]