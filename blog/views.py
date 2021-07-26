from django.shortcuts import redirect, render, HttpResponse
from .models import Post
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import json
from django.contrib import messages
import datetime

# Post.objects.all().delete()

# Create your views here.


def blogHome(request):
    # getting posts in order
    # print(post)
    post = Post.objects.all().order_by('sno')

    # paginator obj created
    paginator = Paginator(post, 4)

    Page_number = request.GET.get('page')
    Page_obj = paginator.get_page(Page_number)
    messages.success(request, "Your message has been successfully sent")
    return render(request, 'blog/blogHome.html', {"page_obj": Page_obj})



def blogPost(request, mysno):
    post = Post.objects.filter(sno=mysno).first()
    if request.user.is_authenticated:
        userjson =request.user.first_name
        userdict = json.loads(userjson)
        return render(request, "blog/blogPost.html", {"post": post, "userp":userdict})
    return render(request, "blog/blogPost.html", {"post": post,})

  




@login_required(login_url='login')
def addblog(request):
    if request.method == "POST":
        # ingredients
        profilejson = request.user.first_name
        p = json.loads(profilejson)
        now = datetime.datetime.now()

        # adding data
        title = request.POST.get('Addblogt')
        author = p["Name"]
        authorUsername=request.user.username
        time = now
        content = request.POST.get('Addblogc')

        # saving
        if(content != "" or title != ""):
            post = Post(title=title, author=author,authorUsername=authorUsername,
                        Timestamp=time, content=content)
            post.save()
            # print(Post)
            return redirect('blogHome')
        else:
            return redirect("addblog")


    return render(request, 'blog/Addblog.html')
    
@login_required(login_url='/home')
def delblog(request, dsno):
    post = Post.objects.filter(sno=dsno).first()
    if(post.authorUsername == request.user.username):
        try:
            post.delete()
            
        except:
            print("wrong") 
        return redirect("blogHome")
    return HttpResponse("This blog belongs to someone else")





    



    
   

