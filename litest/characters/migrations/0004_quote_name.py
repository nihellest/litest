# Generated by Django 4.0.4 on 2022-05-26 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('characters', '0003_alter_character_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='quote',
            name='name',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
