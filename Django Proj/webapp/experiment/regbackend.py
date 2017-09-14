# from registration.views import RegistrationView
from registration.backends.default.views import RegistrationView, ActivationView
from experiment.forms import AppUserForm
from experiment.models import AppUser

class MyRegistrationView(RegistrationView):

	form_class = AppUserForm
	success_url = "complete"

	def register(self, form_class):
		new_user = super(MyRegistrationView,self).register(form_class)
		user_profile = AppUser()
		user_profile.usuario = new_user
		user_profile.nickname = form_class.cleaned_data['nickname']
		user_profile.company = form_class.cleaned_data['company']
		user_profile.save()
		return user_profile
