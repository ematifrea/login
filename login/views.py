from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from login.models import User
# Create your views here.
#
# def home(request):
#     return render(request, "home.html")

@csrf_protect
def login(request):
    if request.method == 'POST':
        account_name = request.POST['Username']
        password = request.POST['Password']
        user = User.objects.filter(account_name=account_name, password=password)
        if not user:
            return HttpResponseRedirect('register')
        elif request.session['user_id'] == user.id:
            return render(request, 'home.html')
        else:
            return HttpResponse('The user %s was not activated. Check your email' % user.account_name)
    elif request.method == "GET":
        return render(request,'login.html')

def register(request):
    return render(request, 'register.html')

def logout(request):
    try:
        del request.session['user_id']
    except KeyError:
        pass
    return HttpResponse("You're logged out.")