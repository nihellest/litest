from django.db import models
from opus.models import Opus


class Character(models.Model):
    GENDERS = (
        ('М', 'Мужчина'),
        ('Ж', 'Женщина'),
    )
    name = models.CharField(max_length=64)
    gender = models.CharField(choices=GENDERS, max_length=1)
    opus = models.ForeignKey(Opus, on_delete=models.CASCADE)


class CharacterTag(models.Model):
    label = models.CharField(max_length=32)


class Quote(models.Model):
    source = models.ForeignKey(Character, on_delete=models.CASCADE)
    text = models.TextField()
