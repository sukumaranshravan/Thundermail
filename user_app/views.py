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
        messages= Message_Tb.objects.filter(recipient_id=user_name,status_reciever='unread').order_by('-time') or Message_Tb.objects.filter(recipient_id=user_name,status_reciever='important').order_by('-time')
        block_list=Block_Tb.objects.filter(user_id=request.session['yourself'])
        return render(request,'home.html',{'see':details,'key':my_name,'view':messages,'blk':block_list})
    else:
        messages.add_message(request,messages.INFO,"User Not Found!")
        return redirect('start_up')
    
def home(request):     # home function also takes care of  inbox.
    my_id=request.session['yourself']
    details = Register_Tb.objects.filter(id=my_id)
    user_name=details[0].user_name
    messages= Message_Tb.objects.filter(recipient_id=user_name,status_reciever='unread').order_by('-time') or Message_Tb.objects.filter(recipient_id=user_name,status_reciever='important').order_by('-time')
    block_list=Block_Tb.objects.filter(user_id=my_id)
    my_name = details[0].name
    return render(request,'home.html',{'key':my_name,'see':details,'view':messages,'blk':block_list})

def sign_out(request):
    request.session.flush()
    messages.add_message(request,messages.INFO,"Signed Out Successfully.")
    return redirect('start_up')

def compose(request):
    my_id=request.session['yourself']
    details = Register_Tb.objects.filter(id=my_id)
    my_name = details[0].name
    return render(request,'compose.html',{'key':my_name,'see':details})

def compose_action(request):
    sender_id=request.session['yourself']
    if '@thundermail.com' in request.POST['recipient']:        # this condition is for reply, because when you click reply it automatically takes the whole user id from the database (coded like that.)
        recipient_id=request.POST['recipient']   
    else:                                       # this is for compose, where user is only required  to fill the user id only.
        recipient_id=request.POST['recipient'] + "@thundermail.com"
    subject=request.POST['subject']
    message=request.POST['message']
    file=request.FILES['attachment']
    date=datetime.date.today()
    time=datetime.datetime.now().strftime('%H:%M')
    block_check = Block_Tb.objects.filter(user_id=recipient_id,blocked_id_id=sender_id)
    if block_check.count()>0:
        send_mail = Message_Tb(sender_id_id=sender_id,recipient_id=recipient_id,subject=subject,message=message,attachment=file,date=date,time=time,status_reciever='blocked')
    else:  
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

def reply(request,id):
    reply_to = Register_Tb.objects.filter(id=id)
    recipient_id=reply_to[0].user_name
    my_id=request.session['yourself']
    details = Register_Tb.objects.filter(id=my_id)
    my_name = details[0].name
    return render(request,'reply.html',{'do':recipient_id,'key':my_name})

def forward(request,id):
    my_id=request.session['yourself']
    details = Register_Tb.objects.filter(id=my_id)
    my_name = details[0].name
    msg = Message_Tb.objects.filter(id=id)
    return render(request,'forward.html',{'fwd':msg,'key':my_name})

def important(request,id):
    my_id= request.session['yourself']
    details = Register_Tb.objects.filter(id=my_id)
    my_user_name=details[0].user_name
    check_imp = Message_Tb.objects.filter(recipient_id=my_user_name,status_reciever='important')
    if check_imp.count()>0:
        Message_Tb.objects.filter(id=id).update(status_reciever='unread')
    else:
        Message_Tb.objects.filter(id=id).update(status_reciever='important')
    return redirect('home')

def view_important(request):
    my_id = request.session['yourself']
    details = Register_Tb.objects.filter(id=my_id)
    my_name = details[0].name
    my_user_name=details[0].user_name
    imp_msg=Message_Tb.objects.filter(recipient_id=my_user_name,status_reciever='important')
    return render(request,'important.html',{'imp':imp_msg,'key':my_name})

def spam(request,id):
    my_id= request.session['yourself']
    details = Register_Tb.objects.filter(id=my_id)
    my_user_name=details[0].user_name
    check_spam = Message_Tb.objects.filter(recipient_id=my_user_name,status_reciever='spam')
    if check_spam.count()>0:
        Message_Tb.objects.filter(id=id).update(status_reciever='unread')
    else:
        Message_Tb.objects.filter(id=id).update(status_reciever='spam')
    # there is a catch here, what if a sender mark his own message from sent messages as spam?
    # we can take that into account by using if and else, like 'if id == my_id do this, else do that.
    # in such case status_sender will be equal to 'spam'.
    # this is applicable for 'important', 'spam' and 'trash'.
    return redirect('home')

def view_spam(request):
    my_id = request.session['yourself']
    details = Register_Tb.objects.filter(id=my_id)
    my_name = details[0].name
    my_user_name=details[0].user_name
    spm_msg=Message_Tb.objects.filter(recipient_id=my_user_name,status_reciever='spam')
    return render(request,'spam.html',{'spm':spm_msg,'key':my_name})

def trash(request,id):
    Message_Tb.objects.filter(id=id).update(status_reciever='trash')
    return redirect('home')

def view_trash(request):
    my_id = request.session['yourself']
    details = Register_Tb.objects.filter(id=my_id)
    my_name = details[0].name
    my_user_name=details[0].user_name
    trash_msg=Message_Tb.objects.filter(recipient_id=my_user_name,status_reciever='trash')
    return render(request,'trash.html',{'trsh':trash_msg,'key':my_name})

def block_user(request,id):
    my_id=request.session['yourself']
    my_details=Register_Tb.objects.filter(id=my_id)
    my_user_name=my_details[0].user_name
    check_user=Block_Tb.objects.filter(user_id=my_user_name,blocked_id_id=id)
    if check_user.count()>0:
        Block_Tb.objects.filter(user_id=my_user_name,blocked_id_id=id).delete()
    else:
        add_block=Block_Tb(user_id=my_user_name,blocked_id_id=id)
        add_block.save()
    return redirect('home')
