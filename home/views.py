# from django.db.models.manager import RelatedManager
# from typing_extensions import Required
from os import pipe
from django import http
from django.db import reset_queries
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

def v(p):
    if(len(p)>5):
        if(" " in p):
            return False
        else:
            return True
    else:
        return False
def l(p):
    if(len(p)<1):
        return False
    else:
        return True

def home(request):
   
    return render(request, 'home/home.html')



def CovidUpdates(request):
    return render(request, 'home/Covid_Updates.html')


def setappointment(request, HuN):
    if(request.user.is_authenticated):

        group = Group.objects.get(name='HospitalHeads')
        users = list(group.user_set.all())
        Hospital = User.objects.get(username=HuN)
        hospitalusername= Hospital.username
       

        clear = False
        username = hospitalusername
        

        msgs = Message.objects.filter(email = "Appointment@hospital").all()
        byuser = []
        # print(msgs)
        for m in msgs:
        
            if(m.Timestamp == request.user.username):
                byuser.append(m)
        if(byuser == []):
            clear =True
        
        
        for a in byuser:
            ms = a.message
            if("BloodDonated" in ms):
                clear =True
            else:
                clear=False
                break
        print(clear)
        
        projson = request.user.first_name
        try:
            prodict = json.loads(projson)
            if( prodict["G"] == "Wa" or prodict["G"] == "h" or prodict["G"] == "e" or prodict["G"] == "c"):
                messages.error(request, "contact Hospital")
                return redirect('Donors')
            else:
                messages.error(request, "contact Hospital/Employee")
                return redirect('Donors')

        except:
            name = request.user.first_name+ " " + request.user.last_name
            email = "Appointment@hospital"
            msg ="Emp will send msg from here"
            now = request.user.username
            if(clear):
                Query = Message( authorUsername=username,email=email,name=name,
                                            Timestamp=now, message=msg)
                Query.save()
                            
                messages.success(request, "Appointment request sent")
                return redirect('Donors')
            else:
                messages.error(request, "Your Appointment is already set")
                return redirect('Donors')
            

                

                

            
            


    else:
        messages.error(request, "Please login for appointment")
        return redirect('login')



@allowed_users(allowed_roles=['Hospital_Employees'])
def setappointmentpage(request):
    empprofjson = request.user.last_name
    empprofobj = json.loads(empprofjson)
    hospitalusername= empprofobj["Au"]
    msgs = Message.objects.all()
    Appointments = []
    for Appointment in msgs:
        if(Appointment.email == "Appointment@hospital" and Appointment.message == "Emp will send msg from here"):
            o={
                "Appby":Appointment.Timestamp,
                "Appbyname":Appointment.name,
            }
            Appointments.append(o)


  
    return render(request, 'home/giveappointments.html', {"App":Appointments})

def appointmentdatesetted(request, DuN):
    if request.method=="POST":
        Appointmentdatee = request.POST.get('AppointmentDate')
        # print(Appointmentdatee)

        msgs = Message.objects.filter(Timestamp = DuN).last()
        print(msgs)
        st =  "AppSeted" +  str(Appointmentdatee)
        msgs.message = st
        msgs.save()
        return redirect('setappointmentpage')
                

@allowed_users(allowed_roles=['Hospital_Employees'])
def appointmentsshown(request):
    empprofjson = request.user.last_name
    empprofobj = json.loads(empprofjson)
    hospitalusername= empprofobj["Au"]
    msgs = Message.objects.all()
    Appointments = []
    Donorz = []
    for Appointment in msgs:
        if(msgs !=""):
            if(Appointment.email == "Appointment@hospital" and "AppSeted" in Appointment.message ):
                o={
                    "Appby":Appointment.Timestamp,
                    "Appbyname":Appointment.name,
                    "Date" : Appointment.message[8:]
                }
                Appointments.append(o)
                
            if(Appointment.email == "Appointment@hospital" and "BloodDonated" in Appointment.message ):
                o={
                    "Appby":Appointment.Timestamp,
                    "Appbyname":Appointment.name,
                    "DonatedOnDate" : Appointment.message[12:]
                }
                Donorz.append(o)
    print(Donorz)

    return render(request, 'home/appointmentsshown.html', {"App":Appointments,"Donorz":Donorz })

        
@allowed_users(allowed_roles=['Hospital_Employees'])
def blooddonated(request, DonorUsername):
    now = datetime.datetime.now()


    msgs = Message.objects.filter(Timestamp = DonorUsername).last()
    st =  "BloodDonated" +  str(now)
    msgs.message = st
    msgs.save()
    return redirect('appointmentsshown')


        



    
    

    
    
    
    






    

    
    
    





def loging(request):
    return render(request, 'home/logingoogle.html')

def reportedblogs(request):
    post = Report.objects.all().order_by('rno')
    li = []
        # {sno= sno,
        # reps = [{}, {}, {}]

        # }

    for p in post:
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
        
        if(msg.email == "example@email"):
            obj ={"name": msg.name,
                    "msg":msg.message,
                    "un":msg.authorUsername,
                    "time":msg.Timestamp
            }

            new_list.append(obj)
    return HttpResponse(json.dumps(new_list))
    
        
        
        
            
    
   




def Donors(request):
    if request.method=="POST":
        bg_val = request.POST.get('Blood_grp_val', '')
        try:
            group = Group.objects.get(name='HospitalHeads')
            users = list(group.user_set.all())
            CSsend = []
            for user in users:
                CSdict = json.loads(user.first_name)
                CSdict2 = json.loads(user.last_name)
                if bg_val in CSdict2["BA"]:
                    o = {
                        "Name":CSdict["N"],
                        "Email":CSdict["E"],
                        "Add":CSdict2["A"],
                        "Phone":CSdict2["P"]
                    }
                    CSsend.append(o)
                
            return HttpResponse(json.dumps(CSsend))
        except Exception as e:
            return HttpResponse('Error Occured')
    userl =[]    
    group = Group.objects.get(name='HospitalHeads')
    hospitals = list(group.user_set.all())
    for h in hospitals:
        userjson1 =h.first_name
        userjson =h.last_name
        userdict1 = json.loads(userjson1)
        userdict = json.loads(userjson)
        o = {
            "un":h.username,
            "n":userdict1["N"],
            "em":userdict1["E"],
            "Add":userdict["A"],
            "P":userdict["P"]
        }
        userl.append(o)

    

    return render(request, 'home/Donors.html', {"Hospitals" : userl})
                
                    
                

                    

                
                
               
                
            
                   
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


def livechat(request):
    if request.method == "POST":
        if(request.user.is_authenticated):
            profilejson = request.user.first_name
            try:
                profiledict = json.loads(profilejson)
                
                
                now = datetime.datetime.now()
                name = profiledict["N"]
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

        else:
            messages.error(request, "Please login to chat")
            return render(request, 'home/home.html')
            
    else:
        return render(request,'home/livechat.html' )
                    

                

                
        



   
    
    






     
     

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
        try:

            username = request.POST.get('husername')
            name = request.POST.get('hname')
            hemail = request.POST.get('hemail')
            haddress = request.POST.get('hadd')
            PhoneNumber = request.POST.get('phonenumber')
            hid = request.POST.get('pass1')
            hid2 = request.POST.get('pass2')

            if(hid2 != hid):
                messages.error(request,"Password did not match")
                return redirect('addhospital')
            myuser = User.objects.create_user(username, hemail, hid)

            profileobj1 = {
                "N":name,"U":username,"G":"h","E":hemail,
            }
            pro2={"A":haddress,"Au":request.user.username,"BA":"Na",
            "P":PhoneNumber}

            myuserjson = json.dumps(profileobj1)
            myuserjson2 = json.dumps(pro2)
            if(v(username) and v(hid) and l(name) and l(hemail) and l(haddress) and l(PhoneNumber) ):
                myuser.first_name = myuserjson
                myuser.last_name = myuserjson2
                # myuser.first_name='hospitalh'

                myuser.save()
                group = Group.objects.get(name='HospitalHeads')
                myuser.groups.add(group)
                messages.success(request, "New Hospital Added")
                return redirect('Add')
            else:
                messages.error(request, "Enter Proper Data")
                return redirect('Add')
        except:
            messages.error(request, "Enter Proper Data")
            return redirect('Add')

       


@login_required(login_url='/home')
@allowed_users(allowed_roles=[ 'HospitalHeads'])
def AddEmployee(request):
    if request.method == "POST":
        try:
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
            if(v(username) and v(hid) and l(hemail)):
            
                myuser.first_name = myuserjson
                myuser.last_name = myuserjson2

                myuser.save()
                group = Group.objects.get(name='Hospital_Employees')
                myuser.groups.add(group)
                messages.success(request, "New Employee Added")
                return redirect('AddEmployee')
            else:
                messages.error(request, "Password/Username invalid")
                return redirect('AddEmployee')
        except:
            messages.error(request, "Enter Proper data")
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
                return redirect('home')

            elif grp ==  "c":
                login(request, user)
                messages.success(request, "Successfully Logged In")
                return redirect('home')
            elif grp == "u":
                login(request,user)
                messages.success(request, "Successfully Logged In")
                return redirect('home')
            elif grp =="h":
                login(request,user)
                messages.success(request, "Successfully Logged In")
                return redirect('home')
            elif grp =="Wa":
                login(request,user)
                messages.success(request, "Successfully Logged In")
                return redirect('home')
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
        DorCS = request.POST.get('DorCS')
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
        DoC = 0
        if(DorCS == "on"):
            DoC = "CS"
        else:
            DoC="BD"

        profileobj1 = {
            "N": name,
            "U":username,
            "G": "c",
            "B": pbloodgrp,
            "D": pdod,
            "n": p_age,
            "T":DoC,

        }
        pro2={
            "A": profiledict2["X"],
            "Y": profiledict2["Y"],
            "Ae": profiledict["E"],
            "Au": request.user.username,"E":pemail,}


        myuserjson = json.dumps(profileobj1)
        myuserjson2 = json.dumps(pro2)
        if(v(username) and v(pid1) and l(name) and l(pemail) and l(pbloodgrp) and l(pdod) and l(p_age)):

            myuser.first_name = myuserjson
            myuser.last_name = myuserjson2

            myuser.save()
            group = Group.objects.get(name='Covid_Survivors')
            myuser.groups.add(group)
            messages.success(request, "Donor Added")
            return redirect('addpat')
        else:
            messages.error(request, "Password/Username invalid")
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
    if request.method == "POST":
        Ap = request.POST.get('A+')
        Bp = request.POST.get('B+')
        ABp = request.POST.get('AB+')
        Op = request.POST.get('O+')
        An = request.POST.get('A-')
        Bn = request.POST.get('B-')
        ABn = request.POST.get('AB-')
        On = request.POST.get('O-')
        App = request.POST.get('A+(P)')
        Bpp = request.POST.get('B+(P)')
        ABpp = request.POST.get('AB+(P)')
        Opp = request.POST.get('O+(P)')
        Anp = request.POST.get('A-(P)')
        Bnp = request.POST.get('B-(P)')
        ABnp = request.POST.get('AB-(P)')
        Onp = request.POST.get('O-(P)')
        bldlist = []
        if(Ap == "on"):
            bldlist.append("1")
        if(Bp == "on"):
            bldlist.append("2")
        if(ABp == "on"):
            bldlist.append("3")
        if(Op == "on"):
            bldlist.append("4")
        if(An == "on"):
            bldlist.append("5")
        if(Bn == "on"):
            bldlist.append("6")
        if(ABn == "on"):
            bldlist.append("7")
        if(On == "on"):
            bldlist.append("8")
        if(App == "on"):
            bldlist.append("9")
        if(Bpp == "on"):
            bldlist.append("10")
        if(ABpp == "on"):
            bldlist.append("11")
        if(Opp == "on"):
            bldlist.append("12")
        if(Anp == "on"):
            bldlist.append("13")
        if(Bnp == "on"):
            bldlist.append("14")
        if(ABnp == "on"):
            bldlist.append("15")
        if(Onp == "on"):
            bldlist.append("16")

        print(bldlist)
       


        # print(bl)
        blood =bldlist
        objjson = request.user.last_name
        objjson1 = request.user.first_name
        obj = json.loads(objjson)
        obj1 = json.loads(objjson1)
        if(obj1["G"] == "h"):
            obj["BA"] = blood
            objj = json.dumps(obj)
            request.user.last_name = objj
            request.user.save()
            
            request.user.save()
            messages.success(request, "Data Updated")
            return redirect('profile')
        else:
            return HttpResponse("error")






    userjson2 =request.user.first_name
    try:
        userdict = json.loads(userjson2)
        profilejson1 = request.user.first_name
        profilejson2 = request.user.last_name
        profiledict1 = json.loads(profilejson1)
        profiledict2 = json.loads(profilejson2)
        return render(request, 'home/profile.html', {"p1":profiledict1,"p2":profiledict2, "gg":False})
    except:
        msgs = Message.objects.filter(Timestamp = request.user.username).last()
        print(msgs)

        if(msgs != None):
            if("AppSeted" in msgs.message or "BloodDonated" in msgs.message):
                hospitaln = json.loads(User.objects.filter(username = msgs.authorUsername)[0].first_name)["N"]
                st =msgs.message
                hn = hospitaln
            else:
                st = "N"
                hn = "NN"
        else:
            st = "N"
            hn = "NN"




        o = {
            "fn":userjson2,
            "ln": request.user.last_name,
            "em":request.user.email,
            "gg":"T",
            "status": st,
            "hname":hn

        }
        print(o)
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
    


        






