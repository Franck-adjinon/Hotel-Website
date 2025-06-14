# Generated by Django 5.2 on 2025-05-07 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("nova", "0003_alter_plat_date_update"),
    ]

    operations = [
        migrations.AddField(
            model_name="chambre",
            name="type_chambre",
            field=models.CharField(
                choices=[
                    ("S", "Chambre Simple"),
                    ("F", "Chambre familiale"),
                    ("P", "Chambre Présidentielle"),
                ],
                default="S",
                max_length=1,
            ),
        ),
        migrations.AddField(
            model_name="plat",
            name="type_plat",
            field=models.CharField(
                choices=[
                    ("P", "Plats Principale"),
                    ("D", "Desserts"),
                    ("B", "Boissons"),
                ],
                default="P",
                max_length=1,
            ),
        ),
    ]
