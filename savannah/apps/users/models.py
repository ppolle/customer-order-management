from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
# Create your models here.


class User(AbstractUser):
    name = models.CharField(_("Name of User"), blank=True,
                            null=True, max_length=255)
    phone_number = models.CharField(
        _("Phone Number"), blank=True, null=True, max_length=255)
    profile_picture = models.CharField(blank=True, null=True, max_length=255)
    
    class Meta:
        ordering = ['-id']
