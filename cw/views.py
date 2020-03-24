from django.shortcuts import render,redirect,HttpResponse
from  django.contrib.auth import authenticate,login,logout
from  django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import auth
from django.db.models import Q
from .models import Professor, Module, Instance, Rate
import json

def login(request):
    if request.method == 'POST':
        username = request.POST.get('user')
        pwd = request.POST.get('pwd')
        user = authenticate(username=username, password=pwd)
        if user:
            auth.login(request, user)
            # request.session.set_expiry(10)
            # request.session['username'] = username
            # request.session['is_login'] = True
            response = HttpResponse("登录成功")
            # response.set_cookie("is_login", True)
            return response
        else:
            return HttpResponse('Fail to login.')
    return HttpResponse('None')

def logout(request):
    auth.logout(request)
    request.session.flush()
    return HttpResponse('Logout.')

def reg(request):
    if request.method == 'POST':
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        email = request.POST.get('email')
        user = User.objects.create_user(username=user,password=pwd,email=email)
        user.save()
    return HttpResponse('Register.')

@login_required()
def list(request):
    # if request.session.get('is_login',None):
    # cookies = request.COOKIES
    # is_login = cookies.get("is_login")
    # if is_login:
    module_list = Instance.objects.all().values('module__mcode', 'module__mname', 'year', 'semester', 'professor__pid',
                                              'professor__pname')
    the_list = []
    for module in module_list:
        item = {'module_code': module['module__mcode'], 'module_name': module['module__mname'],
                'academic_years': module['year'], 'semester': module['semester'],
                'pid': module['professor__pid'], 'pname': module['professor__pname']}
        the_list.append(item)
    payload = {'module_list': the_list}
    http_response = HttpResponse(json.dumps(payload))
    http_response['Content-Type'] = 'application/json'
    http_response.status_code = 200
    http_response.reason_pharse = 'OK'
    return http_response

@login_required
def view(request):
    rate = Rate.objects.all()
    the_list = []
    rate_list = []
    for i in rate:
        flag = 0
        a = len(the_list)
        for m in range(a):
            if (i.professor.pid == the_list[m][0]):
                flag = 1
                the_list[m][2] = (i.rate + the_list[m][2]) / 2
        if (flag == 0):
            the_list.append([i.professor.pid, i.professor.pname, i.rate])
    for i in the_list:
        item = {'pid': i[0], 'pname': i[1], 'rate': i[2]}
        rate_list.append(item)
    payload = {'rate_list': rate_list}
    http_response = HttpResponse(json.dumps(payload))
    http_response['Content-Type'] = 'application/json'
    http_response.status_code = 200
    http_response.reason_pharse = 'OK'
    return http_response

@login_required
def average(request):
    if request.method == "POST":
        pro = request.POST.get('pro')
        module = request.POST.get('module')
        rate = Rate.objects.filter(Q(professor__pid=pro) & Q(module__mcode=module))
        x = 0
        p = ''
        m = ''
        for i in rate:
            x = x + i.rate
            p = i.professor.pname
            m = i.module.mname
        if (len(rate) == 0):
            x = 0
        else:
            x = x / len(rate)
        sen = 'The rating of ' + p + ' (' + pro + ') in module ' + m + ' (' + module + ') is ' + str(x)
        return HttpResponse(sen)

@login_required
def rate(request):
    professor_id = request.POST.get('professor_id')
    mcode = request.POST.get('module_code')
    year = request.POST.get('year')
    semester = request.POST.get('semester')
    rating = request.POST.get('rating')
    professor = Professor.objects.get(pid=professor_id)
    module = Module.objects.get(mcode=mcode)
    rate1 = Rate.objects.create(professor=professor, module=module, year=year, semester=semester, rate=int(rating))
    rate1.save()
    if rate1:
        return HttpResponse("Success")
    else:
        return HttpResponse("Fail")


def wrong(request):
    return HttpResponse('Wrong')