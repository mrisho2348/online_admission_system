from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin



class LoginCheckMiddleWare(MiddlewareMixin):
    
    def process_view(self,request,view_func,view_args,view_kwargs):
        modulename =  view_func.__module__
        user = request.user
        if user.is_authenticated:
            if user.user_type == "1":
               if modulename == "student_application.adminView":
                   pass
               elif modulename == "student_application.views" or  modulename == "django.views.static":
                   pass
            
               else:
                   return HttpResponseRedirect(reverse("admin_home"))

            elif user.user_type == "2":
               if modulename == "student_application.studentsView":
                   pass
               elif modulename == "student_application.views" or  modulename == "django.views.static":
                   pass
            
               else:
                   return HttpResponseRedirect(reverse("student_home"))
            elif user.user_type == "3":
               if modulename == "student_application.studentsView":
                   pass
               elif modulename == "student_application.views" or  modulename == "django.views.static":
                   pass
            
               else:
                   return HttpResponseRedirect(reverse("student_home"))
               
            else:
                return HttpResponseRedirect(reverse("login"))   
        
        else:
            if request.path == reverse("login") or request.path == reverse("DoLogin") or request.path == reverse("logout_user")  or modulename == "django.contrib.auth.views" :
                pass
            
            else:
                return HttpResponseRedirect(reverse("login"))
            





            