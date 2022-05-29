from django import forms
from .models import QuoteQuestion


class QuoteTestForm(forms.Form):
    answers = forms.ChoiceField(choices=[], widget=forms.RadioSelect)
    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super().__init__(*args, **kwargs)
        self.fields['answers'].choices = question.get_answers
