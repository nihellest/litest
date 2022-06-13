"""
Service layer for tests app
"""

from random import sample
from typing import (
    Dict, Optional, Any
)

from django.db import models
from django.http import HttpRequest
from django.contrib.sessions.backends.base import SessionBase
from django.conf import settings
from .models import QuoteQuestion
from .forms import QuestionForm


class TestDataService:
    """
    TestService assistance class for tasks associated with model
    """

    def __init__(self, model: models.Model) -> None:
        self.model = model

    def get_questions(self, count: int=settings.APP_DEFAULT_TEST_RUN_LENGTH) -> Dict[str, Any]:
        """Select `count` of questions shuffled"""

        all_questions = list(self.model.objects.all())
        if count == 0 or count >= len(all_questions):
            count = len(all_questions)
        questions = [q.as_dict for q in sample(all_questions, count)]
        return questions

    def check_answer(self, question_id: int, answer_id: int) -> bool:
        question = self.model.objects.get(pk=question_id)
        return question.is_correct(answer_id)

    def get_correct_answer(self, question_id: int) -> int:
        question = self.model.objects.get(pk=question_id)
        return question.correct_answer.id


class TestService:
    """
    Service responcible for tests view's context reation
    and read/write context data into current session.

    Context dictionary format:

    ```python
    {
        'test_name': str,
        'test_run_link': Optional(str),
        'run': {
            'questions': [
                {
                    'question_id': int,
                    'text': str,
                    'answers': [(int, str), ...],
                    'is_answered': bool,
                    'is_correct': Optional(bool),
                },
                ...
            ]
            'current_index': int,
            'form': TestForm,
            'is_finished': Optional(bool),
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
            'run': self._extract_test_context(session=request.session),
        }
        return context

    def get_run_context(self, request: HttpRequest) -> Dict[str, Any]:
        """Return Dict context for test's run"""

        request.session.modified = False
        run = self._extract_test_context(session=request.session)
        answers = self._extract_answers(request=request)
        if run is None:
            run = self._new_run()
        if answers:
            run = self._update_run(run, answers)

        # Store run data to session
        self._write_session_context(session=request.session, run=run)
        if not run['finished']:
            form = self._get_form(self._get_current_question(run))
        else:
            form = None

        return {
            'test_name': self.name,
            'run': run,
            'form': form,
        }

    def get_results_context(self, request: HttpRequest) -> Dict[str, Any]:
        run = self._extract_test_context(session=request.session)
        return {
            'test_name': self.name,
            'run': run,
        }

    def refresh_context(self, session: SessionBase) -> None:
        """Clear from session test related data"""

        if self._session_has_context(session):
            del session[self._session_key]

    def is_run_finished(self, session: SessionBase) -> bool:
        """Check that current test run is finished"""
        run = self._extract_test_context(session)
        return 'finished' in run and run['finished']

    @property
    def _session_key(self):
        """Return name of key for storing data in session"""

        return f'{self.TESTS_SESSION_KEY}_{self.name}'

    def _session_has_context(self, session: SessionBase) -> bool:
        """Check presence of test related data in session"""

        return self._session_key in session

    def _write_session_context(self, session: SessionBase, run: dict) -> None:
        """Write current run data into session"""

        session[self._session_key] = run

    def _extract_test_context(self, session: SessionBase) -> Optional[Dict[str, Any]]:
        """Метод извлекающий существующий контекст из текущей сессии"""

        if self._session_has_context(session):
            return session[self._session_key]
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
            'finished': False,
        }

    def _update_run(self, run: dict, answers: dict):
        """Update answered questions"""

        if 'answers' in answers:
            answer = int(answers['answers'][0])
            question_id = int(answers['question_id'][0])
            run = self._update_questions(run, question_id, answer)

        # Update current index
        current_question = self._get_current_question(run)
        if current_question:
            run['current_index'] = run['questions'].index(current_question)
        else:
            run['finished'] = True

        return run

    def _update_questions(self, run: dict, question_id: int, answer: int):
        """Update fields of answered questions in run context"""

        for question in run['questions']:
            if question['question_id'] == question_id:
                question['is_answered'] = True
                question['answer'] = answer
                question['is_correct'] = self.data.check_answer(
                    question_id=question_id,
                    answer_id=answer
                    )
                if not question['is_correct']:
                    question['correct_answer'] = self.data.get_correct_answer(question_id)
        return run

    @staticmethod
    def _get_current_question(run):
        """Find first unanswered question"""

        for question in run['questions']:
            if 'is_answered' not in question or not question['is_answered']:
                return question
        return None

    @staticmethod
    def _get_form(question):
        """Generate form for question"""

        return QuestionForm(question=question)


TEST_SERVICES = {
    'quotes': TestService(name='quotes', model=QuoteQuestion),
}
