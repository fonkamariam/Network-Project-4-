from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Follow(models.Model):
    name= models.ForeignKey(User, on_delete=models.CASCADE, related_name="name")
    followers=models.ManyToManyField(User, related_name="followers", blank=True, null=True)
    following=models.ManyToManyField(User, related_name="following", blank=True, null=True)
    def __str__(self):
        return f"{self.name} follow data"

class Posts(models.Model):  
    owner= models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    text= models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    like= models.IntegerField(default=0, blank=True,null=True)
    def __str__(self):
        return f"{self.id} - {self.owner} at {self.timestamp.strftime('%b %d %Y, %I:%M %p')}"
class Like(models.Model):
    liker=models.ForeignKey(User, on_delete=models.CASCADE, related_name="liker")
    liked=models.ManyToManyField(Posts,related_name="liked",blank=True, null=True)
    def __str__(self):
        return f"{self.liker} Like data"
    



    
