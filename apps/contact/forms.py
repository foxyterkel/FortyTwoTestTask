__author__ = 'tyler'
from django import forms
from django.forms.extras.widgets import SelectDateWidget

from apps.contact.models import Contact


class EditForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'
        widgets = {
            'first_name': forms.TextInput(attrs={'size': 50,
                                          'id': 'first_name'}),
            'last_name': forms.TextInput(attrs={'size': 50, 'id': 'last_name'}),
            'birth_date': forms.DateInput(attrs={'id': 'birth_date'}),
            'bio': forms.Textarea(attrs={'cols': 70, 'rows': 4, 'id': 'bio'}),
            'email': forms.TextInput(attrs={'size': 50, 'id': 'email'}),
            'jaber': forms.TextInput(attrs={'size': 50, 'id': 'jaber'}),
            'phone': forms.TextInput(attrs={'size': 50, 'id': 'phone'}),
            'other_contacts': forms.Textarea(attrs={'cols': 70, 'rows': 4,
                                             'id': 'other_contacts'}),
            'photo': forms.FileInput(attrs={'id': 'photo'})
        }
