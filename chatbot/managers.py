from django.db import models

class cbotManager(models.Manager):
	def user(self, request):
		""" Returns only results owned by the current user, or all if super admin """
		return super(cbotManager, self).get_queryset().filter(author=request.user)

class configManager(models.Manager):
	def user(self, request):
		""" Returns only results owned by the current user, or all if super admin """
		#return super(configManager, self).get_queryset().filter(models.Q(author=request.user) | models.Q(is_public=True))  ## For public showing, temporarily disabled
		return super(configManager, self).get_queryset().filter(author=request.user)

class fileManager(models.Manager):
	def user(self, request):
		""" Returns only results owned by the current user, or all if super admin """
		return super(fileManager, self).get_queryset().filter(author=request.user)