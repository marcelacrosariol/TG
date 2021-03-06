from experiment.models import AppUser, Execution
from celery.utils.log import get_task_logger
from celery.decorators import task
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import requests
import os
import time

logger = get_task_logger(__name__)

@task(name="RunExperiment")
def RunExperiment(execution, ide, inputFile='yes'):
    print("\n Executando o exp %s, algoritmo: %s" % (ide, execution))
    # os.system("if [! -d 'executions/']; then mkdir executions; fi")
    os.system("mkdir executions/" + str(ide))

    if(inputFile == 'yes'):
      os.system("wget http://200.201.194.150/experiments/downloadInputFile?id=" +
              str(ide) + " -O ./executions/" + str(ide) + "/input")
      start = time.time()
      os.system(execution + " executions/" + str(ide) + "/input > executions/" + str(ide) + "/output")
    else:
      start = time.time()
      os.system(execution + " > executions/" + str(ide) + "/output")
    dur = time.time() - start
    
    print (dur)
    
    files={'file': str("/executions/"+str(ide)+"/output")}
    path = str("executions/" + str(ide)+"/output")
    print (path)
    
    files = {'file': open(path, 'rb')}
    data = {'id':str(ide),'time':dur}
    
    r = requests.post('http://200.201.194.150/experiments/result', files=files,data=data)
    print (r.status_code, r.reason)
    
    return r.status_code
           # execution.status = 2
           # execution.save()
           # start = time.time()
           # os.system(query)
           # dur = time.time() - start
           # print dur
           # execution.status = 3
           # user = execution.request_by
           # user.notes.add(nota)
           # user.save()
           # execution.time = dur
           # execution.outputFile = queryOutputFile
           # execution.save()
