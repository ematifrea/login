from django.core.urlresolvers import reverse
from django.utils import timezone
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.mail import EmailMessage
from django.views.generic import View

from login.models import User, UserActivation
from login.forms import UserRegistration
from login.utils import hash_input


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
            user = User.objects.get(account_name=account_name, password=hash_input(password))
        except User.DoesNotExist:
            return render(request, 'login.html', {'recovery': 'Incorrect password', 'account_name': account_name})
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
                    message = 'The user %s was not activated. Check your email' % user.account_name
                    return render(request, 'login.html', {'message': message})
    else:
        return render_to_response('login.html', context_instance=context_instance)


def register(request):
    form = UserRegistration()
    if request.method == 'POST':
        form = UserRegistration(request.POST)
        if form.is_valid():
            new_user = User(
                account_name=request.POST['account_name'],
                full_name=request.POST['full_name'],
                email=request.POST['email'],
                password=hash_input(),
                last_login_date=timezone.now())
            new_user.save()
            activation_key = hash_input(request.POST['account_name'])
            ac = UserActivation(user=new_user, activation_key=activation_key)
            ac.save()
            print reverse('login:activate', args=(activation_key,))
            activation_url = request.get_host() + reverse('login:activate', args=(activation_key,))
            print activation_url
            email = EmailMessage('Account activation', 'the activation url %s' % activation_url,
                                 to=[request.POST['email']])
            email.send()
            request.session['account_name'] = request.POST['account_name']

            return render_to_response('confirm.html', {'new_user': new_user})
    return render_to_response('register.html', {'form': form}, context_instance=RequestContext(request))


def activate(request, **kwargs):
    try:
        user_activation = UserActivation.objects.get(activation_key=kwargs['activation_key'])
        if user_activation.key_expiration < timezone.now():
            message = 'The period of account activation has expired. Register again'
            return render(request, 'user_index.html', {'message': message})
        else:
            user_activation.active = True
            user_activation.save()
            user = User.objects.get(pk=user_activation.id)
            return render(request, 'user_index.html', {'user': user})
    except User.DoesNotExist:
        pass


def logout(request):
    try:
        account_name = request.session['account_name']
        del request.session['account_name']
    except KeyError:
        pass
    return render_to_response('logout.html', {'account_name': account_name})


def index(request):
    if not request.session.has_key('account_name'):
        return HttpResponseRedirect('login')
    else:
        return render_to_response('index.html',  {'account_name': request.session['account_name']})


def user_index(request):
    return render_to_response('user_index.html', {'user_id': request.session['user_id']})
