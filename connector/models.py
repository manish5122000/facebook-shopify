# from pyexpat import model
from django.db import models
import jsonfield
# from django.contrib.postgres.fields import ArrayField
# import jsonfield
# Create your models here.

class confi(models.Model):
    shop_name = models.CharField(default=False,max_length=1000)

class facebookresponce(models.Model):
    data = models.CharField(max_length=10000)
    
class Products(models.Model):

    _id = models.IntegerField(null = False)
    title = models.CharField(null = False, max_length=50)
    vendor = models.CharField(null = False, max_length=50)
    variants = jsonfield.JSONField()
    # class Meta:
    #     verbose_name = _("")
    #     verbose_name_plural = _("s")

    def __str__(self):
        return self.vendor 

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})
class app_shop(models.Model):
    _id = models.AutoField(primary_key=True)
    shop_name = models.CharField(null=False,max_length=99)
    access_token = models.CharField(null=False,max_length=99)
    def __str__(self):
        return self.shop_name

class user_details(models.Model):
    user_id = models.IntegerField(null=False)
    shop_name= models.CharField(max_length=99)
    marketplace =   jsonfield.JSONField()
