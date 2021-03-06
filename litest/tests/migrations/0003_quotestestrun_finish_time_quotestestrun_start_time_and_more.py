# Generated by Django 4.0.4 on 2022-06-15 13:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tests', '0002_quotequestionrecord_quotestestrun'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotestestrun',
            name='finish_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='quotestestrun',
            name='start_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quotestestrun',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='quotestestrun',
            name='questions',
            field=models.ManyToManyField(blank=True, null=True, to='tests.quotequestionrecord'),
        ),
    ]
