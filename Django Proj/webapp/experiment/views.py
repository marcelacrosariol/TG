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
    title = "Home"
    if not request.user.is_authenticated(): 
        context = {
            'title': title
        }
        return render(request, "welcome.html", context)
    else:
        form = (request.POST or None)
        showOpt = 'Todas'
        if request.method == 'POST':
            showOpt = request.POST.get("showOpt")
            executionList = Execution.objects.filter().order_by('-id') if showOpt == 'Todas' else Execution.objects.filter(request_by__usuario__id=request.user.id).order_by('-id')
        else:
            executionList = Execution.objects.filter(request_by__usuario__id=request.user.id).order_by('-id')

        try:
            UserProf = AppUser.objects.get(usuario__id=request.user.id)
        except:
            print ("Erro. Criando novo perfil")
            user = User.objects.get(id=request.user.id)
            UserProf = AppUser(usuario=user)
            UserProf.save()
            print ("Criado novo UserProf")

        data, pageI = createPagination(request, executionList, UserProf.resultsPerPage)

        context = {
            'showOpt': showOpt,
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
        # print (execution.outputFile.url)
        # print ("Autorizado")
        response = HttpResponse(
            execution.outputFile, content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename="Resultado-Experimento-' + str(expId) + '"'
        return response
    # print ("Nao autorizado")
    # criar alerta
    return HttpResponseRedirect(reverse('home'))

def downloadSample(request, alg):
    file = Algorithm.objects.get(nameAlg=alg).sample
    file_path = file.path
    
    response = HttpResponse(file, content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path) 
    return response

#################### ADMIN - ALGORITHMS ####################

def listAlg(request):
    algorithmList = Algorithm.objects.filter().order_by('-idAlg') 
    perPage = AppUser.objects.get(usuario=request.user.id).resultsPerPage

    data, pageI = createPagination(request, algorithmList, perPage)

    context = {
        'title': 'Algoritmos',
        'data': data,
        'pagesIndex': pageI,
    }

    return render(request, "admin/algorithm.html", context)

def seeAlg(request, alg):
    title="Algoritmo"

    algL = Algorithm.objects.get(idAlg=alg)

    data = {'nameAlg': algL.nameAlg, 'desc':algL.desc, 'sample':algL.sample,'file':algL.file}
    form = AlgorithmForm(request.POST or None, initial=data)

    context={
        'title': title,
        'form': form,
        'idAlg': algL.idAlg,
    }

    return render(request, "admin/edit_alg.html", context)

def addAlg(request):
    form = AlgorithmForm(request.POST or None)
    return render(request, "admin/add_algorithm.html", {'form':form})

def updateAlg(request,idAlg):
    desc = request.POST.get("desc")
    clear = request.POST.get("sample-clear")
    
    algorithm = Algorithm.objects.get(idAlg=idAlg)

    if (clear == 'on'): algorithm.sample = None
    elif ('sample' in request.FILES):   algorithm.sample = request.FILES['sample']

    algorithm.desc = desc
    algorithm.save()

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

    newAlg.command = './algorithms/' + name    

    newAlg.save()

    return HttpResponseRedirect(reverse('listAlgorithm'))

#################### ADMIN - STATISTICS ####################

def appStatistics(request):
    form = YearChartForm(request.POST or None)
    if request.method == 'POST':
        year = request.POST.get('year')
    else: 
        year = '2017' 

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

    return render(request, "admin/statistics.html", {'form':form, 'dataset': json.dumps(items)})

#################### ADMIN - USERS ####################

def listUsers(request):
    title = 'Usuários'
    appUserList = AppUser.objects.filter().order_by('-id')

    perPage = AppUser.objects.get(usuario=request.user.id).resultsPerPage

    data, pageI = createPagination(request, appUserList, perPage)

    context = {
        'title': title,
        'data': data,
        'pagesIndex': pageI,
    }

    return render(request, "admin/users.html", context)

def seeUser(request, appUser, authUser):

    authUser = User.objects.get(username=authUser)
    appU = AppUser.objects.get(nickname=appUser, usuario=authUser.id)

    nickname = appU.nickname
    company = appU.company
    choice = appU.notification
    resultsPerPage = appU.resultsPerPage

    email = appU.usuario.email
    staff = appU.usuario.is_staff
    active = appU.usuario.is_active

    dataAppUser = {'nickname': nickname, 'company': company, 'choice': choice,'resultsPerPage':resultsPerPage}
    dataUser = {'email': email, 'is_staff': staff,'is_active':active}

    appUserForm = AppUserForm(request.POST or None, initial=dataAppUser)
    userForm = UserForm(request.POST or None, initial=dataUser)
    passwdForm = PasswdChangeForm(request.POST or None)

    context = {
        'title': 'Editar Usuário',
        'appUser': appUser,
        'authUser': authUser.username,
        'appUserForm': appUserForm,
        'userForm': userForm,
        'passwdForm': passwdForm,
    }

    return render(request, 'admin/edit_user.html', context)

def addUser(request):
    title = 'Novo usuário'
    appForm = AppUserForm(request.POST or None)
    uForm = UserForm(request.POST or None)
    context ={
        'title': title,
        'appForm': appForm,
        'uForm': uForm,
    }

    return render(request,'admin/add_user.html',context)

def saveUser(request):
    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password1")
    is_active = request.POST.get('is_active')

    nickname = request.POST.get("nickname")
    company = request.POST.get("company")
    resultsPerPage = request.POST.get("resultsPerPage")
    notification = request.POST.get("choice")

    active = True if is_active == 'on' else False

    user = User(username=username, 
            email=email, 
            is_active=active)
    user.set_password(password)
    user.save()

    appUser = AppUser(nickname=nickname,
        company=company,
        resultsPerPage=resultsPerPage,
        notification=notification,
        usuario=user)
    appUser.save()

    return HttpResponseRedirect(reverse('listUsers'))


#################### USER PROFILE / REGISTER #################### 

def getUserProfile(request, username):
    user = User.objects.get(username=username)
    appUser = AppUser.objects.get(usuario=user.id)
    
    email = user.email
    company = appUser.company
    choice = appUser.notification
    resultsPerPage = appUser.resultsPerPage

    data={'email':email,'company':company,'choice':choice, 'resultsPerPage': resultsPerPage}
    form = AppUserForm(request.POST or None, initial=data)
    context = {
        'user': user, 
        'appUser': appUser,
        'form':form
    }
    return render(request, 'user_profile.html', context)    

def saveProfile(request, uname):
    email =  request.POST.get("email")
    company = request.POST.get("company")
    choice = request.POST.get("choice")
    resultsPerPage = request.POST.get("resultsPerPage")

    #verificar se duplica email
    authUser = User.objects.filter(username=uname)
    authUser.update(email=email)

    appUser = AppUser.objects.filter(usuario=authUser[0].id)

    appUser.update(company=company,notification=choice, resultsPerPage=resultsPerPage)

    if (request.user.is_superuser and 'nickname' in request.POST.dict()):
        nickname = request.POST.get("nickname")
        is_staff = request.POST.get("is_staff")
        is_active = request.POST.get("is_active")

        passwd = request.POST.get("new_password1")
        if(passwd != ''):
            authUser[0].set_password(passwd)

        staff = True if is_staff == 'on' else False
        active = True if is_active == 'on' else False

        # print(is_active, active)
        appUser.update(nickname=nickname)
        authUser.update(is_staff=staff,is_active=active)

        return HttpResponseRedirect(reverse('listUsers'))

    return HttpResponseRedirect(reverse('home'))
    # return HttpResponseRedirect(reverse('userProfile', kwargs={'username':uname}))


def register_sucess(request):
    return render(request, "registration/registration_complete.html", {})


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

        if (execution.inputFile==None): 
            inFile = 'no'
            teste= RunExperiment.delay(alg.command, execution.id, inFile)
        else:
            teste= RunExperiment.delay(alg.command, execution.id)
        print("resultado", teste)

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

    context = {
        'title': title,
        'form': form,
        'help': hlp
    }
    return render(request, "experiments.html", context)
           
@csrf_exempt
def result(request):
    # if request.method == 'POST':
        # print ("POST")
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


#################### PAGINATION ####################

def createPagination(request, appList, resultsPerPage):
    paginator = Paginator(appList, resultsPerPage)
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

    return data, pageI


#################### REMOVE FROM LIST PAGE - ONE OR MANY ####################

def removeList(request, model):
    if request.method == 'POST':
        data = request.POST.get('data')
        if data:
            ids = data.split(",")
            if(model == 'Algoritmos'):
                Algorithm.objects.filter(idAlg__in=ids).delete()
                return HttpResponseRedirect(reverse('listAlgorithm'))
            if(model == 'Home'):
                Execution.objects.filter(id__in=ids).delete()
                return HttpResponseRedirect(reverse('home'))
            if(model == 'Usuários'):
                AppUser.objects.filter(usuario__in=ids).delete()
                User.objects.filter(id__in=ids).delete()
                return HttpResponseRedirect(reverse('listUsers'))