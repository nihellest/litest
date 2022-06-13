"""
Models module for writings app
"""

from django.db import models
from django.conf import settings

class Author(models.Model):
    """Model of authors of writings"""
    name = models.CharField(max_length=64, verbose_name="Имя")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    death_date = models.DateField(null=True, blank=True, verbose_name="Дата смерти")

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"

    def __str__(self) -> str:
        return str(self.name)


class Writing(models.Model):
    """Model of writings"""
    name = models.CharField(max_length=128, verbose_name="Название")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name="Автор")
    publish_date = models.DateField(null=True, blank=True, verbose_name="Дата публикации")

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"

    def __str__(self) -> str:
        return str(self.name)


class Character(models.Model):
    GENDERS = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    name = models.CharField(max_length=64, verbose_name="Имя")
    gender = models.CharField(choices=GENDERS, max_length=1, verbose_name="Пол")
    writing = models.ForeignKey(Writing, on_delete=models.CASCADE, verbose_name="Произведение")

    class Meta:
        verbose_name = "Персонаж"
        verbose_name_plural = "Персонажи"

    def __str__(self) -> str:
        return str(self.name)


class CharacterTag(models.Model):
    label = models.CharField(max_length=32, verbose_name="Метка")

    class Meta:
        verbose_name = "Тег персонажа"
        verbose_name_plural = "Теги персонажа"

    def __str__(self) -> str:
        return str(self.label)


class Quote(models.Model):
    """Model for a character's quotes"""
    name = models.CharField(max_length=128, null=True, blank=True, verbose_name="Название цитаты")
    source = models.ForeignKey(Character, on_delete=models.CASCADE, verbose_name="Источник цитаты")
    text = models.TextField(verbose_name="Текст")

    class Meta:
        verbose_name = "Цитата"
        verbose_name_plural = "Цитаты"

    @property
    def shorten(self) -> str:
        """Shorten text for a pretty quotes view in lists"""

        shorten_length = settings.APP_LONG_TEXT_SHORTEN_LENGTH
        words = str(self.text).split()
        return " ".join(words[:shorten_length]) + ("..." if len(words) > shorten_length else "")

    def __str__(self) -> str:
        name = self.name if self.name else self.shorten
        return f"({self.source.name}) {name}"
