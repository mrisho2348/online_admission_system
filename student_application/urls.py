
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import include, path
from mujtabaa import settings
from . import studentsView, views,adminView
urlpatterns = [  
    path('', views.ShowLogin, name='login'),           
    path('dologin', views.DoLogin, name='DoLogin'),    
    path('admin_home', adminView.admin_home, name='admin_home'),       
    path('add_student', adminView.add_student, name='add_student'),   
    path('add_student_save', adminView.add_student_save, name='add_student_save'),
    path('get_class_levels', adminView.get_class_levels, name='get_class_levels'),     
    path('manage_student', adminView.manage_student, name='manage_student'),     
    path('edit_student/<str:student_id>', adminView.edit_student, name='edit_student'),   
    path('edit_student_save', adminView.edit_student_save, name='edit_student_save'), 
    
    path('add_class_level/', adminView.add_class_level, name='add_class_level'),
    path('manage-class-level/', adminView.manage_class_level, name='manage_class_level'),      
    path('add_class-level-save/', adminView.add_class_level_save, name='add_class_level_save'),      
    path('edit_class_level_save/<int:class_level_id>/', adminView.edit_class_level_save, name='edit_class_level_save'),
    path('edit_class_level/<int:class_level_id>/', adminView.edit_class_level, name='edit_class_level'),
    
    path('add_school', adminView.add_school, name='add_school'),   
    path('add_school_save', adminView.add_school_save, name='add_school_save'),   
    path('manage_school_save', adminView.manage_school_save, name='manage_school_save'), 
    
    path('add_education_level', adminView.add_education_level, name='add_education_level'),   
    path('add_education_level_save', adminView.add_education_level_save, name='add_education_level_save'),   
    path('manage_education_level', adminView.manage_education_level, name='manage_education_level'), 
     
    path('manage_subject', adminView.manage_subject, name='manage_subject'),   
    path('add_subject', adminView.add_subject, name='addsubject'),   
    path('add_subject_save', adminView.add_subject_save, name='addsubjectsave'),  
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
    
] 