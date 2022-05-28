from django.db import models
from characters.models import Quote, Character

class QuoteQuestion(models.Model):
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, verbose_name="Цитата")
    alt_answers = models.ManyToManyField(Character, verbose_name="Дополнительные ответы")

    class Meta:
        verbose_name = "Вопрос теста по цитатам"
        verbose_name_plural = "Вопросы теста по цитатам"

    @property
    def correct_answer(self) -> Character:
        return self.quote.source
    
    def is_correct(self, character: Character) -> bool:
        return character is self.correct_answer

