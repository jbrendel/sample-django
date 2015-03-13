from django.db import models

# Create your models here.

class FileStorage(models.Model):
    name  = models.CharField(max_length=120, db_index=True, blank=True,
                             null=True, unique=True)
    blob  = models.TextField()

