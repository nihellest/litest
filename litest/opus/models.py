from django.db import models


class Author(models.Model):
    """Model of authors of writings"""
    name = models.CharField(max_length=64, verbose_name="Имя")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    death_date = models.DateField(null=True, blank=True, verbose_name="Дата смерти")

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"

    def __str__(self) -> str:
        return self.name


class Opus(models.Model):
    """Model of writings"""
    name = models.CharField(max_length=128, verbose_name="Название")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name="Автор")
    publish_date = models.DateField(null=True, blank=True, verbose_name="Дата публикации")

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"

    def __str__(self) -> str:
        return self.name
