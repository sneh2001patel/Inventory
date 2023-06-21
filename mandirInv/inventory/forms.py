from django import forms
from .models import Report
from django.contrib.auth import get_user_model
from django.forms import HiddenInput
from authencation.models import Area

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


class CreateArea(forms.ModelForm):
    name = forms.CharField(
        error_messages={
            'required': "Please Enter valid area"
        })

    def __init__(self, *args, **kwargs):
        super(CreateArea, self).__init__(*args, **kwargs)
        self.fields["name"].widget.attrs['class'] = "input-field"
        self.fields["name"].widget.attrs["placeholder"] = "Area"
        self.fields["location"].widget.attrs['class'] = "input-field"
        self.fields["location"].widget.attrs["placeholder"] = "Location"

    class Meta:
        model = Area
        fields = ("name", "location",)
