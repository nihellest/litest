import logging
from django.shortcuts import render
from random import choice
from .models import QuoteQuestion
from .forms import QuoteTestForm

logger = logging.getLogger(__name__)


def QuotesTest(request):
    question = choice(list(QuoteQuestion.objects.all()))
    correct_count, questions_count = 0, 0
    result = {}
    if request.method == 'POST':
        questions_count = int(request.POST['questions_count'][0]) + 1
        correct_count = int(request.POST['correct_count'][0])
        answer = int(request.POST['answers'][0])
        previous_question = QuoteQuestion.objects.get(pk=request.POST['question_id'][0])
        result['correct_answer'] = previous_question.correct_answer
        if previous_question.is_correct(answer):
            result['correct'] = True
            correct_count += 1
        else:
            result['correct'] = False
    
    form = QuoteTestForm(question=question)
    context = {
        'form': form,
        'questions_count': questions_count,
        'correct_count': correct_count,
        'result': result,
    }
    return render(request, 'tests/quotes.html', context)
