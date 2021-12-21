# Generated by Django 3.2.9 on 2021-12-21 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_server', '0002_alter_search_csv_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goldbet_research', models.BooleanField(default=True)),
                ('bwin_research', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='ban_period',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='max_research',
            field=models.IntegerField(default=-1),
        ),
    ]
