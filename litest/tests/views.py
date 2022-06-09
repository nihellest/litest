import logging
from typing import Dict, Any

from django.shortcuts import redirect, render
from django.http import Http404, HttpRequest, HttpResponse
from django.views.decorators.http import require_http_methods, require_GET

from .services import TestService, TEST_SERVICES

logger = logging.getLogger(__name__)

DEFAULT_QUESTIONS_COUNT = 3


@require_GET
def GenericTestPage(request, test_name: str) -> HttpResponse:
    """View for test's main page"""

    if test_name not in TEST_SERVICES:
        raise Http404()
    service: TestService = TEST_SERVICES[test_name]
    context: Dict[Any] = service.get_page_context(request)
    return render(request, 'tests/test_page.html', context)


@require_http_methods(['GET', 'POST'])
def GenericTestRun(request: HttpRequest, test_name: str) -> HttpResponse:
    """View for tests"""

    # Get associated TestService instance
    if test_name not in TEST_SERVICES:
        raise Http404()
    service: TestService = TEST_SERVICES[test_name]
    
    # Is new run?
    if request.method == 'GET' and 'new' in request.GET:
        service.refresh_context(request.session)
        return redirect(GenericTestRun, test_name=test_name)
    
    context: Dict[str, Any] = service.get_run_context(request)
    return render(request, 'tests/test_run.html', context)
