from django import forms
from registration.forms import RegistrationFormUniqueEmail
from .models import Algorithm

class AppUserForm(RegistrationFormUniqueEmail):
    nickname = forms.CharField(required=False)
    company = forms.CharField(required=False)


class ExecutionForm(forms.Form):
    hlp = {}
    for item in Algorithm.objects.all():
      hlp[item.nameAlg] = item.desc 


    Algoritmo = forms.ModelChoiceField(queryset=Algorithm.objects.all(),
                                       empty_label="---Selecione um algoritmo---",
                                       required=True,
                                       to_field_name="nameAlg",
                                       )
    Entrada = forms.FileField(required=False)


class ContactForm(forms.Form):
    nome = forms.CharField()
    email = forms.EmailField()
    mensagem = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}))
