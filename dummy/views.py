from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse
from dummy.models import User
from django.core.files.storage import FileSystemStorage
import re
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from djangoProject import database_functions




### Function for registering user(Sign UP)
def index(request):
    if request.method == 'POST' and  request.FILES['user_image']:
        user_name = request.POST['username']
        user_email = request.POST['email']
        user_contact = request.POST['user_contact']
        user_qualification = request.POST['user_qualification']
        password_one = request.POST['password_one']
        password_two = request.POST['password_two']
        myfile = request.FILES['user_image']

        fs = FileSystemStorage(location='media/user/')

        filename = fs.save(myfile.name, myfile)

        f_name = 'user/'+filename
        uploaded_file_url = fs.url(f_name)
        print(uploaded_file_url)


        #validation
        value = {
            'user_name':user_name,
            'user_email' : user_email,
            'user_contact' : user_contact,
            'user_qualification' : user_qualification,
        }
        #
        error_msg = " "
        #
        # regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
        #
        # if (re.search(regex, user_email)):
        #     print("okay")
        # else:
        #     error_msg = "Invalid Email !!"
        #
        # if len(user_contact) < 4:
        #     error_msg = "Phone number must be of 10 digits !!"
        # elif len(user_contact) > 10 :
        #     error_msg = "Phone number must be of 10 digits !!"
        # elif password_one != password_two:
        #     error_msg = "Passwords not matching !!"
        if User.objects.filter(user_name = user_name).exists():
            error_msg = "Username taken !!"
        elif User.objects.filter(user_email = user_email).exists():
            error_msg = "Email taken !!"
        success = ""
        if error_msg == " ":
            user = User.objects.create(user_name = user_name, user_email=user_email,password= password_one,
                                       cnfrm_pass=password_two, user_qualification=user_qualification,
                                       user_contact= user_contact, user_image= uploaded_file_url)
            user.is_active = False
            user.save()

            user_id =user.user_id_pk

            domain =  get_current_site(request).domain
            # link = reverse('activate',kwargs={"user_id":user_id,'token':token_generator.make_token(user)})
            link = reverse('activate',kwargs={"user_id":user_id})

            activate_url = "http://"+domain+link
            email_subject = "ACTIVATE YOUR ACCOUNT !!"
            email_body = "Hi" + user.user_name + 'Please use this link to verify your account\n' + activate_url
            email = EmailMessage(
                email_subject,
                email_body,
                'noreply@dummy.com',
                [user_email],
            )
            email.send(fail_silently=False)
            success = "Please check your email to verify your account !!"

            return render(request, 'home/sign_up.html', {'success': success})

        else:
            data = {
                'error_msg' : error_msg,
                'values' : value
            }
            return render(request, 'home/sign_up.html',data)

    else:
        return render(request, 'home/sign_up.html')



## Email Verification View
class VerificationView(View):
    def get(self, request, user_id):
        print(user_id)
        database_functions.update_user_status(user_id)
        return redirect('confirmation')

## Email confirmation
def confirmation(request):
    return render(request, 'home/confirmation.html')

## Function for log in to dashboard
def login(request):
    if request.method == 'POST':
        user_email = request.POST['email']
        password_one = request.POST['password']
        user_valid = database_functions.check_user_exist(user_email, password_one)
        error_msg = ''
        if user_valid:
            request.session['user_email'] = user_email
            uid = database_functions.get_id(User, user_email)
            user_id = uid[0]['user_id_pk']
            request.session['user_id_pk'] = user_id

            return redirect('dash')
        else:
            error_msg = "Credentials do not match !!"
            return render(request, 'home/login.html', {'error_msg':error_msg})
    else:
        return render(request, 'home/login.html')

## Function to logout from dashboard
def logout(request):
    try:
        del request.session['user_email']
        del request.session['user_id_pk']
        return redirect('login')
    except KeyError:
        pass
        return redirect('login')


##Function to render home page
def home(request):
    return render(request, 'home/index.html')

