from django.db import models
from django.forms import ValidationError
from characters.models import Quote, Character
from random import shuffle
from typing import Union
import logging

logger = logging.getLogger(__name__)


class QuoteQuestion(models.Model):
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, verbose_name="Цитата")
    alt_answers = models.ManyToManyField(Character, verbose_name="Дополнительные ответы")

    class Meta:
        verbose_name = "Вопрос теста по цитатам"
        verbose_name_plural = "Вопросы теста по цитатам"

    def __str__(self) -> str:
        return str(self.quote)

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
    
    def is_correct(self, character: Union[Character, int]) -> bool:
        if isinstance(character, int):
            return character == self.correct_answer.id
        if isinstance(character, Character):
            return character is self.correct_answer
        else:
            raise TypeError(f"Character can be an object or an object id, not {type(character)}")
    
    # TODO: validate that correct answer don't present in alter answers
    # def save(self, *args, **kwargs):
    #     if self.correct_answer in list(self.alt_answers.all()):
    #         raise ValidationError("Correct answer can't be added as alternative answer")
    #     super().save(*args, **kwargs)