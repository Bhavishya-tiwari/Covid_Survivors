# from django.db.models.manager import RelatedManager
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


def AddHospital(request):
    if request.method == "POST":
        adminid = request.POST['adminid']
        adminpassword = request.POST['adminpassword']

        if adminid == 'q@q' and adminpassword == 'q':
            return render(request, 'home/Add_H_admin.html')

    return render(request, 'home/Add_Hospital.html')


# @login_required(login_url='')
# @allowed_users(['Hospital_Heads', 'Website_Admins'])
# def AddHospital(request):
#     return render(request,'home/Add_H_admin.html' )


# Adding Hospitals here (Hosital_Heads)

# yaha na koi restriction lagana
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
            "group": "hospitalh",
            "email":   hemail,
            "Add": haddress,
        }

        myuserjson = json.dumps(profileobj)
        # print(myuserjson)
        myuser.first_name = myuserjson
        # myuser.first_name='hospitalh'

        myuser.save()
        group = Group.objects.get(name='HospitalHeads')
        myuser.groups.add(group)
        # print(myuser)
        # print(group)
        return redirect('AddHospital')


@login_required(login_url='/home')
@allowed_users(allowed_roles=['admin', 'HospitalHeads'])
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
            "group": "H_Emp",
            "email":   hemail,
            "Hospital_name": profiledict["Name"],
            "Hospital_email": profiledict["email"],
            "Hospital_Add": profiledict["Add"],
        }

        myuserjson = json.dumps(profileobj)
        # print(myuserjson)
        myuser.first_name = myuserjson

        myuser.save()
        group = Group.objects.get(name='Hospital_Employees')
        myuser.groups.add(group)
        # print(myuser)
        # print(group)
        return redirect('AddEmployee')

    profilejson = request.user.first_name
    profiledict = json.loads(profilejson)
    # print(profiledict)
    return render(request, 'home/AddEmp.html', {"profile": profiledict})


# Added Hospitals can sign in and add employees here

def AddEmp(request):
    if request.method == "POST":
        # Get the post parameters
        loginusername = request.POST.get('hnamecheck')
        loginpassword = request.POST.get('hidcheck')
        # print(loginusername)
        user = authenticate(username=loginusername, password=loginpassword)
        # print(user)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("AddEmployee")
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("ContactUs")

    return HttpResponse("404- Not found")


def handelLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('home')

# login page


def loginall(request):
    return render(request, 'home/loginpage.html')

# login for employee


def loginemp(request):
    if request.method == "POST":
        # Get the post parameters
        empusername = request.POST.get('empusername')
        emppassword = request.POST.get('emppassword')
        # print(loginusername)
        user = authenticate(username=empusername, password=emppassword)
        # print(user)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect('addpat')
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("ContactUs")

    return redirect('loginall')


# handel login of user
def loginuser(request):
    if request.method == "POST":
        # Get the post parameters
        patusername = request.POST.get('patusername')
        patpassword = request.POST.get('patpassword')
        # print(loginusername)
        user = authenticate(username=patusername, password=patpassword)
        # print(user)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect('Donors')
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("ContactUs")
    return redirect('loginall')

# login employees can add patients


@login_required(login_url='/home')
@allowed_users(allowed_roles=['admin', 'Hospital_Employees'])
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
        print(pid1)
        myuser = User.objects.create_user(username, pemail, pid1)
        profilejson = request.user.first_name
        profiledict = json.loads(profilejson)

        profileobj = {
            "Name": name,
            "group": "Covid_Survivor",
            "email":   pemail,
            "bloodgrp": pbloodgrp,
            "dateofdischarge": pdod,
            "age": p_age,
            "Hospital_name": profiledict["Hospital_name"],
            "Hospital_email": profiledict["Hospital_email"],
            "Hospital_Add": profiledict["Hospital_Add"],
            "Added_by_email": profiledict["email"],

        }

        myuserjson = json.dumps(profileobj)
        # print(myuserjson)
        myuser.first_name = myuserjson

        myuser.save()
        group = Group.objects.get(name='Covid_Survivors')
        myuser.groups.add(group)
        # print(myuser)
        # print(group)
        return redirect('addpat')

    # print(profiledict)
    return render(request, 'home/Add_patient.html')


@login_required(login_url='/home')
def profile(request):
    profilejson = request.user.first_name
    profiledict = json.loads(profilejson)

    return render(request, 'home/profile.html', {"p": profiledict})
