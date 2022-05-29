from django.db import models
from characters.models import Quote, Character
from random import shuffle
import logging

logger = logging.getLogger(__name__)


class QuoteQuestion(models.Model):
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, verbose_name="Цитата")
    alt_answers = models.ManyToManyField(Character, verbose_name="Дополнительные ответы")

    class Meta:
        verbose_name = "Вопрос теста по цитатам"
        verbose_name_plural = "Вопросы теста по цитатам"

    @property
    def get_answers(self):
        characters = list(self.alt_answers.all())
        characters.append(self.correct_answer)
        answers = [(character.id, character.name) for character in characters]
        shuffle(answers)
        return answers

    @property
    def correct_answer(self) -> Character:
        return self.quote.source
    
    def is_correct(self, character: Character) -> bool:
        return character is self.correct_answer
