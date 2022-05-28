# Generated by Django 4.0.4 on 2022-05-27 16:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('characters', '0007_alter_character_opus_alter_charactertag_label_and_more'),
        ('tests', '0002_alter_quotequestion_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotequestion',
            name='alt_answers',
            field=models.ManyToManyField(to='characters.character', verbose_name='Дополнительные ответы'),
        ),
        migrations.AlterField(
            model_name='quotequestion',
            name='quote',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='characters.quote', verbose_name='Цитата'),
        ),
    ]
