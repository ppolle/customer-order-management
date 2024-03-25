from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
# Create your models here.


class User(AbstractUser):
    # First Name and Last Name do not cover name patterns
    # around the globe.
    password = models.CharField(
        _('password'), max_length=128, default="set_password")
    name = models.CharField(_("Name of User"), blank=True,
                            null=True, max_length=255)
    phone_number = models.CharField(
        _("Phone Number"), blank=True, null=True, max_length=255)
    profile_picture = models.ImageField(
        upload_to='user_profile_pictures', blank=True, null=True)
    
    class Meta:
        ordering = ['-id']
