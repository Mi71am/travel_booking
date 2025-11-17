from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	# Add extra fields as needed, e.g. phone, address
	phone = models.CharField(max_length=20, blank=True)
	address = models.CharField(max_length=255, blank=True)
	profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

	def __str__(self):
		return self.user.username
