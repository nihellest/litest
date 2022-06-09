from django import forms
from .models import QuoteQuestion


class QuestionForm(forms.Form):
    """Form for represent question's text and answers"""
    answers = forms.ChoiceField(choices=[], widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):
        self.question = kwargs.pop('question')
        super().__init__(*args, **kwargs)
        self.fields['answers'].choices = self.question['answers']
