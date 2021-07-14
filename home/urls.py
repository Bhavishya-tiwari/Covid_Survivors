from django.urls import path,include
from home import views

urlpatterns = [
    path('', views.home, name='home'),
    path('covidupdates', views.CovidUpdates, name='CovidUpdates'),
    path('donors', views.Donors, name='Donors'),
    path('contactus', views.ContactUs, name='ContactUs'),

    # Add Hospital jaha 2 form hai (hosptal login, admin login)
    path('addhospital', views.AddHospital, name='AddHospital'),

    # Hospital ko signup
    path('addhadmin', views.AddHadmin, name='AddHadmin'),

    # Post req to login hospital
    path('addemployee', views.AddEmp, name='AddEmp'),



    
    # Adding employee by login as hospital
    path('addemployeee', views.AddEmployee, name='AddEmployee'),

    path('logout', views.handelLogout, name='logout'),
    

    # Add employee by hospital head
    path('login', views.loginall, name='login'),
    path('loginemp', views.loginemp, name='loginemp'),

    # Add patients#
    #by employee afte sign in
    path('addpat', views.addpat, name='addpat'),

    # profile
    path('profile', views.profile , name='profile'),
    
    # normal user sign up
    path('nusignup', views.nusignup, name='nusignup'),

    #website admin works
    path('add', views.Add, name='Add'),



    
]