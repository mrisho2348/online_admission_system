import json
from django.urls import reverse
from datetime import datetime
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from django.conf import settings
from django.templatetags.static import static
import os
from .models import (  

    CustomUser,

    SessionYearModel,
    PreviousEducation,
    Students,
    Subject,
    Parent,    
    EducationLevel,
    Class_level,
   School, 
    
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
from django.db.models import Count

def admin_home(request):
    # Fetch secondary students
    form_i_class = Class_level.objects.get(name='Form I')
    form_ii_class = Class_level.objects.get(name='Form II')
    form_iii_class = Class_level.objects.get(name='Form III')
    form_iv_class = Class_level.objects.get(name='Form IV')
    
    form_i_students = Students.objects.filter(selected_class=form_i_class)
    form_ii_students = Students.objects.filter(selected_class=form_ii_class)
    form_iii_students = Students.objects.filter(selected_class=form_iii_class)
    form_iv_students = Students.objects.filter(selected_class=form_iv_class)

# Fetch primary students
    std_i_class = Class_level.objects.get(name='STD I')
    std_ii_class = Class_level.objects.get(name='STD II')
    std_iii_class = Class_level.objects.get(name='STD III')
    std_iv_class = Class_level.objects.get(name='STD IV')
    std_v_class = Class_level.objects.get(name='STD V')
    std_vi_class = Class_level.objects.get(name='STD VI')
    std_vii_class = Class_level.objects.get(name='STD VII')

    std_i_students = Students.objects.filter(selected_class=std_i_class)
    std_ii_students = Students.objects.filter(selected_class=std_ii_class)
    std_iii_students = Students.objects.filter(selected_class=std_iii_class)
    std_iv_students = Students.objects.filter(selected_class=std_iv_class)
    std_v_students = Students.objects.filter(selected_class=std_v_class)
    std_vi_students = Students.objects.filter(selected_class=std_vi_class)
    std_vii_students = Students.objects.filter(selected_class=std_vii_class)

# Fetch nursery students
    baby_class = Class_level.objects.get(name='Baby')
    kg1_class = Class_level.objects.get(name='KG1')
    kg2_class = Class_level.objects.get(name='KG2')

    baby_students = Students.objects.filter(selected_class=baby_class)
    kg1_students = Students.objects.filter(selected_class=kg1_class)
    kg2_students = Students.objects.filter(selected_class=kg2_class)

    # Calculate the total number of secondary students
    total_form_i_students = form_i_students.count()
    total_form_ii_students = form_ii_students.count()
    total_form_iii_students = form_iii_students.count()
    total_form_iv_students = form_iv_students.count()

    # Calculate the total number of primary students
    total_std_i_students = std_i_students.count()
    total_std_ii_students = std_ii_students.count()
    total_std_iii_students = std_iii_students.count()
    total_std_iv_students = std_iv_students.count()
    total_std_v_students = std_v_students.count()
    total_std_vi_students = std_vi_students.count()
    total_std_vii_students = std_vii_students.count()

    # Calculate the total number of nursery students
    total_baby_students = baby_students.count()
    total_kg1_students = kg1_students.count()
    total_kg2_students = kg2_students.count()

    # Query to get the count of students for each educational level
    students_by_education_level = Students.objects.values('education_level__name').annotate(total_students=Count('id'))

    # Initialize variables to store total students for each level
    total_nursery_student = 0
    total_primary_student = 0
    total_secondary_student = 0

    # Iterate through the result and assign totals to respective variables
    for entry in students_by_education_level:
        if entry['education_level__name'] == 'Nursery school level':
            total_nursery_student = entry['total_students']
        elif entry['education_level__name'] == 'Primary school':
            total_primary_student = entry['total_students']
        elif entry['education_level__name'] == 'Secondary school':
            total_secondary_student = entry['total_students']

    # Count the number of male students
    total_male_students = Students.objects.filter(gender='Male').count()
    student_count = Students.objects.all().count()
    subject_count = Subject.objects.all().count()
    # Count the number of female students
    total_female_students = Students.objects.filter(gender='Female').count()

    # Define a list of class levels
    class_levels = ['Baby', 'KG1', 'KG2', 'STD I', 'STD II', 'STD III', 'STD IV', 'STD V', 'STD VI', 'STD VII', 'FORM I', 'FORM II', 'FORM III', 'FORM IV']

    # Create a dictionary to store the total number of students for each class level
    class_level_counts = {}

    # Loop through the class levels and count the students for each
    for class_level in class_levels:
        # Count the students with the selected class level
        total_students = Students.objects.filter(selected_class__name=class_level).count()

        # Add the count to the dictionary
        class_level_counts[class_level] = total_students

    context = {
        "total_nursery_student": total_nursery_student,
        "total_primary_student": total_primary_student,
        "total_secondary_student": total_secondary_student,
        "total_male_students": total_male_students,
        "total_female_students": total_female_students,
        "class_level_counts": class_level_counts,
        "class_levels": class_levels,
        "student_count": student_count,
        "subject_count": subject_count,
        "total_form_i_students": total_form_i_students,
        "total_form_ii_students": total_form_ii_students,
        "total_form_iii_students": total_form_iii_students,
        "total_form_iv_students": total_form_iv_students,
        "total_std_i_students": total_std_i_students,
        "total_std_ii_students": total_std_ii_students,
        "total_std_iii_students": total_std_iii_students,
        "total_std_iv_students": total_std_iv_students,
        "total_std_v_students": total_std_v_students,
        "total_std_vi_students": total_std_vi_students,
        "total_std_vii_students": total_std_vii_students,
        "total_baby_students": total_baby_students,
        "total_kg1_students": total_kg1_students,
        "total_kg2_students": total_kg2_students,
    }

    return render(request, "admin_template/home_content.html", context)

def add_parents(request):
    students = Students.objects.all()
    return render(request, "admin_template/parent_form.html", {'students': students})   

def add_parents(request):
    students = Students.objects.all()
    return render(request, "admin_template/parent_form.html", {'students': students})   


def edit_parents(request, parent_id):
    try:
        request.session['parent_id'] = parent_id       
        parent = Parent.objects.get(id=parent_id)
        students = Students.objects.all()

        # Get the IDs of currently associated students, if any
        associated_student_ids = parent.student.all().values_list('id', flat=True)

        return render(request, "admin_template/edit_parent.html", {
            "id": parent_id,
            "username":  parent.admin.first_name + " " + parent.admin.last_name ,
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
            if not phone:
                messages.error(request, "phone field is required.")         
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
        return render(request, 'admin_template/edit_parent.html', context)

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

            # Create or update the CustomUser
            user, created = CustomUser.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name,
                    'user_type': 3,
                }
            )

            if not created:
                user.email = email
                user.first_name = first_name
                user.last_name = last_name
                user.user_type = 3
                user.password = password
                user.save()

            # Create or update the Parent
            parent, created = Parent.objects.get_or_create(
                admin=user,  # Set the admin field to the user
                defaults={
                    'phone': phone,
                    'occupation': occupation,
                    'address': sheia,
                    'street_address': street,
                    'house_number': house,
                    'national_id': national_id,
                    'status': status,
                    'gender': gender,
                    'parent_type': parent_type,
                }
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

            # Associate the parent with the student
            student.parent.add(parent)

            messages.success(request, "Parent information saved successfully")
            return redirect("add_parents")

        except Exception as e:
            messages.error(request, "Error saving parent information: " + str(e))

    return redirect("add_parents")


def delete_parent(request, parent_id):
    try:
        parent = Parent.objects.get(id=parent_id)
        parent.delete()
        return JsonResponse({"message": "Parent deleted successfully."})
    except Parent.DoesNotExist:
        return JsonResponse({"error": "Parent not found."}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

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
            education_level_id = request.POST.get('school_segment')
            current_class_ids = request.POST.get('current_class')
            birth_certificate_id = request.POST.get('birth_certificate_id')
            allergies = request.POST.get('allergies')           
            sheia_address = request.POST.get('sheia_address')
            street_address = request.POST.get('street_address')
            house_number = request.POST.get('house_number')
            health_status = request.POST.get('health_status')
            physical_disability = request.POST.get('physical_disability')
            subjects_ids = request.POST.getlist('subjects')
            session_year_id = request.POST.get('session_year')
            # Perform validation
            educational_level = EducationLevel.objects.get(id=education_level_id)
            class_level = Class_level.objects.get(id=current_class_ids)    
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
                
                user= CustomUser.objects.create_user(username=username,password=password,email=default_email,first_name=first_name,last_name=last_name,user_type=2)

                # Create a new instance of the Student model
               
                user.students.surname = surname
                user.students.service_type = service_type                
                user.students.date_of_birth = date_of_birth
                user.students.gender = gender
                user.students.phone_number = phone_number
                user.students.education_level = educational_level
                user.students.selected_class = class_level
                user.students.birth_certificate_id = birth_certificate_id
                user.students.allergies = allergies            
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
                user.students.session_year = session_year

                # Save the student record again to include the subjects and session year
                user.students.save()

                messages.success(request, "Successfully added student")
                return redirect("add_previous_education", student_id=user.students.id)
            except ValidationError as ve:
                messages.error(request, ve.message)
            except Exception as e:
                messages.error(request, f"Error saving student record: {str(e)}")
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")

    return redirect("add_student")

def add_previous_student_education(request, student_id, previous_education_id=None):
    student = get_object_or_404(Students, id=student_id)
    edit_mode = False
    previous_education = None
    education_levels = EducationLevel.objects.all()
    previous_education = PreviousEducation.objects.filter(student=student)    
    if previous_education:
        # Check if the request is for editing an existing previous education entry
        try:
            previous_education = PreviousEducation.objects.get(student=student)
            edit_mode = True
        except PreviousEducation.DoesNotExist:
            # If the previous education entry doesn't exist or doesn't belong to the student, it's treated as a new entry.
            previous_education = None

    context = {
        'student': student,
        'previous_education': previous_education,
        'edit_mode': edit_mode,
        'education_levels': education_levels,
    }

    return render(request, "admin_template/add_previous_education.html", context)        

def add_student(request):
    all_subjects = Subject.objects.all()
    all_session_years = SessionYearModel.objects.all()
    
    # Query all education levels from the EducationLevel model
    all_education_levels = EducationLevel.objects.all()

    context = {
        "all_subjects": all_subjects,
        "all_session_years": all_session_years,
        "all_education_levels": all_education_levels,  # Add education levels to the context
    }

    return render(request, "admin_template/add_student.html", context)

def single_student_detail(request, student_id):
    students = get_object_or_404(Students, id=student_id)
    parents = Parent.objects.filter(student=students)
    previous_education = PreviousEducation.objects.filter(student=students)
    
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
        'previousEducation':previous_education,
    }

    return render(request, "admin_template/student_details.html", context)

def add_previous_education_save(request, student_id):
    student = get_object_or_404(Students, id=student_id)
    edit_mode = False
    previous_education = None

    if request.method == 'POST':
        examination_number = request.POST.get('examination_number')
        year_completed = request.POST.get('year_completed')
        education_level_id = request.POST.get('school_level')
        school_name = request.POST.get('school_name')
        results = request.POST.get('results')

        try:
            education_level = EducationLevel.objects.get(id=education_level_id)

            if not examination_number or not year_completed or not school_name or not results:
                messages.error(request, "Please provide all required fields.")
                return redirect(f'add_previous_education/{student_id}/')

            if PreviousEducation.objects.filter(student=student).exists():
                previous_education = PreviousEducation.objects.get(student=student)
            else:
                previous_education = PreviousEducation(student=student)

            previous_education.examination_number = examination_number
            previous_education.year_completed = year_completed
            previous_education.education_level = education_level
            previous_education.school_name = school_name
            previous_education.results = results
            previous_education.save()

            # Redirect to the next step of the application process
            # Modify the URL and view name accordingly
            return redirect('next_application_step', student_id=student_id)

        except Exception as e:
            messages.error(request, f"Error saving previous education information: {str(e)}")

    return redirect(f'add_previous_education/{student_id}/')


def edit_previous_education_save(request, student_id, previous_education_id):
    try:
        # Retrieve the student and previous education objects
        student = get_object_or_404(Students, id=student_id)
        previous_education = PreviousEducation.objects.get(id=previous_education_id, student=student)

        if request.method == "POST":
            # Extract data from the form
            examination_number = request.POST.get('examination_number')
            year_completed = request.POST.get('year_completed')
            education_level_id = request.POST.get('school_level')
            school_name = request.POST.get('school_name')
            results = request.POST.get('results')

            # Update the previous education object
            previous_education.examination_number = examination_number
            previous_education.year_completed = year_completed
            previous_education.education_level_id = education_level_id
            previous_education.school_name = school_name
            previous_education.results = results

            # Save the changes
            previous_education.save()

            # Display a success message
            messages.success(request, "Previous education information updated successfully")

            # Redirect to the next form or page (e.g., the payment page)
            # Replace 'next_form_url' with the actual URL of the next form or page
            return redirect('next_application_step', student_id=student_id)  # Redirect to the payment page or the next step

    except CustomUser.DoesNotExist:
        messages.error(request, "Student not found")
    except PreviousEducation.DoesNotExist:
        messages.error(request, "Previous education record not found")
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")

    # Redirect back to the edit page with the same student and previous education objects
    return redirect('edit_previous_education', student_id=student_id, previous_education_id=previous_education_id)


def single_parent_detail(request, parent_id):
    parent = get_object_or_404(Parent, id=parent_id)
    students = parent.student.all()  # Get all students associated with the parent
    
    context = {
        'parent': parent,
        'students': students,
    }
    
    return render(request, "admin_template/parent_details.html", context)


  
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
    
    return render(request, "admin_template/manage_student.html", {"students": students, "page_obj": page_obj})


def manage_parent(request):
    per_page = request.GET.get('per_page', 3)  # Get the number of items to display per page from the request
    parents = Parent.objects.all()
    parents = parents.order_by('id')
    paginator = Paginator(parents, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "admin_template/manage_parent.html", {"students": parents, "page_obj": page_obj})
 
def student_list(request):
    search_query = request.GET.get('search', '')
    students = Students.objects.all()
    
    if search_query:
        students = students.filter(registration_number__icontains=search_query)
    
    paginator = Paginator(students, per_page=10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "paginator.html", {"students": students, "page_obj": page_obj})  

def get_subjects_by_education_level(request):
    if request.method == 'GET':
        education_level_id = request.GET.get('education_level_id')

        # Query subjects based on the selected education level
        subjects = Subject.objects.filter(education_level_id=education_level_id).values('id', 'subject_name')

        # Convert the queryset to a list of dictionaries
        subjects_list = list(subjects)

        return JsonResponse(subjects_list, safe=False)
    
def manage_subject(request):
    per_page = request.GET.get('per_page', 33)
    search_query = request.GET.get('search', '')

    subjects = Subject.objects.filter(
        Q(subject_name__icontains=search_query) | Q(education_level__name__icontains=search_query)
    )
    subjects = subjects.order_by('id')
    paginator = Paginator(subjects, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "admin_template/manage_subject.html", {
        "subjects": page_obj,
        "search_query": search_query,
    })
    

def edit_subject(request,subject_id):
    # If you want to populate the form fields with an existing Subject object
    subject = Subject.objects.get(pk=subject_id)  # Replace subject_id with the ID of the Subject you want to edit
    education_levels = EducationLevel.objects.all()
    return render(request, 'admin_template/edit_subject.html', {'subject': subject,'education_levels':education_levels}) 
   

def create_or_edit_subject(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id)
    education_levels = EducationLevel.objects.all()

    if request.method == 'POST':
        # Retrieve the selected education level from the POST data
        education_level_id = request.POST.get('education_level')
        subject_name = request.POST.get('subject_name')

        # Perform basic validation
        if not education_level_id or not subject_name:
            messages.error(request, 'Please fill in all the required fields.')
            return redirect('edit_subject', subject_id=subject_id)

        # Check if the selected education level exists
        education_level = get_object_or_404(EducationLevel, pk=education_level_id)

        # Update the Subject object with the selected education level
        subject.education_level = education_level  # Assign the education_level object, not just the ID
        subject.subject_name = subject_name

        # Save the Subject object to the database
        subject.save()

        messages.success(request, 'Subject details successfully updated.')
        return redirect('edit_subject', subject_id=subject_id)

    return render(request, 'edit_subject.html', {'subject': subject, 'education_levels': education_levels})


def subject_details(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id)
    return render(request, 'admin_template/subject_detail.html', {'subject': subject})

def delete_subject(request, subject_id):
    try:
        subject = get_object_or_404(Subject, id=subject_id)
        subject.delete()
        return redirect('manage_subject')
    except Subject.DoesNotExist:
        return JsonResponse({'error': 'Subject not found'}, status=404)

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
        school_segment_ids = request.POST.get('school_segment')
        current_class_ids = request.POST.get('current_class')
        birth_certificate_id = request.POST.get('birth_certificate_id')
        allergies = request.POST.get('allergies')
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
        student.birth_certificate_id = birth_certificate_id
        student.allergies = allergies
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
            
        
        educational_level = EducationLevel.objects.get(pk=school_segment_ids)
        student.education_level = educational_level
                    
       
        current_class = Class_level.objects.get(pk=current_class_ids)
        student.selected_class = current_class

        # Add the selected session year to the student's session_year field
        session_year = SessionYearModel.objects.get(pk=session_year_id)
        student.session_year = session_year

        student.save()

        # del request.session['student_id']
        messages.success(request, "Successfully edited student")
        return redirect("add_previous_education", student_id=user.students.id)
        # return HttpResponseRedirect(reverse("edit_student", kwargs={"student_id": student_id}))

    except CustomUser.DoesNotExist:
        messages.error(request, "User does not exist")
        return HttpResponseRedirect(reverse("edit_student"))

    except Students.DoesNotExist:
        messages.error(request, "Student does not exist")
        return HttpResponseRedirect(reverse("edit_student"))

    except IntegrityError:
        messages.error(request, "Failed to edit student due to a database error")
        return HttpResponseRedirect(reverse("edit_student"))

@csrf_exempt
def get_class_levels(request):
    if request.method == 'GET':
        education_level_id = request.GET.get('education_level_id')        
        # Query class levels based on the selected education level
        class_levels = Class_level.objects.filter(school_level_id=education_level_id).values('id', 'name')
        return JsonResponse(list(class_levels), safe=False)

   
def edit_student(request, student_id):
    try:
        # Get the student record based on the student_id
        student = Students.objects.get(admin__id=student_id)
        request.session['student_id'] = student_id
        education_levels = EducationLevel.objects.all()
        # Fetch all subjects and session years
        all_subjects = Subject.objects.all()
        all_session_years = SessionYearModel.objects.all()

        # Get the currently selected class level for the student
        selected_class = student.selected_class  # This will give you the selected class object

        # Get the currently selected subjects for the student
        selected_subjects = student.subjects.all()  # This will give you a queryset of selected subject objects

        selected_subject_ids = [subject.id for subject in selected_subjects]  # Get IDs of selected subjects

        selected_session_year = student.session_year
        print(student.selected_class.id)
        return render(request, "admin_template/edit_student.html", {
            "student_id": student_id,
            "username": student.admin.username,
            "students": student,
            "all_subjects": all_subjects,
            "all_session_years": all_session_years,
            "selected_subjects": selected_subjects,
            "selected_session_year": selected_session_year,
            "all_education_levels": education_levels,
            "selected_class": selected_class,
            "selected_subjects_ids": selected_subject_ids,
        })
    except Students.DoesNotExist:
        messages.error(request, "Student does not exist")
        return HttpResponseRedirect(reverse("manage_studen"))
    
    
def delete_student(request, student_id):
    try:
        # Get the student based on the student_id
        student = Students.objects.get(id=student_id)        
        # Check if the student exists
        if student:
            # Delete the student
            student.delete()

            # Optionally, you can add a success message here
            messages.success(request, 'Student deleted successfully.')

    except Students.DoesNotExist:
        # Optionally, you can add an error message here
        messages.error(request, 'Student not found.')

    # Redirect to a suitable URL, such as a student list page
    return redirect('manage_student')   
  
    
def add_session(request):    
    return render(request,"admin_template/add_session.html")

def edit_session(request, session_id):
    session = get_object_or_404(SessionYearModel, id=session_id)
    return render(request, "admin_template/edit_session.html", {"session": session})


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

    return render(request, 'admin_template/edit_session.html', {'session': session})


def manage_session(request):
    sessions = SessionYearModel.objects.all()
    return render(request, 'admin_template/manage_session.html', {'sessions': sessions})

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
    
    return render(request, 'admin_template/ad_session.html')    

def  admin_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    return render(request,"admin_template/admin_profile.html",{"user":user})  

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
            school_level = form.cleaned_data["school_level"]  # Update this line
            
            try:
                subject = Subject(subject_name=subject_name, education_level=school_level)  # Update this line
                subject.save()
                
                messages.success(request, "Subject successfully added")
                return HttpResponseRedirect(reverse("addsubject"))  
            
            except Exception as e:
                messages.error(request, f"Failed to add subject. Error: {str(e)}")
                return HttpResponseRedirect(reverse("addsubject"))
            
        else:
            messages.error(request, "Invalid form submission. Please check the form fields.")
            return HttpResponseRedirect(reverse("addsubject"))

  
  
def add_class_level(request):
    # Query the database to get a list of education levels
    education_levels = EducationLevel.objects.all()  # You can adjust this query as needed

    context = {
        'education_levels': education_levels,
    }

    return render(request, 'admin_template/add_school_class.html', context)    

def add_class_level_save(request):
    if request.method == 'POST':
        # Retrieve form data from request.POST
        name = request.POST.get('name')
        school_level_id = request.POST.get('school_level')
        capacity = request.POST.get('capacity')
        start_date = request.POST.get('start_date')

        try:
            # Fetch the selected EducationLevel instance
            school_level = EducationLevel.objects.get(id=school_level_id)

            # Create a new Class_level instance and save it to the database
            class_level = Class_level(
                name=name,
                school_level=school_level,
                capacity=capacity,
                start_date=start_date,
            )
            class_level.save()

            # Add a success message
            messages.success(request, 'Class Level added successfully.')

            # Redirect to a success page or another view
            return redirect('manage_class_level')  # Replace with your desired URL name
        except EducationLevel.DoesNotExist:
            # Handle the case where the selected EducationLevel doesn't exist
            # Add an error message
            messages.error(request, 'Selected School Level does not exist. Please select a valid School Level.')

    # Handle GET request or any form submission errors here
    return render(request, 'admin_template/add_school_class.html')      


def manage_class_level(request):
    # Retrieve all Class_level instances
    class_levels = Class_level.objects.all()    
    # Render the template and pass the class_levels queryset
    return render(request, 'admin_template/manage_school_class.html', {'class_levels': class_levels})

def edit_class_level(request, class_level_id):
    # Retrieve the ClassLevel object or return a 404 error if not found
    class_level = get_object_or_404(Class_level, id=class_level_id)

    # Retrieve all EducationLevels to populate the dropdown
    education_levels = EducationLevel.objects.all()

    context = {
        'class_level': class_level,
        'education_levels': education_levels,
    }

    return render(request, 'admin_template/edit_class_level.html', context)

def edit_class_level_save(request, class_level_id):
    # Get the Class_level object to edit
    class_level = get_object_or_404(Class_level, id=class_level_id)
    
    if request.method == 'POST':
        try:
            # Extract data from the form
            name = request.POST['name']
            school_level_id = request.POST['school_level']
            capacity = request.POST['capacity']
            start_date = request.POST['start_date']
            
            # Update the Class_level object
            class_level.name = name
            class_level.school_level_id = school_level_id
            class_level.capacity = capacity
            class_level.start_date = start_date
            
            # Save the changes
            class_level.save()
            
            messages.success(request, 'Class Level updated successfully.')
            return redirect('manage_class_level')  # Replace with your desired URL name for the class level list
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            # You can add additional error handling here if needed
    return render(request, 'admin_template/edit_class_level.html', {'class_level': class_level})

def delete_class_level(request, class_level_id):
    # Retrieve the ClassLevel object based on the class_level_id
    class_level = get_object_or_404(Class_level, id=class_level_id)

    # Delete the ClassLevel object
    class_level.delete()

    # Redirect to the list of class levels or any appropriate URL
    return redirect('manage_class_level')



def add_subject(request):
    forms = AddSubjectForm()
    return render(request,"admin_template/add_subject.html",{"forms":forms})    

   
def add_school(request):    
    return render(request,"admin_template/add_school_infor.html")
   
def add_school_save(request):
    if request.method == 'POST':
        try:
            # Extract data from the form
            name = request.POST['name']
            address = request.POST['address']
            contact_person = request.POST.get('contact_person', '')  # Use get() to handle optional fields
            contact_email = request.POST.get('contact_email', '')
            contact_phone = request.POST.get('contact_phone', '')
            website = request.POST.get('website', '')
            established_year = request.POST.get('established_year', None)  # Use None for optional integer fields
            principal = request.POST.get('principal', '')
            description = request.POST.get('description', '')

            # Create a new School object and save it to the database
            school = School(
                name=name,
                address=address,
                contact_person=contact_person,
                contact_email=contact_email,
                contact_phone=contact_phone,
                website=website,
                established_year=established_year,
                principal=principal,
                description=description
            )
            school.save()

            messages.success(request, 'School added successfully.')
            return redirect('manage_school_save')  # Replace with your desired URL name for the school list
        except Exception as e:
            messages.error(request, f'Error: {e}')
            return redirect('add_school')  # Redirect back to the add school form with an error message

    return render(request, 'add_school.html')  # Adjust the template name as needed   

def manage_school_save(request):
    # Retrieve all Class_level instances
    schools = School.objects.all()    
    # Render the template and pass the class_levels queryset
    return render(request, 'admin_template/manage_school_infor.html', {'schools': schools})

def edit_school(request, school_id):
    # Retrieve the School object based on the school_id
    school = get_object_or_404(School, id=school_id)

    if request.method == 'POST':
        try:
            # Get the updated data from the POST request
            name = request.POST.get('name')
            address = request.POST.get('address')
            contact_person = request.POST.get('contact_person')
            contact_email = request.POST.get('contact_email')
            contact_phone = request.POST.get('contact_phone')
            website = request.POST.get('website')
            established_year = request.POST.get('established_year')
            principal = request.POST.get('principal')
            description = request.POST.get('description')

            # Update the School object with the new data
            school.name = name
            school.address = address
            school.contact_person = contact_person
            school.contact_email = contact_email
            school.contact_phone = contact_phone
            school.website = website
            school.established_year = established_year
            school.principal = principal
            school.description = description

            school.save()  # Save the updated school details

            return redirect('manage_school_save')  # Redirect to the list of schools or any appropriate URL
        except Exception as e:
            # Handle any exceptions, such as validation errors
            return HttpResponse(f"Error: {e}")

    # If it's a GET request, display the edit form template
    return render(request, 'admin_template/edit_educational_info.html', {'school': school})

def delete_school(request, school_id):
    # Retrieve the School object based on the school_id
    school = get_object_or_404(School, id=school_id)

    # Delete the School object
    school.delete()

    # Redirect to the list of schools or any appropriate URL
    return redirect('manage_school_save')


def add_education_level(request):    
    return render(request,"admin_template/add_education_level.html")

def add_education_level_save(request):
    if request.method == 'POST':
        try:
            # Extract data from the form
            name = request.POST['name']

            # Create a new EducationLevel object and save it to the database
            education_level = EducationLevel(name=name)
            education_level.save()

            messages.success(request, 'Education Level added successfully.')
            return redirect('manage_education_level')  # Replace with your desired URL name for the education level list
        except Exception as e:
            messages.error(request, f'Error: {e}')
            return redirect('add_education_level')  # Redirect back to the add education level form with an error message

    return render(request, 'admin_template/add_education_level.html')  # Adjust the template name as needed

def confirm_delete_education_level(request, education_level_id):
    # Retrieve the EducationLevel object based on the education_level_id
    education_level = get_object_or_404(EducationLevel, id=education_level_id)

    return render(request, 'admin_template/confirm_delete_education_level.html', {'education_level': education_level})

def manage_education_level(request):
    # Retrieve all Class_level instances
    education_levels = EducationLevel.objects.all()    
    # Render the template and pass the class_levels queryset
    return render(request, 'admin_template/manage_education_level.html', {'education_levels': education_levels})



def edit_education_level(request, education_level_id):
    # Retrieve the EducationLevel object based on the education_level_id
    education_level = get_object_or_404(EducationLevel, id=education_level_id)

    if request.method == 'POST':
        # Get the updated data from the POST request
        name = request.POST.get('name')

        # Update the EducationLevel object with the new data
        education_level.name = name
        education_level.save()

        return redirect('manage_education_level')  # Redirect to the list of education levels or any appropriate URL

    # If it's a GET request, display the edit form template
    return render(request, 'admin_template/edit_education_level.html', {'education_level': education_level})


def delete_education_level(request, education_level_id):
    # Retrieve the EducationLevel object based on the education_level_id
    education_level = get_object_or_404(EducationLevel, id=education_level_id)

    if request.method == 'POST':
        # If the request method is POST, it means the user confirmed the deletion.
        # You can delete the object and redirect to the list of education levels or any appropriate URL.
        education_level.delete()
        return redirect('manage_education_level')  # Redirect to the list of education levels or any appropriate URL

    # If the request method is not POST, display a confirmation page.
    return redirect('confirm_delete_education_level', education_level_id=education_level_id)


def generate_student_form(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="student_form.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)

    styles = getSampleStyleSheet()
    style_heading = styles['Heading1']
    style_normal = styles['Normal']
    style_normal.leading = 15

    story = []

    # Create a custom canvas to add watermark and background image
    c = canvas.Canvas(response)
    
    # Add a watermark
    c.setFont("Helvetica", 40)
    c.setFillGray(0.7, 0.7)  # Set the fill color for the watermark
    c.rotate(45)  # Rotate the text
    c.drawString(100, 300, "Watermark")


    c.save()  # Save the canvas

    # Add a title to the form
    title = Paragraph('Student Information Form', style_heading)
    story.append(title)

    # Define form fields for the PDF
    form_fields = [
        ("First Name:", ""),
        ("Surname:", ""),
        ("Service Type:", ""),
        ("Admission Fee Paid:", ""),
        ("Interview Details:", ""),
        ("Date of Birth:", ""),
        ("Gender:", ""),
        ("Phone Number:", ""),
        ("Education Level:", ""),
        ("Selected Class:", ""),
        ("Active:", ""),
        ("Birth Certificate ID:", ""),
        ("Allergies:", ""),
        ("Address:", ""),
        ("Street Address:", ""),
        ("House Number:", ""),
        ("Health Status:", ""),
        ("Physical Disability:", ""),
        ("Subjects:", ""),
        ("Profile Picture:", ""),
        ("Birth Certificate Photo:", "")
    ]

    # Create a grid layout as a table
    table_data = []
    for label, value in form_fields:
        table_data.append([label, value])

    table = Table(table_data, colWidths=[3*inch, 3*inch])
    table.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    story.append(Spacer(1, 12))
    story.append(table)

    doc.build(story)

    return response