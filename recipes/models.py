from django.db import models

class Recipe(models.Model):
  id = models.AutoField(primary_key=True)
  name = models.TextField(max_length=50,null=False,blank=False)
  info = models.TextField(max_length=1000,null=False,blank=False)

  class Meta:
    db_table = 'recipe'