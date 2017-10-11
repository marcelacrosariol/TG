from experiment.models import AppUser, Execution
from celery.utils.log import get_task_logger
from celery.decorators import task
import requests
import os
import time

logger = get_task_logger(__name__)

@task(name="RunExperiment")
def RunExperiment(execution, ide):
    print("\n Executando o exp %s, algoritmo: %s" % (ide, execution))
    os.system("if [! -d 'executions/']; then mkdir executions; fi")
    os.system("mkdir executions/" + str(ide))
    os.system("wget http://150.163.27.203:8000/experiments/downloadInputFile?id=" +
              str(ide) + " -O ./executions/" + str(ide) + "/input")
    start = time.time()
    os.system(execution + " executions/" + str(ide) + "/input > executions/" + str(ide) + "/output")
    dur = time.time() - start
    
    print (dur)
    files={'file': str("/executions/"+str(ide) + "/output")}
    path = str("executions/" + str(ide)+"/output")
    print (path)
    files = {'file': open(path, 'rb')}
    data = {'id':str(ide),'time':dur}
    #   r = requests.post('http://10.1.4.28:8000/about/')
    r = requests.post('http://150.163.27.203:8000/experiments/result', files=files,data=data)
    print (r.status_code, r.reason) 
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
