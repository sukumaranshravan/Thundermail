from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
#since there is no other app, we dont have to import any models from there.
# Create your views here.
def start_up(request):
    return render(request,'index.html')

def sign_up(request):
    return render(request,'register.html')
def register(request):
    name = request.POST['name'].title()
    gender = request.POST['gender']
    dob = request.POST['dob']
    mobile = request.POST['mobile']
    u_name = request.POST['user_name'] + "@thundermail.com"
    p_word = request.POST['password']
    register_me=Register_Tb(name=name,gender=gender,dob=dob,mobile=mobile,user_name=u_name,password=p_word)
    register_me.save()
    return redirect('start_up')

def sign_in(request):
    u_name = request.POST['user_name'] + "@thundermail.com"
    p_word = request.POST['password']
    details = Register_Tb.objects.filter(user_name=u_name,password=p_word)
    if details.count()>0:
        request.session['yourself']=details[0].id
        my_name = details[0].name
        return render(request,'home.html',{'see':details,'key':my_name})
    else:
        messages.add_message(request,messages.INFO,"User Not Found!")
        return redirect('start_up')

def sign_out(request):
    request.session.flush()
    messages.add_message(request,messages.INFO,"Signed Out Successfully.")
    return redirect('start_up')