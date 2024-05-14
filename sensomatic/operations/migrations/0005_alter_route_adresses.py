from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0004_remove_route_route_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='route',
            name='adresses',
            field=models.TextField(),
        ),
    ]
