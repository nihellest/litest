from django import forms
from .models import QuoteQuestion


class QuoteTestForm(forms.Form):
    answers = forms.ChoiceField(choices=[], widget=forms.RadioSelect)
    question_id = forms.HiddenInput()
    def __init__(self, *args, **kwargs):
        self.question = kwargs.pop('question')
        super().__init__(*args, **kwargs)
        self.fields['answers'].choices = self.question.get_answers
