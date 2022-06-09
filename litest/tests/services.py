from abc import ABC, abstractproperty
from dataclasses import dataclass
from random import sample
from typing import (
    List, Dict, Optional, Any, Tuple
)

from django.db import models
from django.http import HttpRequest
from .models import QuoteQuestion
from .forms import QuestionForm


DEFAULT_QUESTIONS_COUNT = 3


class TestDataService:
    """
    TestService assistance class for tasks associated with model
    """

    def __init__(self, model: models.Model) -> None:
        self.model = model

    def get_questions(self, count: int=DEFAULT_QUESTIONS_COUNT) -> Dict[str, Any]:
        """Select `count` of questions shuffled"""

        all_questions = list(self.model.objects.all())
        if count == 0 or count >= len(all_questions):
            count = len(all_questions)
        questions = [q.as_dict for q in sample(all_questions, count)]
        return questions


class TestService:
    """
    Service responcible for tests view's context reation
    and read/write context data into current session.

    Context dictionary format:

    ```python
    {
        'test_name': str,
        'run': {
            'questions': [
                {
                    'question_id': int,
                    'text': str,
                    'answers': [(int, str), ...],
                    'is_answered': bool
                    'is_correct': Optional(bool)
                },
                ...
            ]
            'current_index': int,
            'form': TestForm,
        }
    }
    ```
    """

    TESTS_SESSION_KEY = 'tests'

    def __init__(self, name: str, model: models.Model) -> None:
        self.name = name
        self.data = TestDataService(model)
     
    def get_page_context(self, request: HttpRequest) -> Dict[str, Any]:
        """Return Dict context for main test page"""

        context = {
            'test_name': self.name,
            'run': self._extract_test_context(request),
        }
        return context
    
    def get_run_context(self, request: HttpRequest) -> Dict[str, Any]:
        """Return Dict context for test's run"""

        run = self._extract_test_context(request)
        answers = self._extract_answers(request)
        if run == None:
            run = self._new_run()
        if answers:
            run = self._update_run(run, answers)
        form = self._get_form(self._get_current_question(run))
        
        return {
            'test_name': self.name,
            'run': run,
            'form': form,
        }
    
    def refresh_context(self, request: HttpRequest) -> None:
        ...

    def _extract_test_context(self, request: HttpRequest) -> Optional[Dict[str, Any]]:
        """Метод извлекающий существующий контекст из текущей сессии"""

        if self.TESTS_SESSION_KEY in request.session:
            if self.name in request.session[self.TESTS_SESSION_KEY]:
                return request.session[self.TESTS_SESSION_KEY][self.name]
        return None

    @staticmethod
    def _extract_answers(request) -> Dict[str, Any]:
        """Extract user's submited data"""

        if request.method == 'POST':
            return request.POST
        return None

    def _new_run(self) -> Dict[str, Any]:
        """Generate new run dictionary"""

        return {
            'questions': self.data.get_questions(),
            'current_index': 0,
        }
    
    def _update_run(self, run: dict, answers: dict):
        """Update answered questions"""

        if 'answers' in answers:
            pass
        return NotImplementedError
    
    @staticmethod
    def _get_current_question(run):
        """Find first unanswered question"""

        return run['questions'][run['current_index']]
    
    @staticmethod
    def _get_form(question):
        """Generate form for question"""

        return QuestionForm(question=question)


TEST_SERVICES = {
    'quotes': TestService(name='quotes', model=QuoteQuestion),
}
