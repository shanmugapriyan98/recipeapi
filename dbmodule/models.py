from django.db import models

# Create your models here.
class Recipe(models.Model):
  id = models.AutoField(
    primary_key=True
  )

  text = models.TextField(
    max_length=1000,
    null=False,
    blank=False
  )

  name = models.TextField(
    max_length=20,
    null=False,
    blank=False
  )

  class Meta:
    db_table = 'Recipe'