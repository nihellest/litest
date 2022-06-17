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
from .models import QuoteQuestion, QuotesTestRun
from .forms import QuestionForm


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
        }
    }
    ```
    """

    TESTS_SESSION_KEY = 'tests'

    def __init__(self, name: str, model: models.Model) -> None:
        self.name = name
        self.model = model

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
        answer = self._extract_answer(request=request)
        
        if run is None:
            run = self.model.generate_run(
                count=settings.APP_DEFAULT_TEST_RUN_LENGTH,
                user=request.user
            )
        if answer:
            run.set_answer(answer)

        # Store run data to session
        self._write_session_context(session=request.session, run_id=run.id)
        if not run.is_finished():
            form = self._get_form(run.current_question().question)
        else:
            form = None

        return {
            'test_name': self.name,
            'run_id': run.id,
            'run': run.as_dict,
            'form': form,
        }

    def get_results_context(self, request: HttpRequest) -> Dict[str, Any]:
        run = self._extract_test_context(session=request.session)
        return {
            'test_name': self.name,
            'run': run.as_dict,
        }

    def refresh_context(self, session: SessionBase) -> None:
        """Clear from session test related data"""

        if self._session_has_context(session):
            del session[self._session_key]

    def is_run_finished(self, session: SessionBase) -> bool:
        """Check that current test run is finished"""
        run = self._extract_test_context(session)
        return run.is_finished()

    @property
    def _session_key(self):
        """Return name of key for storing data in session"""

        return f'{self.TESTS_SESSION_KEY}_{self.name}'

    def _session_has_context(self, session: SessionBase) -> bool:
        """Check presence of test related data in session"""

        return self._session_key in session

    def _write_session_context(self, session: SessionBase, run_id: dict) -> None:
        """Write current run data into session"""

        session[self._session_key] = run_id

    def _extract_test_context(self, session: SessionBase) -> Optional[Dict[str, Any]]:
        """Метод извлекающий существующий контекст из текущей сессии"""

        if self._session_has_context(session):
            return self.model.objects.get(pk=session[self._session_key])
        return None

    @staticmethod
    def _extract_answer(request) -> Dict[str, Any]:
        """Extract user's submited data"""

        if request.method == 'POST':
            return int(request.POST['answers'][0])
        return None

    @staticmethod
    def _get_form(question):
        """Generate form for question"""

        return QuestionForm(question=question)


class TestStatisticsService:
    def __init__(self, model):
        self.model = model

    def get_runs_per_user(self, user):
        runs = self.model.objects.filter(user=user)
        return self.statistics_for_runs(runs)

    def statistics_for_runs(self, runs):
        # TODO: Move constant to settings
        LAST_RUNS_COUNT = 10
        last_runs = runs.order_by('-start_time')[:LAST_RUNS_COUNT]
        last_runs_statistics = []
        for run in last_runs:
            last_runs_statistics.append({
                'answered_count': run.answered_count,
                'corrects_count': run.corrects_count,
                'questions_count': run.questions.count(),
                'start_time':   run.start_time
            })
        return {
            'test_name': self.model.test_name(),
            'totals': {
                'total_runs': {
                    'label': 'Всего попыток',
                    'count': len(runs),
                },
                'finished_runs': {
                    'label': 'Законченных попыток',
                    'count': TestStatisticsService._finished_runs(runs),
                },
            },
            'last_runs': last_runs_statistics,
        }
    
    @staticmethod
    def _finished_runs(runs):
        return len([x for x in runs if x.is_finished()])


TEST_SERVICES = {
    'quotes': TestService(name='quotes', model=QuotesTestRun),
}

TEST_STATISTICS_SERVICES = {
    'quotes': TestStatisticsService(model=QuotesTestRun),
}