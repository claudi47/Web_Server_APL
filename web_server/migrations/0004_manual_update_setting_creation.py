from django.db import migrations, models


def create_settings(apps, _):
    settings = apps.get_model("web_server", "Settings")
    settings.objects.create(goldbet_research=True, bwin_research=True)

class Migration(migrations.Migration):

    dependencies = [
        ('web_server', '0003_auto_20211221_1254')
    ]

    operations = [
        migrations.RunPython(create_settings)
    ]
