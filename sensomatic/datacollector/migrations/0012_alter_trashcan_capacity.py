# Generated by Django 5.0.4 on 2024-05-06 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacollector', '0011_alter_trashcan_mac_adress'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trashcan',
            name='capacity',
            field=models.IntegerField(null=True),
        ),
    ]
