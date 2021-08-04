from django.urls import path,include
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from home import views

urlpatterns = [
    path('', views.home, name='home'), 
    path('covidupdates', views.CovidUpdates, name='CovidUpdates'),
    path('donors', views.Donors, name='Donors'),
    path('contactus', views.ContactUs, name='ContactUs'),

    # profile
    path('chatt', views.chat , name='chat'),
    

    # Hospital ko signup
    path('addhadmin', views.AddHadmin, name='AddHadmin'),

    # Post req to login hospital



    
    # Adding employee by login as hospital
    path('addemployeee', views.AddEmployee, name='AddEmployee'),

    path('livechat', views.livechat, name='livechat'),

    path('logout', views.handelLogout, name='logout'),
    

    # Add employee by hospital head
    path('login', views.loginall, name='login'),
    path('loginemp', views.loginemp, name='loginemp'),

    path('logingoogle', views.loging, name='loging'),

    # Add patients#
    #by employee afte sign in
    path('addpat', views.addpat, name='addpat'),

    # profile
    path('profile', views.profile , name='profile'),

    
    # normal user sign up
    # path('nusignup', views.nusignup, name='nusignup'),

    #website admin works
    path('add', views.Add, name='Add'),

    #Blogs visible page
    path('commentshow', views.commentshow, name='commentshow'),

    #deleting section
    path("delH/<str:uH>", views.DelH, name='DelJ'),
    path("delE/<str:uE>", views.DelE, name='DelE'),
    path("delCS/<str:uCS>", views.DelCS, name='DelCS'),
    path("reportedblogs", views.reportedblogs, name='reportedblogs'),




    # password reset section
      path('reset_password/',
     auth_views.PasswordResetView.as_view(template_name="home/password_reset.html"),
     name="reset_password"),

    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="home/password_reset_sent.html"), 
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="home/password_reset_form.html"), 
     name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="home/password_reset_done.html"), 
        name="password_reset_complete"),

    
]
urlpatterns += staticfiles_urlpatterns()