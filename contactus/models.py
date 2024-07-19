from django.db import models

class Message(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50,null=False,blank=False)
    subject = models.CharField(max_length=100,null=False,blank=False)
    message = models.CharField(max_length=1000,null=False,blank=False)

class Meta:
    db_table = 'messages'