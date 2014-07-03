from django.core.urlresolvers import reverse
from django.utils import timezone
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from login.models import User, UserActivation
from login.forms import UserRegistration
import hashlib, random

def login(request):
    context_instance = RequestContext(request)
    if request.method == 'POST':
        account_name = request.POST['account_name']
        password = request.POST['password']
        try:
            user = User.objects.get(account_name=account_name)
        except User.DoesNotExist:
            return HttpResponseRedirect('register')
        try:
            user = User.objects.get(account_name=account_name, password=password)
        except User.DoesNotExist:
            return render(request, 'login.html', {'message' : 'Incorrect credentials', 'account_name': account_name})
        finally:
            if user.active:
                request.session['account_name'] = user.account_name
                return HttpResponseRedirect(reverse('index'))
            elif not user.active:
                return HttpResponse('The user %s was not activated. Check your email' % user.account_name)
    else:
        return render_to_response('login.html', context_instance=context_instance)

def register(request):
    form = UserRegistration()
    if request.method == 'POST':
        form = UserRegistration(request.POST)
        if form.is_valid():
            new_user = User(account_name=request.POST['account_name'], full_name=request.POST['full_name'],
                            email=request.POST['email'], password=request.POST['password'], last_login_date=timezone.now())
            new_user.save()
            salt = hashlib.new(str(random.random())).hexdigest()[:5]
            activation_key = hashlib.new(salt+new_user.username).hexdigest()
            UserActivation.save(user_id=new_user.id, activation_key=activation_key)

            # send activation email
            return HttpResponseRedirect(reverse('index'))
        else:
            form = UserRegistration()
    return render_to_response('register.html', {'form': form}, context_instance=RequestContext(request))

def logout(request):
    try:
        del request.session['account_name']
    except KeyError:
        pass
    return HttpResponse("You're logged out.")

def index(request):
    if not request.session.has_key('account_name'):
        return HttpResponseRedirect('login')
    else:
        return render_to_response('index.html',  {'account_name': request.session['account_name']})