from django.db import models
from django.utils import timezone
import datetime

# Create your models here.

class User(models.Model):
    account_name = models.CharField(max_length=100, unique=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=50)
    last_login_date = models.DateTimeField()



    def __unicode__(self):
        return "Account_name: %s on user %s" % (self.account_name, self.full_name)

class UserActivation(models.Model):
    user = models.ForeignKey(User, unique=True)
    active = models.BooleanField(default=False)
    activation_key = models.CharField(max_length=10)
    key_expiration = models.DateTimeField(default=timezone.now()+datetime.timedelta(weeks=1))

    def __unicode__(self):
        return "Account_name: %s on user %s" % (self.account_name, self.full_name)

