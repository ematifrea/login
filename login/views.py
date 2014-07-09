import base64
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.mail import EmailMessage
from django.views.generic import View

from login.models import User, UserActivation
from login.forms import UserRegistration, EmailForm, ResetPassword
from login.utils import encrypt_input, check_inputs


def login(request):
    context_instance = RequestContext(request)
    if request.method == 'POST':
        account_name = request.POST['account_name']
        password = request.POST['password']
        try:
            user = User.objects.get(account_name=account_name)
            print check_inputs(password, user.password)
            if check_inputs(password, user.password):
                user = User.objects.get(account_name=account_name, password=user.password)
            else:
                return render(request, 'login.html', {'recovery': 'Incorrect password', 'account_name': account_name})
        except User.DoesNotExist:
            return HttpResponseRedirect('register')
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
                password=encrypt_input(request.POST['password']),
                last_login_date=timezone.now())
            new_user.save()
            salt, activation_key = encrypt_input(request.POST['account_name']).split('$')
            ac = UserActivation(user=new_user, activation_key=activation_key)
            ac.save()
            activation_url = request.get_host() + reverse('login:activate', args=(activation_key,))
            email = EmailMessage('Account activation',
                                 'The activation url for your account %s is %s'
                                 % (request.POST['account_name'], activation_url),
                                 to=[request.POST['email']])
            email.send()
            request.session['account_name'] = request.POST['account_name']

            return render_to_response('confirm.html', {'new_user': new_user},
                                      context_instance=RequestContext(request))
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
    if request.session.has_key('account_name'):
        account_name = request.session['account_name']
    try:
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


class UserEmailResetPassword(View):
    form_class = EmailForm
    template_name = 'email_for_reset_form.html'

    def get(self, request, account_name):
        form = self.form_class()
        return render(request, self.template_name, {'form': form, 'account_name': account_name})

    def post(self, request, account_name):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = User.objects.get(account_name=account_name)
            uidb64 = base64.b64encode(str(user.id))
            token, hsh = user.password.split('$')
            pswd_reset_url = request.get_host() + reverse('login:reset_password', args=(uidb64, token))
            email = EmailMessage('Password reset',
                                 'The password reset link for the account %s is %s'
                                 % (account_name, pswd_reset_url),
                                 to=[request.POST['email']])
            email.send()
            print pswd_reset_url
            return HttpResponse('check email to reset')
        return render(request, self.template_name, {'form': form})


class UserResetPassword(View):
    form_class = ResetPassword
    template_name = 'password_reset_form.html'

    def get(self, request, uidb64, token):
        form = self.form_class()
        return render(request, self.template_name, {'form': form, 'uidb64': uidb64, 'token': token})

    def post(self, request, uidb64, token):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = User.objects.get(pk=base64.b64decode(uidb64))
            user.password = encrypt_input(request.POST['password'])
            user.save()
            return HttpResponse('pswd reset done')
        return render(request, self.template_name, {'form': form})