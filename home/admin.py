from django.contrib import admin
from .models import Profile
from .models import Comment
from .models import Message

# Register your models here.
admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(Message)
