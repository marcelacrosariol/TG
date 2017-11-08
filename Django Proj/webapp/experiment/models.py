from django.db import models
from django.contrib.auth.models import User

class Algorithm(models.Model):
    idAlg = models.AutoField(primary_key=True)
    nameAlg = models.CharField(null=False, blank=False, max_length=100)
    desc = models.CharField(null=True, blank=False, max_length=500)
    command = models.CharField(null=False, blank=False, max_length=100)
    sample = models.FileField(upload_to="samples/", null=True, blank=True)
    file = models.FileField(upload_to="algorithms/", null=True, blank=True)

    def __str__(self):
        return self.nameAlg


class AppUser(models.Model):
    nickname = models.CharField(
        default='default', max_length=30, blank=False, null=True)
    company = models.CharField(
        default='default', max_length=50, blank=False, null=True)
    usuario = models.OneToOneField(User)
    date_register = models.DateField('date_register', auto_now_add=True)
    last_access = models.DateField('last_access', auto_now=True)
    resultsPerPage = models.IntegerField(default=10)
    notification = models.CharField(default="yes", choices=(("yes","Sim"),("no","Não")), max_length=4, blank=True)

    def __str__(self):
        return self.nickname


def user_directory_path_in(instance, filename):
    return './users/user_{0}/{1}/input'.format(instance.request_by.usuario.id, instance.id)


def user_directory_path_out(instance, filename):
    return './users/user_{0}/{1}/output'.format(instance.request_by.usuario.id, instance.id)


class Execution(models.Model):
    request_by = models.ForeignKey(AppUser)
    date_requisition = models.DateField('date_requisition', auto_now_add=True)
    status = models.IntegerField(default=1)
    algorithm = models.ForeignKey(Algorithm, null=True, blank=False)
    inputFile = models.FileField(upload_to=user_directory_path_in, null=True)
    outputFile = models.FileField(upload_to=user_directory_path_out, null=True)
    time = models.FloatField(default=-1)
    visible = models.CharField(choices=(("yes","Sim"),("no","Não")), default='yes',blank=False,null=False, max_length=3)

    def __int__(self):
        return self.request_by.id  
