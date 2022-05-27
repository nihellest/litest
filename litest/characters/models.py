from django.db import models
from opus.models import Opus


class Character(models.Model):
    GENDERS = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    name = models.CharField(max_length=64, verbose_name="Имя")
    gender = models.CharField(choices=GENDERS, max_length=1, verbose_name="Пол")
    opus = models.ForeignKey(Opus, on_delete=models.CASCADE, verbose_name="Произведение")

    class Meta:
        verbose_name = "Персонаж"
        verbose_name_plural = "Персонажи"

    def __str__(self) -> str:
        return self.name


class CharacterTag(models.Model):
    label = models.CharField(max_length=32, verbose_name="Метка")

    class Meta:
        verbose_name = "Тег персонажа"
        verbose_name_plural = "Теги персонажа"

    def __str__(self) -> str:
        return self.label


class Quote(models.Model):
    name = models.CharField(max_length=128, null=True, blank=True, verbose_name="Название цитаты")
    source = models.ForeignKey(Character, on_delete=models.CASCADE, verbose_name="Источник цитаты")
    text = models.TextField(verbose_name="Текст")

    class Meta:
        verbose_name = "Цитата"
        verbose_name_plural = "Цитаты"
    
    def __str__(self) -> str:
        return self.name if self.name else self.text
