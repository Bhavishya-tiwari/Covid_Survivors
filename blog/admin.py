from django.contrib import admin
from blog.models import Post, Report
# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display =['sno', 'title', 'author', 'Timestamp', 'content']
@admin.register(Report)
class PostAdmin(admin.ModelAdmin):
    list_display =['rno', 'blog_sno', 'author', 'Timestamp', 'report']

