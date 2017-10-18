from django.contrib import admin
from .models import AppUser, Execution, Algorithm
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

# class AppUserAdminInline(admin.StackedInline):
# 	model = AppUser
# 	max_num = 1
# 	can_delete = False

# class UserAdmin(AuthUserAdmin):
# 	list_display = ['username', 'email']
# 	def add_view(self, *args, **kwargs):
# 		self.inlines = []
# 		return super(UserAdmin, self).add_view(*args, **kwargs)
	
# 	def change_view(self, *args, **kwargs):
# 		self.inlines = [AppUserAdminInline]
# 		return super(UserAdmin, self).change_view(*args, **kwargs)


class AppUserAdmin(admin.ModelAdmin):
	fields = ['nickname', 'usuario', 'company' , 'resultsPerPage', 'notification']
	list_display = ('nickname', 'usuario', 'company', 'date_register', 'last_access', 'resultsPerPage', 'notification')

class ExecutionAdmin(admin.ModelAdmin):
	fields = ['status','request_by', 'algorithm']
	list_display = ['request_by', 'algorithm', 'time', 'date_requisition', 'status', 'inputFile', 'outputFile']

class AlgAdmin(admin.ModelAdmin):
	fields = ['nameAlg', 'desc', 'command', 'sample', 'file']
	list_display = ['idAlg', 'nameAlg', 'desc', 'sample','file']

# # unregister old user admin
# admin.site.unregister(User)
# # register new user admin
# admin.site.register(User, UserAdmin)

admin.site.register(AppUser, AppUserAdmin)
admin.site.register(Execution, ExecutionAdmin)
admin.site.register(Algorithm, AlgAdmin)
