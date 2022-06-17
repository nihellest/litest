"""
Models module for tests app
"""

import logging
from random import shuffle, sample
from typing import Any, Dict, Union, Tuple

from django.db import models
from django.contrib.auth.models import User
from writings.models import Quote, Character

logger = logging.getLogger(__name__)


class AbstractQuestion(models.Model):

    class Meta:
        abstract = True

    @property
    def text(self):
        raise NotImplementedError()

    @property
    def get_answers():
        raise NotImplementedError()

    @property
    def correct_answer(self):
        raise NotImplementedError()


class QuoteQuestion(AbstractQuestion):
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


class QuoteQuestionRecord(models.Model):
    question = models.ForeignKey(QuoteQuestion, on_delete=models.CASCADE)
    answer = models.IntegerField(blank=True, null=True)

    def is_answered(self) -> bool:
        return self.answer is not None
    
    def is_correct(self) -> bool:
        """Check that answer"""
        return self.answer == self.question.correct_answer.id

    @property
    def as_dict(self) -> Dict[str, Any]:
        return {
            'question_id': self.question.id,
            'text': self.question.text,
            'answers': self.question.get_answers(),
            'is_answered': self.is_answered(),
            'is_correct': self.is_correct(),
            'answer': self.answer,
            'correct_answer': self.question.correct_answer.id,
        }

class QuotesTestRun(models.Model):
    questions = models.ManyToManyField(QuoteQuestionRecord, blank=True, null=True)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    finish_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = "Тест на знание цитат"

    @staticmethod
    def generate_run(count: int = 0, user=None):
        """Return new run with `count` of questions"""
        run = QuotesTestRun(user=user)
        run.save()
        all_questions = list(QuoteQuestion.objects.all())
        if count == 0 or count >= len(all_questions):
            count = len(all_questions)
        questions = sample(all_questions, count)
        records = []
        for question in questions:
            records.append(
                QuoteQuestionRecord.objects.create(question=question))
        print(records)
        run.questions.set(records)
        run.save()
        return run

    def is_finished(self) -> bool:
        """Check that all questions are answered"""
        return all([x.is_answered() for x in self.questions.all()])

    def current_question(self) -> QuoteQuestionRecord:
        if not self.is_finished():
            record = [
                x for x in self.questions.all() if not x.is_answered()
            ][0]
            return record
        return None
    
    def set_answer(self, answer) -> None:
        question = self.current_question()
        question.answer = answer
        question.save()

    @property
    def corrects_count(self) -> int:
        corrects = [x for x in self.questions.all() if x.is_correct()]
        return len(corrects)

    @property
    def answered_count(self) -> int:
        answered = [x for x in self.questions.all() if x.is_answered()]
        return len(answered)

    @property
    def as_dict(self) -> Dict[str, Any]:
        questions = [x.as_dict for x in self.questions.all()]
        current_index = None
        if not self.is_finished():
            current = list(
                filter(
                    lambda x: x['question_id'] == self.current_question().question.id, 
                    questions
                )
            )[0]
            current_index = questions.index(current)
        return {
            'questions': questions,
            'current_index': current_index,
        }
    
    @staticmethod
    def test_name():
        return QuotesTestRun._meta.verbose_name