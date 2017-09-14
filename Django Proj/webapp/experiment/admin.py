from django.contrib import admin
from .models import AppUser, Execution, Algorithm

class AppUserAdmin(admin.ModelAdmin):
	fields = ['nickname', 'usuario', 'company' , 'resultsPerPage', 'notification']
	list_display = ('nickname', 'usuario', 'company', 'date_register', 'last_access', 'resultsPerPage', 'notification')

class ExecutionAdmin(admin.ModelAdmin):
	fields = ['status','request_by', 'algorithm']
	list_display = ['request_by', 'algorithm', 'time', 'date_requisition', 'status', 'inputFile', 'outputFile']

class AlgAdmin(admin.ModelAdmin):
	fields = ['nameAlg', 'desc', 'command', 'sample']
	list_display = ['idAlg', 'nameAlg', 'desc', 'sample']

# class NotesAdmin(admin.ModelAdmin):
# 	fields = ['user', 'execution']
# 	list_display = ['id','user',' executions']

admin.site.register(AppUser, AppUserAdmin)
admin.site.register(Execution, ExecutionAdmin)
admin.site.register(Algorithm, AlgAdmin)
