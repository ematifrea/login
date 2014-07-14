import base64
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.mail import EmailMessage
from django.views.generic import View, FormView, TemplateView, UpdateView, DetailView
from django.contrib import messages
from login.models import User, UserActivation
from login.forms import UserRegistration, EmailForm, ResetPassword, UserLoginForm
from login.utils import encrypt_input, check_inputs


class Index(TemplateView):
    template_name = 'index.html'

    def dispatch(self, request, *args, **kwargs):
        if not 'account_name' in self.request.session:
            return HttpResponseRedirect('login')
        else:
            return render_to_response('index.html',  {'account_name': request.session['account_name']})


class Login(FormView):
    form_class = UserLoginForm
    template_name = 'login.html'

    def form_valid(self, form):
        account_name = form.cleaned_data['account_name']
        password = form.cleaned_data['password']
        try:
            user = User.objects.get(account_name=account_name)
            if check_inputs(password, user.password):
                user = User.objects.get(account_name=account_name, password=user.password)
            else:
                messages = ['Incorrect password']
                return render_to_response(self.template_name,
                                          {'form': form,
                                           'account_name': account_name,
                                           'messages': messages})
        except User.DoesNotExist:
            messages.error(self.request, 'pls reg')
            return HttpResponseRedirect('register')
        is_active = False
        try:
            is_active = UserActivation.objects.get(user_id=user.id).active
        except UserActivation.DoesNotExist:
            pass
        finally:
            if is_active:
                self.request.session['account_name'] = user.account_name
                return HttpResponseRedirect(reverse('index'))
            else:
                message = 'The user %s was not activated. Check your email' % user.account_name
                return render_to_response(self.template_name, {'message': message})


class Register(FormView):
    form_class = UserRegistration
    template_name = 'register.html'

    def form_valid(self, form):
        new_user = User(account_name=form.cleaned_data['account_name'],
                        full_name=form.cleaned_data['full_name'],
                        email=form.cleaned_data['email'],
                        password=encrypt_input(form.cleaned_data['password']),
                        last_login_date=timezone.now())
        new_user.save()
        salt, activation_key = encrypt_input(form.cleaned_data['account_name']).split('$')
        ac = UserActivation(user=new_user, activation_key=activation_key)
        ac.save()
        activation_url = self.request.get_host() + reverse('login:activate', args=(activation_key,))
        email = EmailMessage('Account activation',
                             'The activation url for your account %s is %s'
                             % (form.cleaned_data['account_name'], activation_url),
                             to=[form.cleaned_data['email']])
        email.send()
        self.request.session['account_name'] = form.cleaned_data['account_name']

        return render_to_response('confirm.html', {'new_user': new_user},
                                  context_instance=RequestContext(self.request))


class Activate(TemplateView):
    template_name = 'user_index.html'

    @staticmethod
    def validate_activation(key):
        try:
            user_activation = UserActivation.objects.get(activation_key=key)
            if user_activation.key_expiration < timezone.now():
                message = 'The period of account activation has expired. Register again'
                return {'message': message}
            else:
                user_activation.active = True
                user_activation.save()
                user = User.objects.get(pk=user_activation.id)
                return {'user': user}
        except User.DoesNotExist:
            pass

    def get_context_data(self, **kwargs):
        return {'data': self.validate_activation(kwargs['activation_key'])}


class Logout(TemplateView):
    template_name = 'logout.html'

    def get_context_data(self, **kwargs):
        account_name = self.request.session['account_name']
        try:
            del self.request.session['account_name']
        except KeyError:
            pass
        return {'data': account_name}


class UserProfile(DetailView):
    template_name = 'profile.html'
    model = User

class UserEmailResetPassword(FormView):
    form_class = EmailForm
    template_name = 'email_for_reset_form.html'

    def get(self, request, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        return render_to_response(self.template_name,
                                  {'form': form, 'account_name': self.kwargs['account_name']},
                                  context_instance=RequestContext(self.request))

    def form_valid(self, form):
        user = User.objects.get(account_name=self.kwargs['account_name'])
        uidb64 = base64.b64encode(str(user.id))
        token, hsh = user.password.split('$')
        pswd_reset_url = self.request.get_host() + reverse('login:reset_password', args=(uidb64, token))
        email = EmailMessage('Password reset',
                             'The password reset link for the account %s is %s'
                             % (self.kwargs['account_name'], pswd_reset_url),
                             to=[form.cleaned_data['email']])
        email.send()
        return render_to_response(self.template_name, {'reset_message': 'check your email',
                                                       'account_name': self.kwargs['account_name']},
                                  context_instance=RequestContext(self.request))


class UserResetPassword(FormView):
    form_class = ResetPassword
    template_name = 'password_reset_form.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render_to_response(self.template_name, {'form': form,
                                                    'uidb64': self.kwargs['uidb64'],
                                                    'token': self.kwargs['token']})

    def form_valid(self, form):
        user = User.objects.get(pk=base64.b64decode(self.kwargs['uidb64']))
        user.password = encrypt_input(form.cleaned_data['password'])
        user.save()
        return HttpResponse('pswd reset done')
