from django.db import models

# Create your models here.
class userinfo(models.Model):
    Id = models.AutoField(primary_key=True)
    Email = models.EmailField(null=False)
    Pass = models.CharField(null=False)
    Username = models.CharField(null=False)
