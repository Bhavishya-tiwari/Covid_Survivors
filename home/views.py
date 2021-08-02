# from django.db.models.manager import RelatedManager
# from typing_extensions import Required
from django import http
from django.http import response
from django.shortcuts import render, HttpResponse, redirect
# from home.models import Contact
from django.contrib import messages
from django.core.paginator import Paginator
from blog.models import Post,Report
from home.models import Comment,Message
from django.contrib.auth.models import Group, User
from .decorators import unauthenticated_user, allowed_users
from django.contrib.auth import authenticate,  login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
import json
import datetime
import requests

# Create your views here.
# User.objects.all().delete() 
# Message.objects.all().delete()

def home(request):
    if request.method == "POST":
        profilejson = request.user.first_name
        try:
            profiledict = json.loads(profilejson)
            
            
            now = datetime.datetime.now()
            name = profiledict["N"]
            username = request.user.username
            email = request.user.email
            msg = request.POST.get('msg')
            Query = Message( authorUsername=username,email=email,name=name,
                            Timestamp=now, message=msg)
                            #   why email vroo
            if(msg != ""):
                Query.save()
                return HttpResponse("done")
            else:
                return HttpResponse("error")
        except:
            now = datetime.datetime.now()
            name = profilejson + " " + request.user.last_name
            username = request.user.username
            email = "example@email"
            msg = request.POST.get('msg')
            Query = Message( authorUsername=username,email=email,name=name,
                            Timestamp=now, message=msg)
                            #   why email vroo
            if(msg != ""):
                Query.save()
                return HttpResponse("done")
            else:
                return HttpResponse("error")



    return render(request, 'home/home.html')


def CovidUpdates(request):
    return render(request, 'home/Covid_Updates.html')

def loging(request):
    return render(request, 'home/logingoogle.html')

def reportedblogs(request):
    post = Report.objects.all().order_by('rno')
    li = []
        # {sno= sno,
        # reps = [{}, {}, {}]

        # }

    for p in post:
        # print(p.blog_sno)
        p_in_l=False 
        for l in li:
            if ( p.blog_sno == l["sno"]):
                p_in_l=True
                o1 ={ 
                "name":p.rep_by,
                "rep" : p.report,
                "time" : p.Timestamp,
                
                    }
                l["reps"].append(o1)

        if(p_in_l == False):
            o = {
            "sno" : p.blog_sno,
            "title" : p.title,
            "author":p.author,
            "reps":[{
                        "name":p.rep_by,
                        "rep" : p.report,
                        "time" : p.Timestamp,
                                            }]
                                
                }
            li.append(o)

    return render(request, 'home/Blog_r.html', {"r":li})

            

        




def chat(request):

    new_list=[]
    # old_list[-1]=new_list
    msgs = Message.objects.all().order_by('id')
    # obj=[{"n":"l"},{"k":"kk"}]
    for msg in msgs:
        obj ={"name": msg.name,
                "msg":msg.message,
                "un":msg.authorUsername,
                "time":msg.Timestamp
        }
        new_list.append(obj)
        # print(obj)
    return HttpResponse(json.dumps(new_list))
    
        
        
        
            
    
   




def Donors(request):
    if request.method=="POST":
        bg_val = request.POST.get('Blood_grp_val', '')
        try:
            group = Group.objects.get(name='Covid_Survivors')
            users = list(group.user_set.all())
            CSsend = []
            for user in users:
                CSdict = json.loads(user.first_name)
                CSdict2 = json.loads(user.last_name)
                # print("kd")
               
                if( CSdict["B"] == bg_val):
                    print("osi")
                    ob = {
                    "name" : CSdict["N"],
                    "email" : CSdict2["E"],
                    "Hospital_name" : CSdict2["A"],
                    "Hospital_email" : CSdict2["Y"],
                    }
                    CSsend.append(ob)
                    print(CSdict["N"],CSdict2["E"])
                    # print(CSdict["N"],CSdict2[])
                else:    
                    print("K")
            
            return HttpResponse(json.dumps(CSsend))
        except Exception as e:
            return HttpResponse('Error Occured')
    # print(request.user)
    return render(request, 'home/Donors.html')
                   
def ContactUs(request):
    if request.method == "POST":

        now = datetime.datetime.now()


        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        authorUsername=request.user.username
        email = request.POST.get('email')
        c = request.POST.get('comment')
        if(email != "" or c != ""):
            Query = Comment(fname=fname, lname=lname,email=email, authorUsername=authorUsername,
                        Timestamp=now, comment=c)
            Query.save()

            messages.success(request, "Thanks for your feedback")
            return redirect("ContactUs")    
        else:
            messages.error(request, "error occured!!")
            return redirect("ContactUs")    
    return render(request, 'home/contact_us.html')
                    

                

                
        



   
    
    






     
     

@login_required(login_url='/Donors')
@allowed_users(allowed_roles=['Website_Admins', 'HospitalHeads', 'Hospital_Employees'])
def commentshow(request):
    # getting posts in order
    cmn = Comment.objects.all().order_by('id')

    # paginator obj created
    paginator = Paginator(cmn, 2)

    Page_number = request.GET.get('page')
    Page_obj = paginator.get_page(Page_number)
    return render(request, 'home/Commentshow.html', {"page_obj": Page_obj})

    




@login_required(login_url='/Donors')
@allowed_users(allowed_roles=['Website_Admins'])
def Add(request):
    userl =[]    
    group = Group.objects.get(name='HospitalHeads')
    users = list(group.user_set.all())
    for user in users:
        userjson1 =user.first_name
        userjson =user.last_name
        userdict1 = json.loads(userjson1)
        userdict = json.loads(userjson)
        if (userdict["Au"] == request.user.username):
            userl.append(userdict1)

    return render(request, 'home/Add_H_admin.html',{"u":userl})

  
      

   



# done
@login_required(login_url='/Donors')
@allowed_users(allowed_roles=['Website_Admins'])
def AddHadmin(request):
    if request.method == "POST":

        username = request.POST.get('husername')
        name = request.POST.get('hname')
        hemail = request.POST.get('hemail')
        haddress = request.POST.get('hadd')
        hid = request.POST.get('pass1')
        hid2 = request.POST.get('pass2')
        if(hid2 != hid):
            return redirect('addhospital')
        myuser = User.objects.create_user(username, hemail, hid)

        profileobj1 = {
            "N":name,"U":username,"G":"h","E":hemail,
        }
        pro2={    "A":haddress,"Au":request.user.username,}

        myuserjson = json.dumps(profileobj1)
        myuserjson2 = json.dumps(pro2)
        myuser.first_name = myuserjson
        myuser.last_name = myuserjson2
        # myuser.first_name='hospitalh'

        myuser.save()
        group = Group.objects.get(name='HospitalHeads')
        myuser.groups.add(group)
        messages.success(request, "New Hospital Added")
        return redirect('Add')
       


@login_required(login_url='/home')
@allowed_users(allowed_roles=[ 'HospitalHeads'])
def AddEmployee(request):
    if request.method == "POST":
        username = request.POST.get('eusername')
        name = request.POST.get('ename')
        hemail = request.POST.get('eemail')
        hid = request.POST.get('epass1')
        hid2 = request.POST.get('epass2')
        if(hid2 != hid):
            return HttpResponse('password not match')
        myuser = User.objects.create_user(username, hemail, hid)
        profilejson = request.user.first_name
        profilejson2 = request.user.last_name
        profiledict = json.loads(profilejson)
        profiledict2 = json.loads(profilejson2)

        profileobj1 = {
            "N": name,"U":username,"G": "e","E":   hemail,
        }
        pro2 = {
            "X": profiledict["N"],"Y": profiledict["E"],"Z": profiledict2["A"],
            "Au" : request.user.username,}

        myuserjson = json.dumps(profileobj1)
        myuserjson2 = json.dumps(pro2)
        myuser.first_name = myuserjson
        myuser.last_name = myuserjson2

        myuser.save()
        group = Group.objects.get(name='Hospital_Employees')
        myuser.groups.add(group)
        messages.success(request, "New Employee Added")
        return redirect('AddEmployee')
    userl =[]    
    group = Group.objects.get(name='Hospital_Employees')
    users = list(group.user_set.all())
    for user in users:
        userjson =user.first_name
        userjson2 =user.last_name
        userdict1 = json.loads(userjson)
        userdict2 = json.loads(userjson2)
        userdict = {
            "N":userdict1["N"],"U":userdict1["U"],"E":userdict1["E"],
            "Au":userdict2["Au"],"G":userdict1["G"],
        }
        if (userdict["Au"] == request.user.username):
            userl.append(userdict)






    return render(request, 'home/AddEmp.html',{"u":userl})
  






# Logout
def handelLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('home')



# Login
def loginemp(request):
    if request.method == "POST":
        # Get the post parameters
        print("svi")
        uusername = request.POST.get('uusername')
        upassword = request.POST.get('upassword')
        user = authenticate(username=uusername, password=upassword)
        if user is not None:
            profilejson =user.first_name
            profiledict = json.loads(profilejson)
            grp = profiledict["G"]
            if grp == "e":
               
                login(request, user)
                messages.success(request, "Successfully Logged In")
                return redirect('addpat')

            elif grp ==  "c":
                login(request, user)
                messages.success(request, "Successfully Logged In")
                return redirect('Donors')
            elif grp == "u":
                login(request,user)
                messages.success(request, "Successfully Logged In")
                return redirect('Donors')
            elif grp =="h":
                login(request,user)
                messages.success(request, "Successfully Logged In")
                return redirect('AddEmployee')
            elif grp =="Wa":
                login(request,user)
                messages.success(request, "Successfully Logged In")
                return redirect('Add')
            else:
                return HttpResponse("error occured")
        else:
            messages.error(request, "Invalid credentials!")
            return redirect("login")
    return redirect('login')

        










# login employees can add patients
@login_required(login_url='/home')
@allowed_users(allowed_roles=[ 'Hospital_Employees'])
def addpat(request):
    if request.method == "POST":
        username = request.POST.get('pusername')
        name = request.POST.get('pname')
        pemail = request.POST.get('pemail')
        pbloodgrp = request.POST.get('pbloodgrp')
        pdod = request.POST.get('pdod')
        p_age = request.POST.get('p_age')
        pid1 = request.POST.get('pid1')
        pid2 = request.POST.get('pid2')
        if(pid2 != pid2):
            return HttpResponse('password not match')
        myuser = User.objects.create_user(username, pemail, pid1)
        profilejson = request.user.first_name
        profilejson2 = request.user.last_name
        profiledict = json.loads(profilejson)
        profiledict2 = json.loads(profilejson2)

        profileobj1 = {
            "N": name,
            "U":username,
            "G": "c",
            "B": pbloodgrp,
            "D": pdod,
            "n": p_age,
        }
        pro2={
            "A": profiledict2["X"],
            "Y": profiledict2["Y"],
            "Ae": profiledict["E"],
            "Au": request.user.username,"E":pemail,}


        myuserjson = json.dumps(profileobj1)
        myuserjson2 = json.dumps(pro2)
        myuser.first_name = myuserjson
        myuser.last_name = myuserjson2

        myuser.save()
        group = Group.objects.get(name='Covid_Survivors')
        myuser.groups.add(group)
        messages.success(request, "Donor Added")
        return redirect('addpat')
    userl =[]    
    group = Group.objects.get(name='Covid_Survivors')
    users = list(group.user_set.all())
    for user in users:
        userjson =user.first_name
        userjson2 =user.last_name
        userdict = json.loads(userjson)
        userdict2 = json.loads(userjson2)
        if (userdict2["Au"] == request.user.username):
            userl.append(userdict)

  
    return render(request, 'home/Add_patient.html', {"u":userl})


@login_required(login_url='/home')
def profile(request):
    userjson2 =request.user.first_name
    try:
        userdict = json.loads(userjson2)
        profilejson1 = request.user.first_name
        profilejson2 = request.user.last_name
        profiledict1 = json.loads(profilejson1)
        profiledict2 = json.loads(profilejson2)
        return render(request, 'home/profile.html', {"p1":profiledict1,"p2":profiledict2, "gg":False})
    except:
        o = {
            "fn":userjson2,
            "ln": request.user.last_name,
            "em":request.user.email,
            "gg":True
        }
        return render(request, 'home/profile.html', o)
        # return HttpResponse("mk")


    
    
  




# def nusignup(request):
#     if request.method == "POST":

#         username = request.POST.get('nuusername')
#         name = request.POST.get('nuname')
#         hemail = request.POST.get('nuemail')
       
#         hid = request.POST.get('nuid1')
#         hid2 = request.POST.get('nuid2')
#         if(hid2 != hid):
#             return redirect('Donors')
#         myuser = User.objects.create_user(username, hemail, hid)

#         profileobj = {
#             "N": name,
#             "U":username,
#             "G": "u",
#             "E":   hemail,
            
#         }
#         pro2 = {}
#         myuserjson = json.dumps(profileobj)
#         myuserjson2 = json.dumps(pro2)
#         myuser.first_name = myuserjson
#         myuser.last_name = myuserjson2
#         # myuser.first_name='hospitalh'

#         myuser.save()
#         group = Group.objects.get(name='User')
#         myuser.groups.add(group)
#         return redirect('Donors')
#     return render(request, 'home/nusignup.html')

def loginall(request):
    return render(request, 'home/loginpage.html')


#Deleting Users
@login_required(login_url='/home')
@allowed_users(allowed_roles=[ 'Website_Admins'])
def DelH(request, uH):
    group = Group.objects.get(name='HospitalHeads')
    users = list(group.user_set.all())
    Hospital = User.objects.get(username=uH)
    if Hospital in users:
        userjson =Hospital.last_name
        userdict = json.loads(userjson)
        if(userdict["Au"]==request.user.username):
            try:
                Hospital.delete()
                messages.success(request, "Hospital Deleted")
                return redirect("Add")

            except:
                messages.error(request, "hospital not Found") 
                return redirect("Add")


# Deleting employees
@login_required(login_url='/home')
@allowed_users(allowed_roles=[ 'HospitalHeads'])
def DelE(request, uE):
    group = Group.objects.get(name='Hospital_Employees')
    users = list(group.user_set.all())
    Employee = User.objects.get(username=uE)
    if Employee in users:
        userjson =Employee.last_name
        userdict = json.loads(userjson)
        if(userdict["Au"]==request.user.username):
            try:
                Employee.delete()
                messages.success(request, "Employee deleted")
                return redirect("AddEmployee")

            except:
                messages.error(request, "Employee not found") 
                return redirect("AddEmployee")



# Deleting employees
@login_required(login_url='/home')
@allowed_users(allowed_roles=[ 'Hospital_Employees'])
def DelCS(request, uCS):
    group = Group.objects.get(name='Covid_Survivors')
    users = list(group.user_set.all())
    CSur = User.objects.get(username=uCS)
    if CSur in users:
        userjson =CSur.last_name
        userdict = json.loads(userjson)
        if(userdict["Au"]==request.user.username):
            try:
                CSur.delete()
                messages.sucess(request, "Donor deleted")
                return redirect("addpat")

            except:
                messages.error(request, "Donor not found") 
                return redirect("addpat")
    


        






