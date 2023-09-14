from django.contrib.auth import logout,login
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from django.shortcuts import render
from django.urls import reverse
from student_application.emailBackEnd import EmailBackend
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages

def members(request):  
  return render(request,'myfirst.html')

def ShowLogin(request):  
  return render(request,'login.html')



def DoLogin(request):
  if request.method!="POST":
    return HttpResponse("<h2>Method Not allowed")
  
  else:
    user = EmailBackend.authenticate(request,request.POST.get("email"),request.POST.get("password"))
    if user!=None:    
      login(request,user)  
      if user.user_type=="1":      
        return HttpResponseRedirect(reverse("admin_home"))
      
      elif user.user_type == "2":
        return HttpResponseRedirect(reverse("staff_home"))
      
      elif user.user_type == "3":
        return HttpResponseRedirect(reverse("student_home"))
      
      else:
        return HttpResponseRedirect(reverse("student_home"))
    
    else:
      messages.error(request,"Invalid Login Details")
      return HttpResponseRedirect(reverse("admin_home"))
    
    
def GetUserDetails(request):
  user = request.user
  if user.is_authenticated:
    return HttpResponse("User : "+user.email+" usertype : " + user.usertype)
  else:
    return HttpResponse("Please login first")   
  
  
def logout_user(request):
  logout(request)
  return HttpResponseRedirect(reverse("login"))
    
    
    
    
 
  
  