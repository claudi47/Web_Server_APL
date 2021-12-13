# Generated by Django 3.2.9 on 2021-12-12 09:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('username', models.CharField(max_length=127)),
                ('user_identifier', models.CharField(max_length=127, primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Search',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('csv_url', models.URLField(blank=True, max_length=255)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='searches', to='web_server.user')),
            ],
        ),
        migrations.CreateModel(
            name='BetData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=127)),
                ('match', models.CharField(max_length=127)),
                ('one', models.CharField(max_length=127)),
                ('ics', models.CharField(max_length=127)),
                ('two', models.CharField(max_length=127)),
                ('gol', models.CharField(max_length=127)),
                ('over', models.CharField(max_length=127)),
                ('under', models.CharField(max_length=127)),
                ('web_site', models.CharField(max_length=127)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('search', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bet_data', to='web_server.search')),
            ],
        ),
    ]
