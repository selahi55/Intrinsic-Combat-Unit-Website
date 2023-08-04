from django import forms
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
import datetime

from .models import Disciplines, Contact, Client, Trainer

class DateInput(forms.DateInput):
    input_type = 'date'
    format = '%d%m%Y'
    
class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=50, required=True)
    last_name  = forms.CharField(max_length=50, required=True)
    email      = forms.EmailField(max_length=150, required=True, label='Your Email')
    message    = forms.CharField(max_length=150, widget=forms.Textarea, required=False)
    date       = forms.DateField(initial=now, widget=DateInput)
    discipline = forms.ChoiceField(required=True, choices=Disciplines.choices, widget=forms.Select(attrs={'class': 'dropdown'}))
    
    def clean_date(self):
        date = self.cleaned_data['date']

        if date < datetime.date.today():
            raise ValidationError(_('Invalid Date-Appointment in Past.'))
        
        if date > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid Date-Appointment should be made in one month time.'))
        
        return date

class ContactModelForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['date', 'discipline', 'showed_up']
        widgets = {'date': DateInput, 'discipline': forms.Select(attrs={'class': 'dropdown-contact'})}

    def clean_date(self):
        date = self.cleaned_data['date']

        if date < datetime.date.today():
            raise ValidationError(_('Invalid Date-Appointment in Past.'))
        
        if date > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid Date-Appointment should be made in one month time.'))
        
        return date

class EmailForm(forms.Form):
    subject = forms.CharField(max_length=100, required=True)
    message = forms.CharField(max_length=500, required=True, widget=forms.Textarea)

class TrainerEditForm(forms.ModelForm):
    class Meta:
        model = Trainer
        fields = ['percent']