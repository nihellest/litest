"""
Models module for tests app
"""

import logging
from random import shuffle
from typing import Union, Tuple

from django.db import models
from writings.models import Quote, Character

logger = logging.getLogger(__name__)


class QuoteQuestion(models.Model):
    """Model for quotes test's question"""

    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, verbose_name="Цитата")
    alt_answers = models.ManyToManyField(Character, verbose_name="Дополнительные ответы")

    class Meta:
        verbose_name = "Вопрос теста по цитатам"
        verbose_name_plural = "Вопросы теста по цитатам"

    def __str__(self) -> str:
        return str(self.quote)

    @property
    def text(self):
        return self.quote.text

    @property
    def as_dict(self):
        """Return dictionary optimized for question's views"""
        return {
            'question_id': self.pk,
            'text': self.text,
            'answers': self.get_answers,
        }

    @property
    def get_answers(self) -> Tuple[int, str]:
        """
        Return question's answers as two-tuple

        Format: `(id: int, label: str)`
        """
        characters = list(self.alt_answers.all())
        characters.append(self.correct_answer)
        answers = [(character.id, character.name) for character in characters]
        shuffle(answers)
        return answers

    @property
    def correct_answer(self) -> Character:
        return self.quote.source

    def is_correct(self, character: Union[Character, int]) -> bool:
        """Take id or object of answer & return boolean of answer correctnesse"""
        if isinstance(character, int):
            return character == self.correct_answer.id
        if isinstance(character, Character):
            return character is self.correct_answer
        raise TypeError(f"Character can be an object or an object id, not {type(character)}")

    # TODO: validate that correct answer don't present in alter answers
    # def save(self, *args, **kwargs):
    #     if self.correct_answer in list(self.alt_answers.all()):
    #         raise ValidationError("Correct answer can't be added as alternative answer")
    #     super().save(*args, **kwargs)
