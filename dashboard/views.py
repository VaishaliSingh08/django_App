from django.core.files.storage import FileSystemStorage
from django.shortcuts import render,redirect
from djangoProject import  database_functions as db
from dummy.models import User, Products


## function for dashboard page
def dash(request):
    uid  = request.session['user_id_pk']
    details = db.get_all_object_from_id(User, uid)
    username = details[0]['user_name']
    user_img =  details[0] ['user_image']
    return  render(request, 'dashboard/index.html', {'username':username, 'user_img':user_img})

## function for user profile page(pedit user profile)
def user_profile(request):
    uid  = request.session['user_id_pk']
    details = db.get_all_object_from_id(User, uid)
    username = details[0]['user_name']
    email = details[0]['user_email']
    contact = details[0]['user_contact']
    qualifications = details[0]['user_qualification']
    password = details[0]['password']
    image = details[0]['user_image']
    user_img = details[0]['user_image']
    if request.method == "POST":
        # print(request.POST['update_profile'])

        username = request.POST['username']
        email = request.POST['email']
        contact = request.POST['user_contact']
        qualifications = request.POST['user_qualification']
        password = request.POST['password']
        # image = request.POST['image']
        myfile = request.FILES['image']

        fs = FileSystemStorage(location='media/user/')

        filename = fs.save(myfile.name, myfile)

        f_name = 'user/' + filename
        uploaded_file_url = fs.url(f_name)
        print(uploaded_file_url)

        error_msg = " "

        if len(contact) < 4:
            error_msg = "Phone number must be of 10 digits !!"
        elif len(contact) < 10:
            error_msg = "Phone number must be of 10 digits !!"
        print(error_msg)

        if error_msg == " ":
            user = User.objects.filter(user_id_pk=uid).update(user_name=username, user_email=email,
                                                             password=password,
                                                            user_image = uploaded_file_url,
                                                             user_qualification=qualifications,
                                                             user_contact=contact)



            return render(request, 'dashboard/profile.html',{'username':username, 'email':email, 'qualifications': qualifications,
                             'password':password, 'contact' : contact,'image':uploaded_file_url, 'user_img':user_img})
        else:
            return render(request, 'dashboard/profile.html',
                          {'username': username, 'email': email, 'qualifications': qualifications,
                           'password': password, 'contact': contact, "error_msg" :error_msg,'image':uploaded_file_url, 'user_img':user_img})

    return  render(request, 'dashboard/profile.html', {'username':username, 'email':email, 'qualifications': qualifications,
                             'password':password, 'contact' : contact, 'image':image,'user_img':user_img})


## To show final listing products page
def products(request):
    uid = request.session['user_id_pk']
    details = db.get_all_object_from_id(User, uid)
    username = details[0]['user_name']
    user_img = details[0]['user_image']
    if Products.objects.filter(user_id_fk=uid).exists():
        p = Products.objects.filter(user_id_fk=uid).values()
        data= {"p": p, "username" :username}
        return  render(request,'dashboard/product-list.html', data)
    return render(request, 'dashboard/product-list.html', {'username':username, 'user_img':user_img})


# Function for adding products
def add_product(request):
    uid = request.session['user_id_pk']
    details = db.get_all_object_from_id(User, uid)
    username = details[0]['user_name']
    user_img = details[0]['user_image']
    if request.method == "POST":
        # print(request.POST['trash'])

        p_name = request.POST['p_name']
        p_desc = request.POST['p_desc']
        p_price = request.POST['p_price']
        myfile = request.FILES['add_product']

        fs = FileSystemStorage(location='media/products/')

        filename = fs.save(myfile.name, myfile)

        f_name = 'products/' + filename
        uploaded_file_url = fs.url(f_name)
        print(uploaded_file_url)
        products = Products.objects.create(p_name=p_name, p_price=p_price, p_desc=p_desc,
                                           p_image=uploaded_file_url, user_id_fk=uid)

        products.save()

        return redirect('products')

    return render(request, 'dashboard/product-edit.html', {'username':username, 'user_img': user_img})


# Function to delete any product
def delete(request, id):
    uid = request.session['user_id_pk']
    p = Products.objects.filter(user_id_fk=uid, p_id_pk=id).values()
    pid = p[0]['p_id_pk']
    print(pid)
    Products.objects.filter(p_id_pk=pid).delete()

    return redirect('products')


# Function to edit any product information
def edit_product(request, id):
    uid = request.session['user_id_pk']
    details = db.get_all_object_from_id(User, uid)
    username = details[0]['user_name']
    user_img = details[0]['user_image']
    p = Products.objects.filter(user_id_fk=uid, p_id_pk= id).values()

    p_name =  p[0]['p_name']
    p_desc = p[0]['p_desc']
    p_price =  p[0]['p_price']
    p_image = p[0]['p_image']
    print('p1', p)
    pid = p[0]['p_id_pk']

    if request.method == "POST":
        p_name = request.POST['p_name']
        p_desc = request.POST['p_desc']
        p_price = request.POST['p_price']


        if request.method == "FILES":
            myfile = request.FILES['update']

            print(myfile)

            fs = FileSystemStorage(location='media/products/')

            filename = fs.save(myfile.name, myfile)

            f_name = 'products/' + filename
            uploaded_file_url = fs.url(f_name)
            print(uploaded_file_url)
            user = Products.objects.filter(p_id_pk=id).update(p_name=p_name, p_price=p_price, p_desc=p_desc,
                                               p_image=uploaded_file_url)


            return render(request, 'dashboard/profile11.html',{'p_name': p_name, 'p_price': p_price, 'p_desc': p_desc,
                                                                   'p_image': uploaded_file_url, 'username':username, 'user_img':user_img})


        user = Products.objects.filter(p_id_pk=id).update(p_name=p_name, p_price=p_price, p_desc=p_desc)
        return render(request, 'dashboard/profile11.html', {'p_name': p_name, 'p_price': p_price, 'p_desc': p_desc, 'username':username,'p_image': p_image, 'pid':pid, 'user_img':user_img})


    return render(request, 'dashboard/profile11.html',{'p_name': p_name, 'p_price': p_price, 'p_desc': p_desc,
                                                               'p_image': p_image, 'pid':pid,'username':username, 'user_img':user_img})


# Function to show all products on website page
def show_products(request):
    p = Products.objects.all().values()
    data = {"p": p}
    return render(request, 'home/index.html', data)

def home(request):

    return render(request, 'home/index.html')



