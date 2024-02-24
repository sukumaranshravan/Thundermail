from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
import datetime
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
        user_name = details[0].user_name
        messages= Message_Tb.objects.filter(recipient_id=user_name)
        return render(request,'home.html',{'see':details,'key':my_name,'view':messages})
    else:
        messages.add_message(request,messages.INFO,"User Not Found!")
        return redirect('start_up')
    
def home(request):
    my_id=request.session['yourself']
    details = Register_Tb.objects.filter(id=my_id)
    user_name=details[0].user_name
    messages= Message_Tb.objects.filter(recipient_id=user_name)
    my_name = details[0].name
    return render(request,'home.html',{'key':my_name,'see':details,'view':messages})

def sign_out(request):
    request.session.flush()
    messages.add_message(request,messages.INFO,"Signed Out Successfully.")
    return redirect('start_up')

def compose(request):
    return render(request,'compose.html')

def compose_action(request):
    sender_id=request.session['yourself']
    recipient_id=request.POST['recipient'] + "@thundermail.com"
    subject=request.POST['subject']
    message=request.POST['message']
    file=request.FILES['attachment']
    date=datetime.date.today()
    time=datetime.datetime.now().strftime('%H:%M')
    send_mail = Message_Tb(sender_id_id=sender_id,recipient_id=recipient_id,subject=subject,message=message,attachment=file,date=date,time=time)
    send_mail.save()
    messages.add_message(request,messages.INFO,"Message sent.")
    return redirect("home")

def sent_items(request):
    my_id=request.session['yourself']
    details = Register_Tb.objects.filter(id=my_id)
    messages= Message_Tb.objects.filter(sender_id_id=my_id)
    my_name = details[0].name
    return render(request,'sent_items.html',{'key':my_name,'see':details,'view':messages})

def read_message(request,id):
    my_id=request.session['yourself']
    details = Register_Tb.objects.filter(id=my_id)
    my_name = details[0].name
    message=Message_Tb.objects.filter(id=id)
    return render(request,'read_message.html',{'key':my_name,'see':details,'read':message})