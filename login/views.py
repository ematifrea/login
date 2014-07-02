from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from login.models import User


def login(request):
    if request.method == 'POST':
        account_name = request.POST['Username']
        password = request.POST['Password']
        user = User.objects.get(account_name=account_name, password=password)

        if not user:
            return HttpResponseRedirect('register')
        else:
            if user.active:
                request.session['account_name'] = user.account_name
                return HttpResponse(index(request))
            elif not user.active:
                return HttpResponse('The user %s was not activated. Check your email' % user.account_name)
    # elif request.method == "GET":
    #     return render(request,'login.html')

def register(request):
    return render(request, 'register.html')

def logout(request):
    try:
        del request.session['account_name']
    except KeyError:
        pass
    return HttpResponse("You're logged out.")

def index(request):
    if not request.session.has_key('account_name'):
        return render(request, 'login.html')
    else:
        context = RequestContext(request)
        context_dict =  {'account_name': request.session['account_name']}
        return render_to_response('index.html', context_dict, context)