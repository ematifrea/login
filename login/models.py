from django.db import models

# Create your models here.

class User(models.Model):
    account_name = models.CharField(max_length=100, unique=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=50)
    token = models.CharField(max_length=25)
    active = models.BooleanField(default=False)
    last_login_date = models.DateTimeField()

    def __str__(self):
        return "Account_name: %s on user %s" % (self.account_name, self.full_name)