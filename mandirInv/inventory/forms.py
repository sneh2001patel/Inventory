from django import forms
from .models import Report
from django.contrib.auth import get_user_model
from django.forms import HiddenInput
from authencation.models import Area
from .models import Item

User = get_user_model()


class CreateReport(forms.ModelForm):
    # expected = forms.IntegerField(attrs={'placeholder':'quantity','onkeyup':'success()'})
    def __init__(self, *args, **kwargs):
        super(CreateReport, self).__init__(*args, **kwargs)
        self.fields["actual"].label = ""
        self.fields['actual'].widget.attrs['onkeyup'] = 'success()'
        self.fields['actual'].widget.attrs['id'] = 'textsend'
        self.fields['actual'].widget.attrs['class'] = 'input-field'
        self.fields['actual'].widget.attrs['placeholder'] = 'Actual Quantity'
        # self.fields['actual'].widget.attrs['label'] = 'Hello '

    def clean_actual(self):
        cleaned_data = self.cleaned_data
        actual = cleaned_data.get('actual')
        return actual

    def clean(self):
        cleaned_data = self.cleaned_data
        print("all data: ", cleaned_data)
        return cleaned_data

    class Meta:
        model = Report
        fields = ('actual',)


class CreateItem(forms.ModelForm):
    # uid = forms.IntegerField()
    # description = forms.CharField()
    # details = forms.CharField()
    # image = forms.ImageField()
    # quantity = forms.IntegerField()
    # code = forms.CharField()
    # area = forms.ModelForm()
    details = forms.CharField(widget=forms.Textarea(attrs={'name': 'body', 'rows': '3', 'cols': '5'}))
    def __init__(self, *args, **kwargs):
        super(CreateItem, self).__init__(*args, **kwargs)
        self.fields['code'].widget.attrs['class'] = 'input-field'
        self.fields['code'].label = ""
        self.fields['code'].widget.attrs['placeholder'] = "Code"

        self.fields['description'].widget.attrs['class'] = 'input-field'
        self.fields['description'].label = ""
        self.fields['description'].widget.attrs['placeholder'] = "Title"

        self.fields['quantity'].widget.attrs['class'] = 'input-field'
        self.fields['quantity'].label = ""
        self.fields['quantity'].widget.attrs['placeholder'] = "Quantity"
        self.fields['details'].widget.attrs['class'] = 'input-field'
        self.fields['details'].label = ""
        self.fields['details'].widget.attrs['placeholder'] = "Details"
        self.fields['details'].widget.attrs['rows'] = 5
        self.fields['area'].label = ""
        self.fields['area'].widget.attrs['class'] = 'input-field'
        self.fields['image'].widget.attrs['id'] = 'imgInp'
        self.fields['image'].widget.attrs['onchange'] = 'readURL(this);'

        # self.fields['area'].widget.attrs['class'] = 'input-field'



    class Meta:
        model = Item
        fields = ["code", "description", "quantity", "area", "details", 'image']

        exclude = ['slug', 'uid']


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
