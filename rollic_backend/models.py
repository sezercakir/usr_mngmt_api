from django.db import models

class User(models.Model):
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250, unique=True, null=False)
    email = models.EmailField(max_length=250, unique=True, null=False)
    password = models.CharField(max_length=250)
    
    
    def __str__(self) -> str:
        return self.name