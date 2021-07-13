from django.db import models

# Create your models here.
class Post(models.Model):
    sno=models.AutoField(primary_key=True)
    title=models.CharField(max_length=255)
    author=models.CharField(max_length=50)
    Timestamp=models.CharField(max_length=50)
    content=models.TextField()

    def __str__(self):
        return self.title + " by " + self.author