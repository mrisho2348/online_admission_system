import json
from django.urls import reverse
from datetime import datetime
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

from student_application.models import (  

    CustomUser,

    SessionYearModel,

    Students,
    Subject,
    Parent,    
 
)

from student_application.forms import  (
    AddSessionYearForm,  
    AddSubjectForm,
  
)

from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from django.db import IntegrityError, DatabaseError
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpResponseBadRequest
from PIL import Image

def admin_home(request):
  
    subject_count = Subject.objects.all().count()
    student_count = Students.objects.all().count()

    subject_all = Subject.objects.all()
    subject_list = [subject.subject_name for subject in subject_all]



    student_all = Students.objects.all()

    student_name_list = []
    for student in student_all:  
        student_name_list.append(student.admin.username)

    context = {
     
        "subject_count": subject_count,
        "subject_list": subject_list,  
        "student_count": student_count,
    }

    return render(request, "hod_template/home_content.html", context)

def add_parents(request):
    students = Students.objects.all()
    return render(request, "hod_template/parent_form.html", {'students': students})   

def add_parents(request):
    students = Students.objects.all()
    return render(request, "hod_template/parent_form.html", {'students': students})   


def edit_parents(request, parent_id):
    try:
        request.session['parent_id'] = parent_id       
        parent = Parent.objects.get(id=parent_id)
        students = Students.objects.all()

        # Get the IDs of currently associated students, if any
        associated_student_ids = parent.student.all().values_list('id', flat=True)

        return render(request, "hod_template/edit_parent.html", {
            "id": parent_id,
            "username": parent.name,
            "parents": parent,
            "students": students,
            "associated_student_ids": associated_student_ids,  # Pass the associated student IDs to the template
        })
    except Parent.DoesNotExist:
        messages.error(request, "Parent not found.")
        return redirect("manage_parent")





def update_parent(request, parent_id):
    try:
        parent = get_object_or_404(Parent, id=parent_id)

        if request.method == 'POST':
            # Retrieve form field values from the request
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            occupation = request.POST.get('occupation')
            address = request.POST.get('sheia')
            street_address = request.POST.get('street')
            house_number = request.POST.get('house')
            national_id = request.POST.get('nationalid')
            status = request.POST.get('status')
            gender = request.POST.get('gender')
            parent_type = request.POST.get('type')

            # Perform form field validation
            if not name:
                messages.error(request, "Name field is required.")
            elif not phone:
                messages.error(request, "Phone Number field is required.")
            elif not occupation:
                messages.error(request, "Occupation field is required.")
            elif not address:
                messages.error(request, "Sheia Address field is required.")
            elif not street_address:
                messages.error(request, "Street Address field is required.")
            elif not house_number:
                messages.error(request, "House Number field is required.")
            elif not national_id:
                messages.error(request, "National ID field is required.")
            elif not status:
                messages.error(request, "Status field is required.")
            elif not gender:
                messages.error(request, "Gender field is required.")
            elif not parent_type:
                messages.error(request, "Relation field is required.")
            else:
                # Update the parent record
                parent.name = name
                parent.phone = phone
                parent.occupation = occupation
                parent.address = address
                parent.street_address = street_address
                parent.house_number = house_number
                parent.national_id = national_id
                parent.status = status
                parent.gender = gender
                parent.parent_type = parent_type

                # Get the selected students (assuming 'students' is a list of student IDs from the form)
                selected_student_ids = request.POST.getlist('student_id')

                # Clear existing relationships and add the selected students
                parent.student.clear()  # Clear all existing relationships
                for student_id in selected_student_ids:
                    student = get_object_or_404(Students, id=student_id)
                    parent.student.add(student)  # Add selected students to the relationship

                parent.save()

                messages.success(request, "Parent and associated students have been successfully updated.")
                return redirect("edit_parents", parent_id=parent_id)

        context = {
            'parent': parent,
            'students': Students.objects.all(),
            'selected_student_ids': [student.id for student in parent.student.all()] if hasattr(parent, 'student') else []
        }
        return render(request, 'hod_template/edit_parent.html', context)

    except Parent.DoesNotExist:
        messages.error(request, "Parent not found.")
        return redirect("edit_parents", parent_id=parent_id)
    
    
def save_parent(request):
    if request.method == "POST":
        try:
            student_id = request.POST.get('student_id')
            phone = request.POST.get('phone')
            occupation = request.POST.get('occupation')
            sheia = request.POST.get('sheia')
            street = request.POST.get('street')
            house = request.POST.get('house')
            national_id = request.POST.get('nationalid')
            status = request.POST.get('status')
            gender = request.POST.get('gender')
            parent_type = request.POST.get('type')

            username = request.POST.get('username')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            password = request.POST.get('password')

            if not all([student_id, phone, username, first_name, last_name, email, password]):
                messages.error(request, "Please provide all required fields")
                return redirect("add_parents")

            student = Students.objects.get(id=student_id)

            user, created = CustomUser.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name,
                    'user_type': 8,
                }
            )

            if not created:
                user.email = email
                user.first_name = first_name
                user.last_name = last_name
                user.user_type = 8
                user.set_password(password)
                user.save()

            parent, created = Parent.objects.get_or_create(
                phone=phone,
                occupation=occupation,
                address=sheia,
                street_address=street,
                house_number=house,
                national_id=national_id,
                status=status,
                gender=gender,
                parent_type=parent_type
            )

            if not created:
                parent.phone = phone
                parent.occupation = occupation
                parent.address = sheia
                parent.street_address = street
                parent.house_number = house
                parent.national_id = national_id
                parent.status = status
                parent.gender = gender
                parent.parent_type = parent_type
                parent.save()

            parent.admin = user
            parent.save()

            student.parent.add(parent)

            messages.success(request, "Parent information saved successfully")
            return redirect("add_parents")

        except Exception as e:
            messages.error(request, "Error saving parent information: " + str(e))

    return redirect("add_parents")


def add_student_save(request):
    if request.method == "POST":
        try:
            # Extract form data
            first_name = request.POST.get('first_name')
            surname = request.POST.get('surname')
            service_type = request.POST.get('service_type')
            last_name = request.POST.get('last_name')
            date_of_birth_str = request.POST.get('date_of_birth')
            date_of_birth = datetime.strptime(date_of_birth_str, '%Y-%m-%d').date()
            gender = request.POST.get('gender')
            phone_number = request.POST.get('phone_number')
            school_segment = request.POST.get('school_segment')
            current_class = request.POST.get('current_class')
            birth_certificate_id = request.POST.get('birth_certificate_id')
            allergies = request.POST.get('allergies')
            current_year = request.POST.get('current_year')
            is_finished = request.POST.get('is_finished')
            sheia_address = request.POST.get('sheia_address')
            street_address = request.POST.get('street_address')
            house_number = request.POST.get('house_number')
            health_status = request.POST.get('health_status')
            physical_disability = request.POST.get('physical_disability')
            subjects_ids = request.POST.getlist('subjects')
            session_year_id = request.POST.get('session_year')

            # Perform validation
            if not first_name or not last_name or not date_of_birth:
                messages.error(request, "Please provide all required fields")
                return redirect("add_student")

            # Save the form data to the database
            try:
                # Save the student's profile picture
                student_photo_url = None
                student_photo = request.FILES.get('student_photo')
                if student_photo:
                    if student_photo.size > 5242880:  # 10 MB (size in bytes)
                        raise ValidationError("Profile picture size should be less than 5 MB.")
                    if not student_photo.name.lower().endswith(('.jpg', '.jpeg', '.png')):
                        raise ValidationError("Only JPG, JPEG, and PNG image files are allowed for profile pictures.")
                    fs = FileSystemStorage()
                    filename = fs.save(student_photo.name, student_photo)
                    student_photo_url = fs.url(filename)

                # Save the birth certificate photo
                birth_certificate_photo_url = None
                birth_certificate_photo = request.FILES.get('birth_certificate_photo')
                if birth_certificate_photo:
                    if birth_certificate_photo.size > 5242880:  # 10 MB (size in bytes)
                        raise ValidationError("Birth certificate photo size should be less than 5 MB.")
                    if not birth_certificate_photo.name.lower().endswith(('.pdf')):
                        raise ValidationError("Only PDF image files are allowed for birth certificate photos.")
                    fs = FileSystemStorage()
                    filename = fs.save(birth_certificate_photo.name, birth_certificate_photo)
                    birth_certificate_photo_url = fs.url(filename)

                # Retrieve or create the CustomUser instance based on the username
                username = first_name.lower() + last_name.lower()
                default_email = first_name.lower() + "@gmail.com"
                password = '1234'  # Set a default password
                
                user= CustomUser.objects.create_user(username=username,password=password,email=default_email,first_name=first_name,last_name=last_name,user_type=3)

                # Create a new instance of the Student model
               
                user.students.surname = surname
                user.students.service_type = service_type
                user.students.last_name = last_name
                user.students.date_of_birth = date_of_birth
                user.students.gender = gender
                user.students.phone_number = phone_number
                user.students.school_segment = school_segment
                user.students.current_class = current_class
                user.students.birth_certificate_id = birth_certificate_id
                user.students.allergies = allergies
                user.students.current_year = current_year
                user.students.is_finished = is_finished
                user.students.address = sheia_address
                user.students.street_address = street_address
                user.students.house_number = house_number
                user.students.health_status = health_status
                user.students.physical_disability = physical_disability
                user.students.profile_pic = student_photo_url
                user.students.birth_certificate_photo = birth_certificate_photo_url

                # Save the student record
                user.save()

                # Add the selected subjects to the student's subjects field
                for subject_id in subjects_ids:
                    subject = Subject.objects.get(pk=subject_id)
                    user.students.subjects.add(subject)

                # Add the selected session year to the student's session_id field
                session_year = SessionYearModel.objects.get(pk=session_year_id)
                user.students.session_id = session_year

                # Save the student record again to include the subjects and session year
                user.students.save()

                messages.success(request, "Successfully added student")
                return redirect("add_student")
            except ValidationError as ve:
                messages.error(request, ve.message)
            except Exception as e:
                messages.error(request, f"Error saving student record: {str(e)}")
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")

    return redirect("add_student")

        

def add_student(request):
    all_subjects = Subject.objects.all()
    all_session_years = SessionYearModel.objects.all()

    context = {
        "all_subjects": all_subjects,
        "all_session_years": all_session_years,
    }

    return render(request, "hod_template/add_student.html", context)

def single_student_detail(request, student_id):
    students = get_object_or_404(Students, id=student_id)
    parents = Parent.objects.filter(student=students)
    selected_subjects = students.subjects.all()
    father = None
    mother = None
    male_guardian = None
    female_guardian = None
    male_sponsor = None
    female_sponsor = None

    for parent in parents:
        if parent.parent_type == 'parent':
            if parent.gender == 'male':
                father = parent
            elif parent.gender == 'female':
                mother = parent
        elif parent.parent_type == 'guardian':
            if parent.gender == 'male':
                male_guardian = parent
            elif parent.gender == 'female':
                female_guardian = parent
        elif parent.parent_type == 'sponsor':
            if parent.gender == 'male':
                male_sponsor = parent
            elif parent.gender == 'female':
                female_sponsor = parent

    context = {
        'students': students,
        'father': father,
        'mother': mother,
        'male_guardian': male_guardian,
        'female_guardian': female_guardian,
        'male_sponsor': male_sponsor,
        'female_sponsor': female_sponsor,
        'selected_subjects':selected_subjects,
    }

    return render(request, "hod_template/student_details.html", context)


def single_parent_detail(request, parent_id):
    parent = get_object_or_404(Parent, id=parent_id)
    students = parent.student.all()  # Get all students associated with the parent
    
    context = {
        'parent': parent,
        'students': students,
    }
    
    return render(request, "hod_template/parent_details.html", context)


  
def manage_student(request):
    per_page = request.GET.get('per_page', 3)
    current_class = request.GET.get('current_class')  # Get the selected class from the request
    students = Students.objects.all()
    
    if current_class:  # Filter students by class if it is selected
        students = students.filter(current_class=current_class)
    students = students.order_by('id')
    paginator = Paginator(students, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "hod_template/manage_student.html", {"students": students, "page_obj": page_obj})


def manage_parent(request):
    per_page = request.GET.get('per_page', 3)  # Get the number of items to display per page from the request
    parents = Parent.objects.all()
    parents = parents.order_by('id')
    paginator = Paginator(parents, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "hod_template/manage_parent.html", {"students": parents, "page_obj": page_obj})
 
def student_list(request):
    search_query = request.GET.get('search', '')
    students = Students.objects.all()
    
    if search_query:
        students = students.filter(registration_number__icontains=search_query)
    
    paginator = Paginator(students, per_page=10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "paginator.html", {"students": students, "page_obj": page_obj})  


def manage_subject(request):
    per_page = request.GET.get('per_page', 3)
    search_query = request.GET.get('search', '')

    subjects = Subject.objects.filter(
        Q(subject_name__icontains=search_query) | Q(school_segment__icontains=search_query)
    )
    subjects = subjects.order_by('id')
    paginator = Paginator(subjects, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "hod_template/manage_subject.html", {
        "subjects": subjects,
        "page_obj": page_obj,
        "search_query": search_query,
    })
    

def edit_subject(request,subject_id):
    # If you want to populate the form fields with an existing Subject object
    subject = Subject.objects.get(pk=subject_id)  # Replace subject_id with the ID of the Subject you want to edit
    return render(request, 'hod_template/edit_subject.html', {'subject': subject}) 
   

def create_or_edit_subject(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id)

    if request.method == 'POST':
        school_segment = request.POST.get('school_segment')
        subject_name = request.POST.get('subject_name')

        # Perform basic validation
        if not school_segment or not subject_name:
            messages.error(request, 'Please fill in all the required fields.')
            return redirect('edit_subject', subject_id=subject_id)

        # Update the Subject object with the form data
        subject.school_segment = school_segment
        subject.subject_name = subject_name

        # Save the Subject object to the database
        subject.save()

        messages.success(request, 'Subject details successfully updated.')
        return redirect('edit_subject', subject_id=subject_id)  # Provide the subject_id as an argument

    return render(request, 'edit_subject.html', {'subject': subject})

def subject_details(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id)
    return render(request, 'hod_template/subject_detail.html', {'subject': subject})


def edit_student_save(request):
    if request.method != "POST":
        return HttpResponse("Method not allowed")

    print("Session data:", request.session.items())
    student_id = request.session.get("student_id")
    print("Student ID:", student_id)
    if not student_id:
        return HttpResponseRedirect(reverse("manage_student"))

    try:
        user = CustomUser.objects.get(id=student_id)

        # Get the form data
        first_name = request.POST.get('first_name')
        surname = request.POST.get('surname')
        service_type = request.POST.get('service_type')
        last_name = request.POST.get('last_name')
        date_of_birth_str = request.POST.get('date_of_birth')
        date_of_birth = datetime.strptime(date_of_birth_str, '%Y-%m-%d').date()
        gender = request.POST.get('gender')
        phone_number = request.POST.get('phone_number')
        school_segment = request.POST.get('school_segment')
        current_class = request.POST.get('current_class')
        birth_certificate_id = request.POST.get('birth_certificate_id')
        allergies = request.POST.get('allergies')
        current_year = request.POST.get('current_year')
        is_finished = request.POST.get('is_finished')
        sheia_address = request.POST.get('sheia_address')
        street_address = request.POST.get('street_address')
        house_number = request.POST.get('house_number')
        health_status = request.POST.get('health_status')
        physical_disability = request.POST.get('physical_disability')

        # Get the selected subjects and session year
        subjects_ids = request.POST.getlist('subjects')
        session_year_id = request.POST.get('session_year')

        # Perform validation
        if not all([first_name, last_name, date_of_birth]):
            messages.error(request, "Please provide all required fields")
            return redirect("add_student")

        # Update user information
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        # Update student information
        student = Students.objects.get(admin=user)
        student.surname = surname
        student.service_type = service_type
        student.date_of_birth = date_of_birth
        student.gender = gender
        student.phone_number = phone_number
        student.school_segment = school_segment
        student.current_class = current_class
        student.birth_certificate_id = birth_certificate_id
        student.allergies = allergies
        student.current_year = current_year
        student.is_finished = is_finished
        student.address = sheia_address
        student.street_address = street_address
        student.house_number = house_number
        student.health_status = health_status
        student.physical_disability = physical_disability

        # Validate and save the profile picture
        student_photo = request.FILES.get('student_photo')
        if student_photo:
            if student_photo.size > 5242880:  # 5 MB limit
                raise ValidationError("Profile picture size should not exceed 5 MB.")
            if not student_photo.name.lower().endswith(('.png', '.jpg', '.jpeg')):
                raise ValidationError("Invalid file format. Only PNG, JPG, and JPEG files are allowed.")
            fs = FileSystemStorage()
            filename = fs.save(student_photo.name, student_photo)
            student.profile_pic = fs.url(filename)

        # Validate and save the birth certificate photo
        birth_certificate_photo = request.FILES.get('birth_certificate_photo')
        if birth_certificate_photo:
            if birth_certificate_photo.size > 5242880:  # 5 MB limit
                raise ValidationError("Birth certificate photo size should not exceed 5 MB.")
            if not birth_certificate_photo.name.lower().endswith('.pdf'):
                raise ValidationError("Invalid file format. Only PDF files are allowed.")
            fs = FileSystemStorage()
            filename = fs.save(birth_certificate_photo.name, birth_certificate_photo)
            student.birth_certificate_photo = fs.url(filename)

        student.save()

        # Clear existing subjects and add the selected subjects to the student's subjects field
        student.subjects.clear()
        for subject_id in subjects_ids:
            subject = Subject.objects.get(pk=subject_id)
            student.subjects.add(subject)

        # Add the selected session year to the student's session_year field
        session_year = SessionYearModel.objects.get(pk=session_year_id)
        student.session_year = session_year

        student.save()

        # del request.session['student_id']
        messages.success(request, "Successfully edited student")
        return HttpResponseRedirect(reverse("edit_student", kwargs={"student_id": student_id}))

    except CustomUser.DoesNotExist:
        messages.error(request, "User does not exist")
        return HttpResponseRedirect(reverse("edit_student"))

    except Students.DoesNotExist:
        messages.error(request, "Student does not exist")
        return HttpResponseRedirect(reverse("edit_student"))

    except IntegrityError:
        messages.error(request, "Failed to edit student due to a database error")
        return HttpResponseRedirect(reverse("edit_student"))




   
def edit_student(request, student_id):
    try:
        # Get the student record based on the student_id
        student = Students.objects.get(admin__id=student_id)
        request.session['student_id'] = student_id
        # Fetch all subjects and session years
        all_subjects = Subject.objects.all()
        all_session_years = SessionYearModel.objects.all()

        # Get the currently selected subjects and session year for the student
        selected_subjects = student.subjects.all()
        selected_session_year = student.session_year

        return render(request, "hod_template/edit_student.html", {
            "student_id": student_id,
            "username": student.admin.username,
            "students": student,
            "all_subjects": all_subjects,
            "all_session_years": all_session_years,
            "selected_subjects": selected_subjects,
            "selected_session_year": selected_session_year,
        })

    except Students.DoesNotExist:
        messages.error(request, "Student does not exist")
        return HttpResponseRedirect(reverse("manage_studen"))
    
def add_session(request):    
    return render(request,"hod_template/add_session.html")

def edit_session(request, session_id):
    session = get_object_or_404(SessionYearModel, id=session_id)
    return render(request, "hod_template/edit_session.html", {"session": session})


def edit_session_save(request, session_id):
    session = get_object_or_404(SessionYearModel, id=session_id)

    if request.method == 'POST':
        # Get the data from the form submission
        session_start_year = request.POST.get('session_start_year')
        session_end_year = request.POST.get('session_end_year')

        # Update the session with the new data
        session.session_start_year = session_start_year
        session.session_end_year = session_end_year
        session.save()

        # Display a success message
        messages.success(request, 'Session updated successfully.')

        # Redirect to the list of sessions after successful editing
        return redirect('manage_session')
    else:
        # Display an error message for invalid form submission
        messages.error(request, 'Failed to update session. Please check the form data.')

    return render(request, 'hod_template/edit_session.html', {'session': session})


def manage_session(request):
    sessions = SessionYearModel.objects.all()
    return render(request, 'hod_template/manage_session.html', {'sessions': sessions})

def delete_session(request, session_id):
    try:
        session = SessionYearModel.objects.get(id=session_id)
        session.delete()
        messages.success(request, "Session deleted successfully.")
    except SessionYearModel.DoesNotExist:
        messages.error(request, "Session not found.")
    return redirect('manage_session')


def add_session_save(request):
    if request.method == 'POST':
        session_start_year = request.POST.get('session_start_year')
        session_end_year = request.POST.get('session_end_year')

        if session_start_year and session_end_year:
            SessionYearModel.objects.create(
                session_start_year=session_start_year,
                session_end_year=session_end_year
            )
            # Display a success message after successfully creating the session
            messages.success(request, 'Session added successfully.')
            return redirect('add_session')  # Replace 'list_sessions' with the URL name of a page that displays all sessions.
        else:
            # Display an error message if any of the fields are missing
            messages.error(request, 'Failed to add session. Please fill in all the fields.')
    
    return render(request, 'hod_template/ad_session.html')    

def  admin_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    return render(request,"hod_template/admin_profile.html",{"user":user})  

def edit_profile_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("admin_profile"))
    
    else:
       first_name = request.POST.get("first_name")
       last_name = request.POST.get("last_name")
       password = request.POST.get("password")
       try:           
          customuser = CustomUser.objects.get(id=request.user.id)
          customuser.first_name = first_name
          customuser.last_name = last_name
          if password!= "" and password!=None:
              customuser.set_password(password)     
                         
          customuser.save()
          messages.success(request,"profile is successfully edited")
          return HttpResponseRedirect(reverse("admin_profile"))
      
       except:
            messages.error(request,"editing  of profile  failed")
            return HttpResponseRedirect(reverse("admin_profile"))
        
@csrf_exempt
def check_email_exist(request):
    email = request.POST.get("email")
    user_object = CustomUser.objects.filter(email=email).exists()
    if user_object:
        return HttpResponse(True)
    
    else:
        return HttpResponse(False)
    
    
@csrf_exempt
def check_username_exist(request):
    username = request.POST.get("username")
    user_object = CustomUser.objects.filter(username=username).exists()
    if user_object:
        return HttpResponse(True)
    
    else:
        return HttpResponse(False)        
    
def add_subject_save(request):
    if request.method != "POST":
        return HttpResponse("Method not allowed")
    
    else:        
        form = AddSubjectForm(request.POST)
        if form.is_valid():
            subject_name = form.cleaned_data["subject_name"]
            school_segment = form.cleaned_data["school_segment"]
            
            try:
                subject = Subject(subject_name=subject_name, school_segment=school_segment)
                subject.save()
                
                messages.success(request, "Subject successfully added")
                return HttpResponseRedirect(reverse("addsubject"))  
            
            except Exception as e:
                messages.error(request, f"Failed to add subject. Error: {str(e)}")
                return HttpResponseRedirect(reverse("addsubject"))
            
        else:
            messages.error(request, "Invalid form submission. Please check the form fields.")
            return HttpResponseRedirect(reverse("addsubject"))
            

def add_subject(request):
    forms = AddSubjectForm()
    return render(request,"hod_template/add_subject.html",{"forms":forms})       