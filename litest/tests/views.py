import logging
from django.shortcuts import render
from .models import QuoteQuestion
from .forms import QuoteTestForm

logger = logging.getLogger(__name__)


def QuotesTest(request):
    question = QuoteQuestion.objects.get(pk=1)
    form = QuoteTestForm(question=question)
    correct_count = 0
    questions_count = 0
    answer = {}
    if request.method == 'POST':
        questions_count = int(request.POST['questions_count'][0]) + 1
        correct_count = int(request.POST['correct_count'][0])
        answer = int(request.POST['answers'][0])
        previous_question = QuoteQuestion.objects.get(pk=request.POST['question_id'][0])
        if previous_question.correct_answer.id == answer:
            correct_count += 1
    
    context = {
        'question': question,
        'form': form,
        'answer': answer,
        'questions_count': questions_count,
        'correct_count': correct_count,
    }
    return render(request, 'tests/quotes.html', context)
