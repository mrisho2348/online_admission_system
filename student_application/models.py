from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.dispatch import receiver
from django.db.models.signals import post_save
# Model for Education Levels (Secondary, Primary, Nursery)
class EducationLevel(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class SessionYearModel(models.Model):
    id = models.AutoField(primary_key=True)
    session_start_year = models.DateField()
    session_end_year = models.DateField()
    objects=models.Manager()
        

    
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)
        
class CustomUser(AbstractUser):
    user_type_data = ((1, "HOD"), (2, "Students"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)

    # Provide unique related_name for groups and user_permissions fields
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='custom_user_set'  # Use a unique related_name
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_set'  # Use a unique related_name
    )

    objects = CustomUserManager()
    

class AdminHOD(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()     

# Model for Schools
class School(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    contact_person = models.CharField(max_length=100, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    established_year = models.PositiveIntegerField(blank=True, null=True)
    principal = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

# Model for Classes
class Class(models.Model):
    name = models.CharField(max_length=50)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    class_teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    capacity = models.PositiveIntegerField()
    start_date = models.DateField()

    def __str__(self):
        return f"{self.school} - {self.name}"

class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    education_level = models.ForeignKey(EducationLevel, on_delete=models.CASCADE)
    subject_name = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
# Model for Students

class Students(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)  
    surname = models.CharField(max_length=100)    
    service_type = models.CharField(max_length=100, default='school', blank=True)  
    admission_fee_paid = models.BooleanField(default=False)
    interview_details = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)  
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10)    
    phone_number = models.CharField(max_length=20)
    education_level = models.ForeignKey(EducationLevel, on_delete=models.CASCADE)
    selected_class = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    birth_certificate_id = models.CharField(max_length=100)
    allergies = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=200)
    street_address = models.CharField(max_length=200)
    house_number = models.CharField(max_length=20)
    health_status = models.CharField(max_length=200)
    physical_disability = models.CharField(max_length=200)
    subjects = models.ManyToManyField(Subject, related_name='students', blank=True)
    profile_pic = models.FileField(null=True, blank=True)
    birth_certificate_photo = models.FileField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True) 
    # Add the ForeignKey field to SessionYearModel
    session_year = models.ForeignKey(SessionYearModel, on_delete=models.SET_NULL, null=True, blank=True)
    objects = models.Manager()
    def __str__(self):
        return self.admin.first_name + " " + self.admin.last_name
    
    
class Parent(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    
    TYPE_CHOICES = [
        ('parent', 'Parent'),
        ('guardian', 'Guardian'),
        ('sponsor', 'Sponsor'),
    ]
    
    
    phone = models.CharField(max_length=20)
    occupation = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    street_address = models.CharField(max_length=100)
    house_number = models.CharField(max_length=10)
    national_id = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    status = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    parent_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    student = models.ManyToManyField(Students,  related_name='parent')
    fcm_token = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)       
    objects = models.Manager()    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"    
    
    


# Model for Admissions
class Admission(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    control_number = models.CharField(max_length=10, unique=True)
    admission_fee_amount = models.DecimalField(max_digits=10, decimal_places=2, default=10000.00)
    interview_date = models.DateTimeField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Admission for {self.student.user.username}"



    
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:  # HOD
            AdminHOD.objects.create(admin=instance)
        elif instance.user_type == 2:  # Students
            Students.objects.create(admin=instance)

            
 
@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminhod.save()
    elif instance.user_type == 2:
        instance.staffs.save()
