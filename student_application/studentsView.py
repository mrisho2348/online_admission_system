
from datetime import datetime
from time import strptime
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from student_application.models import (
   
    CustomUser,
    
    Students, 
    Subject,

)
from student_application.templatetags.custom_filters import strftime


def student_home(request):
    student_object = Students.objects.get(admin=request.user.id)
    
    # Get subject-related data
    subject_data = Subject.objects.filter(students=student_object)  # Assuming students is the related_name of the ManyToManyField
    subject_name = []

    total_subjects_taken = student_object.subjects.count()  # Assuming subjects is the related_name of the ManyToManyField
    
    for subject in subject_data:  
    
       
        subject_name.append(subject.subject_name)
      
    
    return render(
        request,
        "student_template/student_home.html",
        {
           
            "subject_name": subject_name,
         
            "total_subjects_taken": total_subjects_taken,
            "students": student_object,
        },
    )





def  student_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    students = Students.objects.get(admin=user)
    return render(request,"student_template/student_profile.html",{"user":user,"students":students})  

@login_required
def student_profile_save(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        password = request.POST.get("password")
        address = request.POST.get("address")

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != "" and password is not None:
                customuser.set_password(password)
            customuser.save()

            students = Students.objects.get(admin=customuser.id)
            students.address = address
            students.save()

            messages.success(request, "Profile has been successfully edited")
        except:
            messages.error(request, "Editing of profile failed")

    return HttpResponseRedirect(reverse("student_profile"))