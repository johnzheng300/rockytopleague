from PIL import Image
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE) #on_delete=models.CASCADE means if user is deleted, the profile is too, one way
	image = models.ImageField(default='default.jpg', upload_to='profile_pics')

	def __str__(self):
		return f'{self.user.username} Profile'

	def save(self, *args, **kwargs):
		super(Profile, self).save(*args, **kwargs)
		img = Image.open(self.image.path)

		if img.height > 300 or img.width > 300:
			img.thumbnail((300, 300))
			img.save(self.image.path)