from django import forms
from registration.forms import RegistrationFormUniqueEmail
from .models import Algorithm, Execution
from django.contrib.auth.models import User
from django.contrib.auth.forms import SetPasswordForm

class PasswdChangeForm(SetPasswordForm):
  error_messages = {'password_mismatch': "As duas senhas não são iguais.",}
  
  new_password1 = forms.CharField(label="Nova senha",
                                    widget=forms.PasswordInput,
                                    required=False)
  new_password2 = forms.CharField(label="Confirmação da nova senha",
                                    widget=forms.PasswordInput,
                                    required=False)

class AppUserForm(RegistrationFormUniqueEmail):
    username = forms.CharField(required=True, label='Usuário', max_length=20, help_text="Máximo 20 caracteres")
    password1 = forms.CharField(required=True,label="Senha", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmação da senha", widget=forms.PasswordInput, help_text="Digite a mesma senha do campo anterior")
    nickname = forms.CharField(required=True, label='Nome', max_length=30)
    company = forms.CharField(required=True, label='Empresa / Instituição', max_length=30)
    resultsPerPage =forms.IntegerField(required=False, initial=10, label="Resultados por página")
    choice = forms.ChoiceField(choices=[('yes','Sim'),('no','Não')], initial='yes', widget=forms.Select, required=False,label="Notificação da conclusão de execuções por email?")

class UserForm(forms.ModelForm):
  class Meta:
    model = User
    fields = ['email','password','user_permissions','is_staff', 'is_active', 'user_permissions']
    labels = {
            'email': 'Email',
            'password': 'Senha',
            'user_permissions': 'Permissões',
            'is_staff': 'Administrador', 
            'is_active': 'Conta Ativa', 
                }
    help_text = {
            'is_active': 'Define se a conta está ativa',
    }

class ExecutionForm(forms.Form):
    Algoritmo = forms.ModelChoiceField(queryset=Algorithm.objects.all(),
                                       empty_label='---Selecione um algoritmo---',
                                       required=True,
                                       to_field_name='nameAlg',
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
      fields = ['nameAlg','desc','sample','file']
      labels = {
            'nameAlg': 'Algoritmo',
            'desc': 'Descrição',
            'sample': 'Exemplo de entrada',
            'file': 'Arquivo' 
                }

