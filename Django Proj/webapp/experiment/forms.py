from django import forms
from registration.forms import RegistrationFormUniqueEmail
from .models import Algorithm, Execution

class AppUserForm(RegistrationFormUniqueEmail):
    nickname = forms.CharField(required=False)
    company = forms.CharField(required=False)
    choice = forms.ChoiceField(choices=[('yes','Sim'),('no','Não')], initial='yes', widget=forms.RadioSelect, required=False,label="Notificação da conclusão de execuções por email?")


class ExecutionForm(forms.Form):
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

class YearChartForm(forms.Form):
    years =[]
    for date in Execution.objects.dates('date_requisition','year'): years.append((date.year,date.year))

    year = forms.ChoiceField(choices=years, initial='2017', widget=forms.Select(attrs={'max_length': 4}), required=True, label="Selecione um ano")

class AlgorithmForm(forms.ModelForm):
    class Meta:
      model = Algorithm
      fields = ['nameAlg','desc','sample']