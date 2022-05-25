from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=64)
    birth_date = models.DateField(blank=True)
    death_date = models.DateField(blank=True)


class Opus(models.Model):
    """Художественное произведение"""
    name = models.CharField(max_length=128)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    publish_date = models.DateField(blank=True)
