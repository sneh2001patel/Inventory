from django import forms
from .models import Report
from django.contrib.auth import get_user_model

User = get_user_model()


class CreateReport(forms.ModelForm):
    # expected = forms.IntegerField(attrs={'placeholder':'quantity','onkeyup':'success()'})
    def __init__(self, *args, **kwargs):
        super(CreateReport, self).__init__(*args, **kwargs)
        self.fields['actual'].widget.attrs['onkeyup'] = 'success()'
        self.fields['actual'].widget.attrs['id'] = 'textsend'
        self.fields['actual'].widget.attrs['placeholder'] = 'Actual Quantity'
        # self.fields['actual'].widget.attrs['label'] = 'Hello '

    class Meta:
        model = Report
        fields = ('actual',)

