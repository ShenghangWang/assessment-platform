from django import forms
class DynamicQuizForm(forms.Form):
    def __init__(self, *args, questions=None, **kwargs):
        super().__init__(*args, **kwargs)
        for q in questions or []:
            self.fields[q['key']] = forms.TypedChoiceField(label=q['text'], choices=[(i, str(i)) for i in range(1, 6)], coerce=int, widget=forms.RadioSelect, required=True)
