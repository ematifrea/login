from django.core.urlresolvers import reverse
from django.utils import timezone
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.mail import EmailMessage

from login.models import User, UserActivation
from login.forms import UserRegistration
import hashlib
import random

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
            is_active = False
            try:
                is_active = UserActivation.objects.get(user_id=user.id).active
            except UserActivation.DoesNotExist:
                pass
            finally:
                if is_active:
                    request.session['account_name'] = user.account_name
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return HttpResponse('The user %s was not activated. Check your email' % user.account_name)
    else:
        return render_to_response('login.html', context_instance=context_instance)

def register(request):
    form = UserRegistration()
    if request.method == 'POST':
        form = UserRegistration(request.POST)
        if form.is_valid():
            registration_dict = {'account_name': request.POST['account_name'],
                                 'full_name': request.POST['full_name'],
                                 'email': request.POST['email'],
                                 'password': request.POST['password'],
                                 'last_login_date': timezone.now()}

            salt = hashlib.new(str(random.random())).hexdigest()[:5]
            registration_dict['activation_key'] = hashlib.new(salt+registration_dict['account_name']).hexdigest()
            new_user_id = User().save(registration_dict)
            activation_url = reverse('login:user_index', args=(new_user_id,))

            print activation_url

            email = EmailMessage('Account activation', 'the activation url', to=[request.POST['email']])
            email.send()
            request.session['account_name'] = request.POST['account_name']

            url = reverse('login:user_index', args=(new_user_id,))
            message = 'An activation email has been sent.'
            print url
            return HttpResponseRedirect(reverse(url))
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

def user_index(request):
    return render_to_response('user_index.html', {'user_id': request.session['user_id']})