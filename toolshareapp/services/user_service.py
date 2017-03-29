from django.db.models import Q

from toolshareapp.models import User
from django.contrib.auth.models import User as SystemUser
from toolshareapp.models.user_role import UserRole
from toolshareapp.services import ToolService
from toolshareapp.services import ShedService

toolService = ToolService()
shedService = ShedService()

class UserService:

	def register(self, user):
		system_user = SystemUser.objects.create_user(user.email,
									   user.email,
									   user.password)
		system_user.save()
		user.register(system_user)
		user.save()
		return user
		
	def update(self, user):
		
		orig = User.objects.get(id = user.id)
		
		if orig.zip_code != user.zip_code:
			for tool in toolService.get_tools_owned_by_user(user.id):
				toolService.withhold(tool.id)
			
			if self.has_shed(user.id):
				shed = shedService.get_shed_by_user(user.id)
				shedService.deregister(shed.id)
		
		user.save()
		
	def deactivate(self, user_id):
		user = User.objects.get(pk=user_id)
		user.deactivate()
		user.save()
		return user
	
	def ResetPassword(self, user):
		user.set_password('new password')
		user.save()
	def ChangeUserRole(self, user):
		user.role = UserRole.objects.get(description)
		user.save()
		
	def get_users(self, search_term, user_id):
		user = User.objects.get(id=user_id)
		users = User.objects.filter(active=True).filter(zip_code=user.zip_code)
		
		if search_term:
			users = users.filter(
				Q(name__contains = search_term) |
				Q(lastname__contains = search_term) |
				Q(email__contains = search_term)
			)
			
		return users
	
	def get_user(self, user_id):
		return User.objects.get(id=user_id)
	
	def get_user_by_email(self, email):
		return User.objects.get(email=email)
	
	def has_shed(self, user_id):
		user = self.get_user(user_id)
		return user.shed_set.exclude(active=False).count() > 0
	
	def get_preferred_pickup_location(self, user_id):
		return self.get_user(user_id).preferred_pickup_location