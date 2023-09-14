"""
URL configuration for teachercollage project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import include, path
from mujtabaa import settings
from student_application import studentsView, views,adminView
urlpatterns = [
    path('', include('tabora_teachers_app.urls')),
    path('admin/', admin.site.urls),
    path('accounts/',include('django.contrib.auth.urls')),
    path('', views.ShowLogin, name='login'),
    path('GetUserDetails', views.GetUserDetails, name='GetUserDetails'),
    path('dologin', views.DoLogin, name='DoLogin'),
    path('admin_home', adminView.admin_home, name='admin_home'),     
  
    path('add_student', adminView.add_student, name='add_student'),   
    path('add_student_save', adminView.add_student_save, name='add_student_save'),    
    path('add_subject', adminView.add_subject, name='addsubject'),   
    path('add_subject_save', adminView.add_subject_save, name='addsubjectsave'),    
   
    path('manage_student', adminView.manage_student, name='manage_student'),   
   
    path('manage_subject', adminView.manage_subject, name='manage_subject'),   
    
      
    path('edit_student/<str:student_id>', adminView.edit_student, name='edit_student'),   
    path('edit_student_save', adminView.edit_student_save, name='edit_student_save'),   
   
    path('edit_subject/<str:subject_id>', adminView.edit_subject, name='edit_subject'),   

    path('manage_session', adminView.manage_session, name='manage_session'),   
    path('manage_session_save', adminView.edit_session_save, name='edit_session_save'),
    path('check_email_exist', adminView.check_email_exist, name='check_email_exist'),
    path('check_username_exist', adminView.check_username_exist, name='check_username_exist'),

  
    path('admin_profile', adminView.admin_profile, name='admin_profile'), 
    path('edit_profile_save', adminView.edit_profile_save, name='edit_profile_save'), 
    


   
     
    # student url paths  
    path('student_home', studentsView.student_home, name='student_home'),     
       
  
    path('student_profile', studentsView.student_profile, name='student_profile'),    
    path('student_profile_save', studentsView.student_profile_save, name='student_profile_save'),    
    path('logout_user', views.logout_user, name='logout_user'),  # Move this line here
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)