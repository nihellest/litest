"""
Forms module for tests app
"""

from django import forms


class QuestionForm(forms.Form):
    """Form for represent question's text and answers"""
    answers = forms.ChoiceField(choices=[], widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):
        self.question = kwargs.pop('question')
        super().__init__(*args, **kwargs)
        self.fields['answers'].choices = self.question.get_answers()
