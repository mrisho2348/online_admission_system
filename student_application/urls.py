
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
    path('get_class_levels/', adminView.get_class_levels, name='get_class_levels'),     
    path('manage_student', adminView.manage_student, name='manage_student'),     
    path('edit_student/<str:student_id>', adminView.edit_student, name='edit_student'),   
    path('edit_student_save', adminView.edit_student_save, name='edit_student_save'), 
    path('students', adminView.student_list, name='student-list'), 
    path('delete_student/<int:student_id>/', adminView.delete_student, name='delete_student'),
    path('single_student_detail/<int:student_id>/', adminView.single_student_detail, name='single_student_detail'),
    path('add_previous_education/<int:student_id>/', adminView.add_previous_student_education, name='add_previous_education'),
    path('edit_previous_education/<int:student_id>/<int:previous_education_id>/', adminView.add_previous_student_education, name='edit_previous_education'),
    path('add_previous_education_save/<int:student_id>/', adminView.add_previous_education_save, name='add_previous_education_save'),
    path('edit_previous_education/<int:student_id>/<int:previous_education_id>/', adminView.edit_previous_education_save, name='edit_previous_education_save'),

    
    
    path('single_parent_detail/<str:parent_id>', adminView.single_parent_detail, name='single_parent_detail'),
    path('edit_parents/<str:parent_id>', adminView.edit_parents, name='edit_parents'),   
    path('edit_student_save', adminView.edit_student_save, name='edit_student_save'),   
    path('add_parents', adminView.add_parents, name='add_parents'),   
    path('save_parent', adminView.save_parent, name='save_parent'),   
    path('manage_parent', adminView.manage_parent, name='manage_parent'),       
    path('update_parent/<int:parent_id>/', adminView.update_parent, name='update_parent'),
    path('delete_parent/<int:parent_id>/', adminView.delete_parent, name='delete_parent'),
    
    path('add_class_level/', adminView.add_class_level, name='add_class_level'),
    path('manage-class-level/', adminView.manage_class_level, name='manage_class_level'),      
    path('add_class-level-save/', adminView.add_class_level_save, name='add_class_level_save'),      
    path('edit_class_level_save/<int:class_level_id>/', adminView.edit_class_level_save, name='edit_class_level_save'),
    path('edit_class_level/<int:class_level_id>/', adminView.edit_class_level, name='edit_class_level'),
    path('delete_class_level/<int:class_level_id>/', adminView.delete_class_level, name='delete_class_level'),

    
    path('add_school', adminView.add_school, name='add_school'),   
    path('add_school_save', adminView.add_school_save, name='add_school_save'),   
    path('manage_school_save', adminView.manage_school_save, name='manage_school_save'), 
    path('edit_school/<int:school_id>/', adminView.edit_school, name='edit_school'),
    path('delete_school/<int:school_id>/', adminView.delete_school, name='delete_school'),
    
    path('add_education_level', adminView.add_education_level, name='add_education_level'),   
    path('add_education_level_save', adminView.add_education_level_save, name='add_education_level_save'),   
    path('manage_education_level', adminView.manage_education_level, name='manage_education_level'), 
    path('edit_education_level/<int:education_level_id>/', adminView.edit_education_level, name='edit_education_level'),
    path('delete_education_level/<int:education_level_id>/', adminView.delete_education_level, name='delete_education_level'),
    path('confirm_delete_education_level/<int:education_level_id>/', adminView.confirm_delete_education_level, name='confirm_delete_education_level'),
    
    path('manage_subject', adminView.manage_subject, name='manage_subject'),   
    path('add_subject', adminView.add_subject, name='addsubject'),   
    path('add_subject_save', adminView.add_subject_save, name='addsubjectsave'),  
    path('edit_subject/<str:subject_id>', adminView.edit_subject, name='edit_subject'),   
    path('subject/<int:subject_id>/', adminView.subject_details, name='subject_details'),
    path('edit_subject/<int:subject_id>/', adminView.create_or_edit_subject, name='create_or_edit_subject'),
    path('get_subjects_by_education_level/',adminView.get_subjects_by_education_level, name='get_subjects_by_education_level'),
    path('delete_subject/<int:subject_id>/', adminView.delete_subject, name='delete_subject'),
    
    path('add_session/', adminView.add_session, name='add_session'),
    path('add_session_save/', adminView.add_session_save, name='add_session_save'),
    path('edit_session/<int:session_id>/', adminView.edit_session, name='edit_session'),
    path('edit_session_save/<int:session_id>/', adminView.edit_session_save, name='edit_session_save'),
    path('manage_session/', adminView.manage_session, name='manage_session'),
    path('delete_session/<int:session_id>/', adminView.delete_session, name='delete_session'),
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