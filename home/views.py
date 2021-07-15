# from django.db.models.manager import RelatedManager
# from typing_extensions import Required
from django import http
from django.shortcuts import render, HttpResponse, redirect
# from home.models import Contact
from django.contrib import messages
from blog.models import Post
from django.contrib.auth.models import Group, User
from .decorators import unauthenticated_user, allowed_users
from django.contrib.auth import authenticate,  login, logout
from django.contrib.auth.decorators import login_required
import json
# Create your views here.
# User.objects.all().delete()


def home(request):
    return render(request, 'home/home.html')


def CovidUpdates(request):

        return render(request, 'home/Covid_Updates.html')

        







def Donors(request):
    return render(request, 'home/Donors.html')


def ContactUs(request):
    return render(request, 'home/contact_us.html')

    




@login_required(login_url='/Donors')
@allowed_users(allowed_roles=['Website_Admins'])
def Add(request):
    userl =[]    
    group = Group.objects.get(name='HospitalHeads')
    users = list(group.user_set.all())
    for user in users:
        userjson =user.first_name
        userdict = json.loads(userjson)
        if (userdict["Addedby_Username"] == request.user.username):
            userl.append(userdict)

    return render(request, 'home/Add_H_admin.html',{"u":userl})

  
      

   




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

        profileobj = {
            "Name": name,
            "username":username,
            "group": "hospitalh",
            "email":   hemail,
            "Add": haddress,
            "Addedby_Username":request.user.username,
        }

        myuserjson = json.dumps(profileobj)
        myuser.first_name = myuserjson
        # myuser.first_name='hospitalh'

        myuser.save()
        group = Group.objects.get(name='HospitalHeads')
        myuser.groups.add(group)
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
        profiledict = json.loads(profilejson)

        profileobj = {
            "Name": name,
            "username":username,
            "group": "H_Emp",
            "email":   hemail,
            "Hospital_name": profiledict["Name"],
            "Hospital_email": profiledict["email"],
            "Hospital_Add": profiledict["Add"],
            "Addedby_Username" : request.user.username,
        }

        myuserjson = json.dumps(profileobj)
        myuser.first_name = myuserjson

        myuser.save()
        group = Group.objects.get(name='Hospital_Employees')
        myuser.groups.add(group)
      
        return redirect('AddEmployee')

    profilejson = request.user.first_name
    profiledict = json.loads(profilejson)
    return render(request, 'home/AddEmp.html', {"profile": profiledict})


# Added Hospitals can sign in and add employees here




def handelLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('home')

# login page



# login for employee


def loginemp(request):
    if request.method == "POST":
        # Get the post parameters
        uusername = request.POST.get('uusername')
        upassword = request.POST.get('upassword')
        user = authenticate(username=uusername, password=upassword)
        if user is not None:
            profilejson =user.first_name
            profiledict = json.loads(profilejson)
            grp = profiledict["group"]
            if grp == "H_Emp":
               
                login(request, user)
                messages.success(request, "Successfully Logged In")
                return redirect('addpat')

            elif grp ==  "Covid_Survivor":
                login(request, user)
                messages.success(request, "Successfully Logged In")
                return redirect('Donors')
            elif grp == "User":
                login(request,user)
                messages.success(request, "Successfully Logged In")
                return redirect('Donors')
            elif grp =="hospitalh":
                login(request,user)
                messages.success(request, "Successfully Logged In")
                return redirect('AddEmployee')
            elif grp =="Website_Admins":
                login(request,user)
                messages.success(request, "Successfully Logged In")
                return redirect('Add')



            else:
                return HttpResponse("error occured")

        
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("ContactUs")

    return redirect('loginall')




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
        profiledict = json.loads(profilejson)

        profileobj = {
            "Name": name,
            "username":username,
            "group": "Covid_Survivor",
            "email":   pemail,
            "bloodgrp": pbloodgrp,
            "dateofdischarge": pdod,
            "age": p_age,
            "Hospital_name": profiledict["Hospital_name"],
            "Hospital_email": profiledict["Hospital_email"],
            "Hospital_Add": profiledict["Hospital_Add"],
            "Added_by_email": profiledict["email"],
            "Addedby_Username": request.user.username,

        }

        myuserjson = json.dumps(profileobj)
        myuser.first_name = myuserjson

        myuser.save()
        group = Group.objects.get(name='Covid_Survivors')
        myuser.groups.add(group)

        return redirect('addpat')

    profilejson =request.user.first_name
    profiledict = json.loads(profilejson)
    grp = profiledict["group"]
    return render(request, 'home/Add_patient.html', {"G":grp})


@login_required(login_url='/home')
def profile(request):
    profilejson = request.user.first_name
    profiledict = json.loads(profilejson)

    return render(request, 'home/profile.html', {"p": profiledict})

def nusignup(request):
    if request.method == "POST":

        username = request.POST.get('nuusername')
        name = request.POST.get('nuname')
        hemail = request.POST.get('nuemail')
       
        hid = request.POST.get('nuid1')
        hid2 = request.POST.get('nuid2')
        if(hid2 != hid):
            return redirect('Donors')
        myuser = User.objects.create_user(username, hemail, hid)

        profileobj = {
            "Name": name,
            "username":username,
            "group": "User",
            "email":   hemail,
            
        }
        myuserjson = json.dumps(profileobj)
        myuser.first_name = myuserjson
        # myuser.first_name='hospitalh'

        myuser.save()
        group = Group.objects.get(name='User')
        myuser.groups.add(group)
        return redirect('Donors')
    return render(request, 'home/nusignup.html')

def loginall(request):
    return render(request, 'home/loginpage.html')


#Deleting Users
@login_required(login_url='/home')
@allowed_users(allowed_roles=[ 'Website_Admins'])
def DelH(request, uH):
    group = Group.objects.get(name='HospitalHeads')
    users = list(group.user_set.all())
    Hospital = User.objects.get(username=uH)
    # print(Hospital.first_name)
    if Hospital in users:
        try:
            Hospital.delete()
            messages.sucess(request, "The user is deleted")
        except:
            messages.error(request, "The user not found") 
        return redirect("Add")


def DelE(request, uH):
    return HttpResponse("delete Employee")








