from django.shortcuts import redirect, render, HttpResponse
from django.urls.conf import path
from .models import Post, Report
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import json
from django.contrib import messages
import datetime
import os


# Report.objects.all().delete()
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
    # messages.success(request, "Your message has been successfully sent")
    return render(request, 'blog/blogHome.html', {"page_obj": Page_obj})



def blogPost(request, mysno):
    post = Post.objects.filter(sno=mysno).first()
    

    if request.user.is_authenticated:
        userjson =request.user.first_name
        try:
            userdict = json.loads(userjson)
            return render(request, "blog/blogPost.html", {"post": post, "userp":userdict})
        except:
            o = {
                "U":request.user.username
            }
            return render(request,"blog/blogPost.html", {"post": post,"userp":o})
    return render(request, "blog/blogPost.html", {"post": post})
  




# @login_required(login_url='login')
def addblog(request):
    if request.method == "POST":
        # # ingredients
        if(request.user.is_authenticated):
            profilejson = request.user.first_name
            
            try:
                p = json.loads(profilejson)
                now = datetime.datetime.now()

                # adding data
                title = request.POST.get('Addblogt')
                author = p["N"]
                authorUsername=request.user.username
                time = now
                content = request.POST.get('Addblogc')
                try:

                    # img = request.FILES['imgupload']
                    # print(img)

                    # saving
                    if(content != "" or title != ""):
                        post = Post(title=title, author=author,authorUsername=authorUsername,
                                    Timestamp=time,blog_img="img", content=content)
                        post.save()
                        # print(Post)
                        messages.success(request, "Blog Added")
                        return redirect('blogHome')
                    else:
                        messages.error(request, "Error occured")
                        return redirect("addblog")

                except:
                    if(content != "" or title != ""):
                        post = Post(title=title, author=author,authorUsername=authorUsername,
                                    Timestamp=time,blog_img="exampleImage", content=content)
                        post.save()
                        # print(Post)
                        messages.success(request, "Blog Added")

                        return redirect('blogHome')
                    else:
                        messages.error(request, "Error occured")

                        return redirect("addblog")





            except:
                now = datetime.datetime.now()

                # adding data
                title = request.POST.get('Addblogt')
                author = profilejson + " " + request.user.last_name
                authorUsername=request.user.username
                time = now
                content = request.POST.get('Addblogc')
                try:

                    img = request.FILES['imgupload']
                    # print(img)

                    # saving
                    if(content != "" or title != ""):
                        post = Post(title=title, author=author,authorUsername=authorUsername,
                                    Timestamp=time,blog_img=img, content=content)
                        post.save()
                        
                        messages.success(request, "Blog Added")

                        return redirect('blogHome')
                    else:
                        messages.error(request, "Error occured")
                        
                        return redirect("addblog")
                except:
                    if(content != "" or title != ""):
                        post = Post(title=title, author=author,authorUsername=authorUsername,
                                    Timestamp=time,blog_img="exampleImage", content=content)
                        post.save()
                        # print(Post)
                        messages.success(request, "Blog Added")

                        return redirect('blogHome')
                    else:
                        messages.error(request, "Error occured")

        
                        return redirect("addblog")
        else:
            return HttpResponse("login please")

    if(request.user.is_authenticated):
        return render(request, 'blog/Addblog.html')
    else:
        messages.error(request, "Please login to blog")
        return redirect('blogHome')

          
                    
            
            





    
@login_required(login_url='/home')
def delblog(request, dsno):

    if request.method == "POST":
        profilejson = request.user.first_name

        profiledict = json.loads(profilejson)
        post = Post.objects.filter(sno=dsno).first()
        rep = Report.objects.filter(blog_sno=dsno).all()

        if( profiledict["G"]=='e'):
            try:

                for r in rep:
                    r.delete()

                url ="./med/" +  str(post.blog_img)
                
                if os.path.exists(url):
                    os.remove(url)
                    print("deleted")
                else:
                    print("The file does not exist")
                post.delete()
                
                messages.success(request, "Blog Deleted")    
                return redirect('reportedblogs')
            except:
                print("wrong") 
                return redirect('reportedblogs')
        return HttpResponse("This blog belongs to someone else")  
                
    else:
        profilejson = request.user.first_name
        try:

            profiledict = json.loads(profilejson)
            post = Post.objects.filter(sno=dsno).first()
            rep = Report.objects.filter(blog_sno=dsno).all()

            from_rep = False

            if(profiledict["G"]=='e' or request.user.username == post.authorUsername):
                try:
                    for r in rep:
                        r.delete()
                

                    
                    url ="./med/" +  str(post.blog_img)
                    if os.path.exists(url):
                        os.remove(url)
                        print("deleted")
                    else:
                        print("The file does not exist")
                    post.delete()
                    messages.success(request, "Blog Deleted")    
        
                    return redirect("blogHome")
                    
                except:
                    print("wrong") 
                
                    return redirect("blogHome")
        except:
            post = Post.objects.filter(sno=dsno).first()
            rep = Report.objects.filter(blog_sno=dsno).all()

            from_rep = False

            if(post.authorUsername == request.user.username):
                try:
                    for r in rep:
                        r.delete()
                

                    
                    url ="./med/" +  str(post.blog_img)
                    if os.path.exists(url):
                        os.remove(url)
                        print("deleted")
                    else:
                        print("The file does not exist")
                    post.delete()
                    messages.success(request, "Blog Deleted")    
        
                    return redirect("blogHome")
                    
                except:
                    print("wrong") 
                
                    return redirect("blogHome")

            
          
                
        
        
        
        return HttpResponse("This blog belongs to someone else")
        
    
    


# @login_required(login_url='/home')
def repblog(request, rsno):
    post = Post.objects.filter(sno=rsno).first()
    # print(post)
    if(request.user.is_authenticated):
        blog_sno=rsno
        rep_by = request.user.username
        # author = post.author
        now = datetime.datetime.now()
        title = post.title
        author = post.author
        reason = request.POST.get('reason')

        if(reason != ""):
            rep = Report(blog_sno=blog_sno,title = title,author=author, rep_by=rep_by,Timestamp=now, report=reason)
            rep.save()
            messages.success(request, "Blog Reported")
            return redirect("blogHome")
        else:
            messages.error(request, "Error occured")

            return redirect("blogHome")
    else:
        messages.error(request, "Please login to Report")
        return redirect('blogHome')

    






    



    
   

