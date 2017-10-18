from django.db.models import Count
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.template import RequestContext
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from experiment.forms import *
from experiment.models import Execution, Algorithm, AppUser
from django.http import HttpResponseRedirect, HttpResponse 
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from django.core.files import File
# jsonview - Crispy validation

import json, os
from jsonview.decorators import json_view
from crispy_forms.utils import render_crispy_form
from crispy_forms.helper import FormHelper
from django.contrib import messages
# paginator
from experiment.paginator import paginate

from experiment.tasks import RunExperiment
from random import randint

#################### HOME #################### 

def home(request):
    if not request.user.is_authenticated():
        title = "Bem-vindo"
        context = {
            'title': title
        }
        return render(request, "welcome.html", context)
    else:
        title = "Welcome %s" % request.user
        print(request.user.id)
        executionList = Execution.objects.filter(
            request_by__usuario__id=request.user.id).order_by('-id')
        try:
            UserProf = AppUser.objects.get(usuario__id=request.user.id)
        except:
            print ("Erro. Criando novo perfilf")
            user = User.objects.get(id=request.user.id)
            UserProf = AppUser(usuario=user)
            UserProf.save()
            print ("Criado novo UserProf")
        paginator = Paginator(executionList, UserProf.resultsPerPage)
        page = request.GET.get('page')
        if page is None:
            page = 1
        try:
            executions = paginator.page(page)
        except PageNotAnInteger:
            executions = paginator.page(1)
        except EmptyPage:
            executions = paginator.page(paginator.num_pages)  # da pra tratar
        if paginator.count == 0:
            data = None
        else:
            data = executions
        pageI = paginate(page, paginator)
        context = {
            'title': title,
            'data': data,
            'pagesIndex': pageI,
        }
        return render(request, "home.html", context)

#################### ABOUT #################### 

def about(request):
    return render(request, "about.html", {})

#################### CONTACT #################### 

def contact(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        subject = 'Portal Friends - Mensagem de %s ' % (
            form.cleaned_data.get("nome"))
        from_email = settings.EMAIL_HOST_USER  
        to_email = from_email
        sender = form.cleaned_data.get("email")
        message = "Contact: " + sender + "\n" + form.cleaned_data.get("mensagem")
        send_mail(subject,
                  message,
                  from_email,
                  [to_email],
                  fail_silently=False)
        return HttpResponseRedirect(reverse('contact'))
    context = {
        'form': form,
    }
    return render(request, "contact.html", context)

#################### USER PROFILE / REGISTER #################### 

def getUserProfile(request, username):
    user = User.objects.get(username=username)
    appUser = AppUser.objects.get(usuario=user.id)
    
    email = user.email
    company = appUser.company
    choice = appUser.notification

    data={'email':email,'company':company,'choice':choice}
    form = AppUserForm(request.POST or None, initial=data)
    context = {
        'user': user, 
        'appUser': appUser,
        'form':form
    }
    return render(request, 'user_profile.html', context)    

def saveProfile(request, username):
    email =  request.POST.get("email")
    company = request.POST.get("company")
    choice = request.POST.get("choice")

    user = User.objects.filter(username=username).update(email=email)
    appUser = AppUser.objects.filter(usuario=user)

    appUser.update(company=company,notification=choice)

    return HttpResponseRedirect(reverse('userProfile', kwargs={'username':username}))


def register_sucess(request):
    return render(request, "registration/registration_complete.html", {})

#################### FILES DOWNLOAD / UPLOAD #################### 

def downloadInputFile(request):
    expId = request.GET.get('id')
    execution = Execution.objects.get(pk=expId)
    # if (execution.request_by.usuario.id == request.user.id):
    #     response = HttpResponse(
    #         execution.inputFile, content_type='application/force-download')
    #     response[
    #         'Content-Disposition'] = 'attachment; filename="entrada-Experimento-' + str(expId) + '"'
    #     return response
    # criar alerta
    response = HttpResponse(
        execution.inputFile, content_type='application/force-download')
    response[
        'Content-Disposition'] = 'attachment; filename="entrada-Experimento-' + str(expId) + '"'
    return response
    # return HttpResponseRedirect(reverse('home'))

def downloadOutputFile(request):
    expId = request.GET.get('id')
    execution = Execution.objects.get(pk=expId)
    if (execution.request_by.usuario.id == request.user.id):
        print (execution.outputFile.url)
        print ("Autorizado")
        response = HttpResponse(
            execution.outputFile, content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename="Resultado-Experimento-' + str(expId) + '"'
        return response
    print ("Nao autorizado")
    # criar alerta
    return HttpResponseRedirect(reverse('home'))

def downloadSample(request, path):
    file = Algorithm.objects.get(nameAlg=path).sample
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    response = HttpResponse(file, content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
    return response

#################### ADMIN - ALGORITHMS ####################

def listAlg(request):
    listAlg = Algorithm.objects.all()
    return render(request, "algorithm.html", {'title': 'Algoritmos' ,'algorithms':listAlg})

def seeAlg(request, alg):
    title="Algoritmo"
    alg = Algorithm.objects.get(idAlg=alg)

    data = {'nameAlg': alg.nameAlg, 'desc':alg.desc, 'sample':alg.sample,'file':alg.file}
    form = AlgorithmForm(request.POST or None, initial=data)

    context={
        'title': title,
        'form': form,
        'idAlg': alg.idAlg
    }

    return render(request, "edit_alg.html", context)

def addAlg(request):
    form = AlgorithmForm(request.POST or None)
    return render(request, "add_algorithm.html", {'form':form})

def updateAlg(request,idAlg):
    desc = request.POST.get("desc")
    clear = request.POST.get("sample-clear")
    
    if (clear == 'on'):
        sample = None
    else:
        sample = request.FILES['sample']

    algorithm = Algorithm.objects.filter(idAlg=idAlg).update(desc=desc,sample=sample)
    return HttpResponseRedirect(reverse('listAlgorithm'))

def removeAlg(request):
    if request.method == 'POST':
        data = request.POST.get('data')
        print (data)
        if data:
            ids = data.split(",")
            print (ids)
            Algorithm.objects.filter(idAlg__in=ids).delete()
        # objects = Model.objects.filter(id__in=object_ids)
    return HttpResponseRedirect(reverse('listAlgorithm'))

def saveAlg(request):
    name = request.POST.get('nameAlg')
    desc= request.POST.get('desc')
    algFile = request.FILES['file']
            
    newAlg = Algorithm()

    newAlg.nameAlg = name
    newAlg.desc = desc
    newAlg.command = './'
    newAlg.file=algFile
   
    if ('sample' in request.FILES): 
        sample = request.FILES['sample']
        newAlg.sample=sample
        
    newAlg.save()
    extension = algFile.name.split(".")[-1].lower()
    
    if (extension== 'c'):
        os.system("gcc " + Algorithm.objects.get(nameAlg=name).file.path + " -o algorithms/" + name + ' 2> log.txt' )
        newAlg.command = './algorithms/' + name

    newAlg.save()

    return HttpResponseRedirect(reverse('listAlgorithm'))

#################### ADMIN - EXECUTIONS ####################

#################### ADMIN - STATISTICS ####################

def appStatistics(request):
    form = YearChartForm(request.POST or None)
    if request.method == 'POST':
        year = request.POST.get('year')
    else: 
        year = '2017' 
    print(year)
    
    #Dataset
    items = {}
    #For each algorithm in the database
    for algorithm in Algorithm.objects.all():
        
        data = []
        label = algorithm.nameAlg
        
        for month in range(12):
            qtd = Execution.objects.filter(algorithm=algorithm.pk,date_requisition__month=month+1, date_requisition__year=year).count()
            data.append(qtd)
        
        items[algorithm.nameAlg] = data 

    return render(request, "statistics.html", {'form':form, 'dataset': json.dumps(items)})

#################### EXPERIMENTS / EXECUTION ####################

@json_view
@csrf_protect
def checkForm(request):
    form = ExecutionForm(request.POST or None)  # request POST?
    print(request.POST)
    print ("\n\n")

    if form.is_valid():  # processa
        experiments(request)
        helper = FormHelper()
        helper.form_id = 'form_exec'
        helper.form_action = '.'
        form_html = render_crispy_form(ExecutionForm(None), helper)
        return {'success': True, 'form_html': form_html}
    else:
        helper = FormHelper()
        helper.form_id = 'form_exec'
        helper.form_action = '.'
        form_html = render_crispy_form(form, helper, RequestContext(request))
        return {'success': False, 'form_html': form_html}


@csrf_protect
def experiments(request):
    if request.method == 'POST':
        form = ExecutionForm(request.POST, request.FILES or None)
        if not form.is_valid():
            title = "Experiments %s" % (request.user)
            # form_html = render_crispy_form(form)
            context = {
                'form': form,
                'title': title,
            }
            return render(request, "experiments.html", context)
        algorithm = request.POST.get('Algoritmo')
        d_User = User.objects.get(username=request.user)
        alg = Algorithm.objects.get(nameAlg=algorithm)
        execution = Execution(
            request_by=d_User.appuser,
            algorithm=alg
        )
        execution.save()
        if (request.FILES):
            # print request.FILES
            fileIn = request.FILES["Entrada"]
            execution.inputFile = fileIn
            execution.save()
            queryInputFile = (
                settings.MEDIA_ROOT +
                execution.inputFile.name.replace('./', '/')
            ).replace(' ', '\ ')
            queryOutputFile = queryInputFile
            queryOutputFile = queryOutputFile.replace('input', 'output')
            # print "QUERY OUT : " + queryOutputFile
            query = alg.command + ' ' + queryInputFile + '>' + queryOutputFile
            # print query
        else:
            query = execution.algorithm.command
            outputFilePath = './users/user_' + \
            str(execution.request_by.usuario.id) + \
            '/' + str(execution.id) + '/output'
        # print(outputFilePath)
        # teste = RunExperiment.delay(execution.algorithm.command)
        teste = RunExperiment.delay(alg.command, execution.id)
        # teste = RunExperiment.delay(query, execution, outputFilePath)
        #print teste.status
        # RunExperiment.apply_async(
        #     args=[query, execution, outputFilePath], kwargs={}, countdown=60)
        # RunExperiment.delay(query, execution, outputFilePath)
        # os.system(query)
        # execution.outputFile = queryOutputFile
        execution.save()
        title = "Experiments %s" % (request.user)
        # cont = {"title": title, "form": form}
        return HttpResponseRedirect(reverse('home'))
        # return render(request, "experiments.html", cont)
    form = ExecutionForm(request.POST or None)
    title = "Experiments %s" % (request.user)

    hlp = {}
    for item in Algorithm.objects.all():
      hlp[item.nameAlg] = [item.desc,str(item.sample)]

    print (hlp)

    context = {
        'title': title,
        'form': form,
        'help': hlp
    }
    return render(request, "experiments.html", context)

def experimentsRemove(request):
    if request.method == 'POST':
        data = request.POST.get('data')
        if data:
            ids = data.split(",")
            print (ids)
            Execution.objects.filter(id__in=ids).delete()
        # objects = Model.objects.filter(id__in=object_ids)
    return HttpResponseRedirect(reverse('home'))

@csrf_exempt
def result(request):
    if request.method == 'POST':
        print ("POST")
    if (request.FILES):
            idExec = request.POST.get("id")
            tempo  = request.POST.get("time")
            print("id: %s time: %s" %(idExec,tempo))

            execution = Execution.objects.get(id=idExec)
            fileIn = request.FILES["file"]
            execution.outputFile=fileIn
            execution.status=3
            execution.time = tempo
            execution.save()

            appUser = execution.request_by
            userEmail = appUser.usuario.email

            if (appUser.notification == 'yes'): 
                subject = 'Portal Friends - Experimento concluido com sucesso' 
                from_email = settings.EMAIL_HOST_USER  
                to_email = userEmail
                message = "Olá " + appUser.nickname + " experiencia " + idExec + " foi concluida com sucesso"
                send_mail(subject, message,from_email,[to_email], fail_silently=False)

    return HttpResponse(1)
