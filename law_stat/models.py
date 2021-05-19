from django.db import models

# Create your models here.

# 法律条文模型
class Provision(models.Model):
    compose_name = models.TextField('编',default= None)
    arrange_name = models.TextField('分编',default=None)
    chapter_name = models.TextField('章',default=None)
    section_name = models.TextField('节',default=None)
    provision_name = models.TextField('条',default=None)
    content = models.TextField('条文内容',default=None)