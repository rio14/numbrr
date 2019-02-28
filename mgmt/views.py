from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import *
from django.conf import settings
from django.contrib import messages
import requests
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.forms import UserCreationForm
from accounts.models import *

def send_msg(request):
    body = request.POST.get('body')
    # num = request.POST.get('area')
    num2 = request.POST.get('subarea')
    print(num2)
    print(body)
    print(request.user)
    if num2:
        if num2 == '1' and body:
            contact_list = Customer.objects.all().filter(owner = request.user)

        else:
            contact_list = Customer.objects.all().filter(owner = request.user, area__iexact=num2.lstrip())
        contact = [num for num in contact_list]
        contact_list2 = []
        for i in range(len(contact)):
            contact_list2.append(contact[i].mobile)
        print(contact_list2)
        a =  ",".join([str(x) for x in contact_list2])
        print(a)
        if a:

            send = requests.post("https://smsapi.24x7sms.com/api_2.0/SendSMS.aspx?APIKEY=IfNu2yr2CXc&MobileNo={0}&SenderID=Sharda&Message={1}&ServiceName=PROMOTIONAL_SPL".format(a,body))
            print(send)
    area = Userprofile.objects.all().filter(owner = request.user)
    # staff = Staff.objects.value('owner').filter(name=request.user)

    contact = [num for num in area]
    area = []
    for i in range(len(contact)):
        area.append(contact[i].area)
    # print(contact_list2)
    a =  ",".join([str(x) for x in area])
    d = list(a.split(","))
    b = {}
    c = 0
    for v in d:
        b[v] = c
        c+=1
    # print(b)
    # print(a)
    # print(list(a.split(",")))

    subarea = Customer.objects.values('subarea').filter(owner = request.user).distinct()
    return render(request, 'accounts/sent/send_msg.html', {'area':b,'subarea':subarea})

def send_msg_to(request):
    no_by_contact = Customer.objects.all().filter(owner = request.user,mobile__gt=1)
    contact = [num for num in no_by_contact]
    contact_list = ['8770919212','9111199991','9976744444']
    # for i in range(len(contact)):
    #     contact_list.append(contact[i].mobile)
    # print(contact_list)
    a = '8770919212'
    # a = ','.join(contact_list)
    a = ",".join([str(x) for x in contact_list])
    print(a)
    # send = requests.get("http://137.59.52.74/api/mt/SendSMS?user=ritesh01&password=ritesh01&senderid=WISHES&channel=Trans&DCS=8&flashsms=0&number={0}&text={1}&route=01".format(a,query2))
    # for n in contact_list:
    #     print(n)
    send = requests.post("https://smsapi.24x7sms.com/api_2.0/SendSMS.aspx?APIKEY=IfNu2yr2CXc&MobileNo={}&SenderID=Sharda&Message=testing&ServiceName=PROMOTIONAL_SPL".format(a))
    print(send)
    # print('sending {} to {} numbers'.format(query2,no_by_address))
    return HttpResponse('msg sent')


def add_customer(request):
    if request.user.is_staff:
        staff_name = Staff.objects.all().filter(name=request.user)
        staff = [num for num in staff_name]
        s = []
        for i in range(len(staff)):
            s.append(staff[i].owner)
        # print(contact_list2)
        a =  ",".join([str(x) for x in s])
        print(a)

    if request.method == 'POST':
        form = Add_customer(request.POST or None)
        if form.is_valid():
            print(request.user.is_staff)
            # print(Staff.objects.values('owner').filter(name=request.user))
            if request.user.is_staff:
                name = form.cleaned_data['name']
                email = form.cleaned_data['email']
                mobile = form.cleaned_data['mobile']
                dob = form.cleaned_data['dob']
                area = form.cleaned_data['area']
                subarea = form.cleaned_data['subarea']
                city = form.cleaned_data['city']
                ani = form.cleaned_data['ani']
                Customer.objects.create(
                owner = a,
                name = name,
                email = email,
                mobile = mobile,
                dob = dob,
                area = area,
                subarea = subarea,
                city = city,
                anniversary = ani
                )
            else:
                name = form.cleaned_data['name']
                email = form.cleaned_data['email']
                mobile = form.cleaned_data['mobile']
                dob = form.cleaned_data['dob']
                area = form.cleaned_data['area']
                subarea = form.cleaned_data['subarea']
                city = form.cleaned_data['city']
                ani = form.cleaned_data['ani']
                Customer.objects.create(
                owner = request.user,
                name = name,
                email = email,
                mobile = mobile,
                dob = dob,
                area = area,
                subarea = subarea,
                city = city,
                anniversary = ani
                )
            messages.success(
                request,('New Customer successfully Added'))
            return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        form = Add_customer()
    # area = Userprofile.objects.values('area').filter(owner = request.user)
    # a = ",".join([str(x) for x in area])
    # print(a)
    if request.user.is_staff:
        contact_list = Userprofile.objects.all().filter(owner = a)
    else:
        contact_list = Userprofile.objects.all().filter(owner = request.user)
    contact = [num for num in contact_list]
    contact_list2 = []
    for i in range(len(contact)):
        contact_list2.append(contact[i].area)
    # print(contact_list2)
    a =  ",".join([str(x) for x in contact_list2])
    d = list(a.split(","))
    b = {}
    c = 0
    for v in d:
        b[v] = c
        c+=1
    # print(b)
    # print(a)
    # print(list(a.split(",")))
    return render(request, 'accounts/add_customer/add.html', {
        'form':form, 'area':b
    })


def add_branch(request, name):
    if request.method == 'POST':
        t = Userprofile.objects.get(useraname=name)
        form = Add_branch(request.POST)
        data = Userprofile.objects.only('area').filter(useraname=name)
        if form.is_valid():
            print(request.POST.get('branch'))
            t = Userprofile.objects.get(useraname=name)
            b = ',{}'.format(request.POST.get('branch'))
            t.area += b
            t.save()
            messages.success(
                request,('New Branch successfully Added'))
            return render(request, 'accounts/add_customer/add_branch.html', {'form': form, 'data':data})
    else:
        form = Add_branch()
        data = Userprofile.objects.only('area').filter(useraname=name)

    return render(request, 'accounts/add_customer/add_branch.html', {'form': form, 'data':data})

def add_staff(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data.get('username'))
            user = form.save()
            print(user)
            user.is_staff = True
            user.email = request.POST.get('email')
            user.save()
            # name = request.POST.get('username'),
            # email = request.POST.get('email'),
            a = request.POST.get('username')
            b = request.POST.get('email')
            c = request.POST.get('mobile')

            Staff.objects.create(
            owner = request.user,
            name = a,
            email = b,
            mobile = c
            )

            # username = form.cleaned_data.get('username')
            # raw_password = form.cleaned_data.get('password1')
            # user = authenticate(username=username, password=raw_password)
            # login(request, user)
            messages.success(
                request,('New Staff successfully Added'))
            return render(request, 'accounts/add_staff/add_staff.html', {'form': form})
    else:
        form = UserCreationForm()
    return render(request, 'accounts/add_staff/add_staff.html', {'form': form})
