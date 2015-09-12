__author__ = 'tyler'
from django import forms

from apps.contact.models import Contact


class EditForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'
        widgets = {
            'first_name': forms.TextInput(attrs={'size': 50,
                                          'id': 'first_name',
                                          'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'size': 50,
                                                'id': 'last_name',
                                                'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'id': 'birth_date',
                                                 'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'cols': 70, 'rows': 4, 'id': 'bio',
                                         'class': 'form-control'}),
            'email': forms.TextInput(attrs={'size': 50, 'id': 'email',
                                            'class': 'form-control'}),
            'skype': forms.TextInput(attrs={'size': 50, 'id': 'skype',
                                            'class': 'form-control'}),
            'contacts': forms.TextInput(attrs={'size': 50, 'id': 'contacts',
                                               'class': 'form-control'}),
            'jaber': forms.TextInput(attrs={'size': 50, 'id': 'jaber',
                                            'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'size': 50, 'id': 'phone',
                                            'class': 'form-control'}),
            'other_contacts': forms.Textarea(attrs={'cols': 70, 'rows': 4,
                                             'id': 'other_contacts',
                                             'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'id': 'photo'})
        }
