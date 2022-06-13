"""
Views module for tests app
"""

import logging
from typing import Dict, Any

from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import Http404, HttpRequest, HttpResponse
from django.views.decorators.http import require_http_methods, require_GET

from .services import TestService, TEST_SERVICES

logger = logging.getLogger(__name__)

DEFAULT_QUESTIONS_COUNT = 3


def get_service(test_name: str) -> TestService:
    """Get associated TestService instance"""

    if test_name not in TEST_SERVICES:
        raise Http404()
    return TEST_SERVICES[test_name]


@require_GET
def generic_test_page(request, test_name: str) -> HttpResponse:
    """View for test's main page"""

    service: TestService = get_service(test_name)
    context: Dict[Any] = service.get_page_context(request)
    context['test_run_link'] = reverse(
        generic_test_run,
        kwargs={'test_name': test_name}
    )
    return render(request, 'tests/test_page.html', context)


@require_http_methods(['GET', 'POST'])
def generic_test_run(request: HttpRequest, test_name: str) -> HttpResponse:
    """View for tests"""

    service: TestService = get_service(test_name)

    # Is new run?
    if request.method == 'GET' and 'new' in request.GET:
        service.refresh_context(session=request.session)
        return redirect(generic_test_run, test_name=test_name)

    context: Dict[str, Any] = service.get_run_context(request)
    if service.is_run_finished(session=request.session):
        return redirect(generic_test_results, test_name=test_name)

    return render(request, 'tests/test_run.html', context)


@require_GET
def generic_test_results(request: HttpRequest, test_name: str) -> HttpResponse:
    """View for test's result page"""

    service: TestService = get_service(test_name)
    context = service.get_results_context(request)

    # Check that run was finished
    if not service.is_run_finished(session=request.session):
        return redirect(generic_test_run, test_name=test_name)

    return render(request, 'tests/test_results.html', context)
