# Generated by Django 5.0.3 on 2024-04-03 10:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datacollector', '0002_trashisland_latitude_trashisland_longitude'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sensordata',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='trashcan',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='trashisland',
            options={'ordering': ['-created_at']},
        ),
    ]