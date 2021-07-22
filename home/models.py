from django.db import models
from django.contrib.auth.models import Group, User


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE),
    uniqueid = models.AutoField(primary_key=True),
    Name = models.CharField(max_length=50),
    Hospital = models.CharField(max_length=255),
    Group = models.CharField(max_length=130),
    email = models.TextField(),
    timeStamp = models.DateTimeField(blank=True),

    def __str__(self):
        return f'{self.user.username} Profile'

class Comment(models.Model):
    id=models.AutoField(primary_key=True)
    fname=models.CharField(max_length=50)
    lname=models.CharField(max_length=50)
    authorUsername=models.CharField(max_length=50, default="")
    email=models.CharField(max_length=70)
    comment=models.TextField()
    
    Timestamp=models.CharField(max_length=50)


    def __str__(self):
        return self.fname
class Message(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)
    authorUsername=models.CharField(max_length=50, default="")
    email=models.CharField(max_length=70)
    message=models.TextField()
    Timestamp=models.CharField(max_length=50)
    
    def __str__(self):
        return self.name + str(self.id)




