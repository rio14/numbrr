from django.contrib import messages
from django.contrib.auth import login, authenticate, REDIRECT_FIELD_NAME
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LogoutView as BaseLogoutView, PasswordChangeView as BasePasswordChangeView,
    PasswordResetDoneView as BasePasswordResetDoneView, PasswordResetConfirmView as BasePasswordResetConfirmView,
)
import requests
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.crypto import get_random_string
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import View, FormView
from django.conf import settings

from .utils import (
    send_activation_email, send_reset_password_email, send_forgotten_username_email, send_activation_change_email,
)
from .forms import *
from .models import *

class GuestOnlyView(View):
    def dispatch(self, request, *args, **kwargs):
        # Redirect to the index page if the user already authenticated
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)

        return super().dispatch(request, *args, **kwargs)


class LogInView(GuestOnlyView, FormView):
    template_name = 'accounts/log_in.html'

    @staticmethod
    def get_form_class(**kwargs):
        if settings.DISABLE_USERNAME or settings.LOGIN_VIA_EMAIL:
            return SignInViaEmailForm

        if settings.LOGIN_VIA_EMAIL_OR_USERNAME:
            return SignInViaEmailOrUsernameForm

        return SignInViaUsernameForm

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        # Sets a test cookie to make sure the user has cookies enabled
        request.session.set_test_cookie()

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        request = self.request

        # If the test cookie worked, go ahead and delete it since its no longer needed
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()

        # The default Django's "remember me" lifetime is 2 weeks and can be changed by modifying
        # the SESSION_COOKIE_AGE settings' option.
        if settings.USE_REMEMBER_ME:
            if not form.cleaned_data['remember_me']:
                request.session.set_expiry(0)

        login(request, form.user_cache)

        redirect_to = request.POST.get(REDIRECT_FIELD_NAME, request.GET.get(REDIRECT_FIELD_NAME))
        url_is_safe = is_safe_url(redirect_to, allowed_hosts=request.get_host(), require_https=request.is_secure())

        if url_is_safe:
            return redirect(redirect_to)

        return redirect(settings.LOGIN_REDIRECT_URL)


# class SignUpView(GuestOnlyView, FormView):
#     template_name = 'accounts/sign_up.html'
#     form_class = SignUpForm
#
#     def form_valid(self, form):
#         request = self.request
#         user = form.save(commit=False)
#
#         if settings.DISABLE_USERNAME:
#             # Set a temporary username
#             user.username = get_random_string()
#         else:
#             user.username = form.cleaned_data['username']
#
#         if settings.ENABLE_USER_ACTIVATION:
#             user.is_active = True
#
#         # Create a user record
#         user.save()
#         messages.success(
#             request, _('New user created now login'))
#                 # Change the username to the "user_ID" form
#         if settings.DISABLE_USERNAME:
#             user.username = f'user_{user.id}'
#             user.save()
#
#         if settings.ENABLE_USER_ACTIVATION:
#             code = get_random_string(20)
#
#             act = Activation()
#             act.code = code
#             act.user = user
#             act.save()
#
#             send_activation_email(request, user.email, code)
#
#             messages.success(
#                 request, _('You are signed up. To activate the account, follow the link sent to the mail.'))
#         else:
#             raw_password = form.cleaned_data['password1']
#
#             user = authenticate(username=user.username, password=raw_password)
#             login(request, user)
#
#             messages.success(request, _('You are successfully signed up!'))
#
#         return redirect('index')

def register(request):
    if request.method == 'POST':
        uf = SignUpForm(request.POST)
        upf = ChangeProfileForm2(request.POST)
        if uf.is_valid() and upf.is_valid():
            print(uf)
            print(upf)
            user = uf.save()
            user.is_active = False
            user.save()
            # userprofile = upf.save(commit=False)#need to get the user profile object first
            print(request.POST.get('mobile'),)
            print(request.POST.get('SenderID'),)
            Userprofile.objects.create(
            owner = request.POST.get('username'),
            useraname = request.POST.get('username'),
            email = request.POST.get('email'),
            mobile = request.POST.get('mobile'),
            senderid = request.POST.get('SenderID'),
            area = request.POST.get('branch')
            )
            body = 'Thanks {} For Creating Account Your Account is currently disable'.format(request.POST.get('username'))
            send = requests.post("https://smsapi.24x7sms.com/api_2.0/SendSMS.aspx?APIKEY=IfNu2yr2CXc&MobileNo={0}&SenderID=Sharda&Message={1}&ServiceName=PROMOTIONAL_SPL".format(request.POST.get('mobile'),body))
            print(send)
            # userprofile.user = user #then set the user to user
            # userprofile.save() #then save to the database
            return redirect('accounts:log_in')
    else:
        uf = SignUpForm()
        upf = ChangeProfileForm2()
    return render(request, 'accounts/sign_up.html',{"form":uf, 'form2':upf})


class ActivateView(View):
    @staticmethod
    def get(request, code):
        act = get_object_or_404(Activation, code=code)

        # Activate profile
        user = act.user
        user.is_active = True
        user.save()

        # Remove the activation record
        act.delete()

        messages.success(request, _('You have successfully activated your account!'))

        return redirect('accounts:log_in')


class ResendActivationCodeView(GuestOnlyView, FormView):
    template_name = 'accounts/resend_activation_code.html'

    @staticmethod
    def get_form_class(**kwargs):
        if settings.DISABLE_USERNAME:
            return ResendActivationCodeViaEmailForm

        return ResendActivationCodeForm

    def form_valid(self, form):
        user = form.user_cache

        activation = user.activation_set.first()
        activation.delete()

        code = get_random_string(20)

        act = Activation()
        act.code = code
        act.user = user
        act.save()

        send_activation_email(self.request, user.email, code)

        messages.success(self.request, _('A new activation code has been sent to your email address.'))

        return redirect('accounts:resend_activation_code')


class RestorePasswordView(GuestOnlyView, FormView):
    template_name = 'accounts/restore_password.html'

    @staticmethod
    def get_form_class(**kwargs):
        if settings.RESTORE_PASSWORD_VIA_EMAIL_OR_USERNAME:
            return RestorePasswordViaEmailOrUsernameForm

        return RestorePasswordForm

    def form_valid(self, form):
        user = form.user_cache
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk)).decode()

        send_reset_password_email(self.request, user.email, token, uid)

        return redirect('accounts:restore_password_done')


class ChangeProfileView(LoginRequiredMixin, FormView):
    template_name = 'accounts/profile/change_profile.html'
    form_class = ChangeProfileForm

    def get_initial(self):
        user = self.request.user
        initial = super().get_initial()
        initial['username'] = user.username
        initial['email'] = user.email
        return initial

    def form_valid(self, form):
        user = self.request.user
        user.u = form.cleaned_data['username']
        user.email = form.cleaned_data['email']
        user.mobile = form.cleaned_data['mobile']
        user.area = form.cleaned_data['area']
        print(user.area)
        Userprofile.objects.create(
        owner=user.u,
        useraname=user.u,
        email=user.email,
        mobile=user.mobile,
        area=user.area
            )
        user.save()
        messages.success(self.request, _('Profile data has been successfully updated.'))
        return redirect('accounts:change_profile')
#
# def edit_profile(request):
#     if request.method == 'POST':
#         val = Userprofile.objects.all().filter(useraname=request.user).first()
#         print(val)
#         form = EditProfileForm(request.POST, instance=val)
#
#         if form.is_valid():
#             form.save()
#             return redirect(reverse('accounts:view_profile'))
#     else:
#         val = Userprofile.objects.all().filter(useraname=request.user).first()
#         print(val.serializable_value)
#         form = EditProfileForm(instance=val)
#
#         args = {'form': form}
#         return render(request, 'accounts/profile/change_profile.html', args)
#
#
# def edit_profile(request):
#     val= get_object_or_404(Userprofile,useraname=request.user)
#     form = EditProfileForm(request.POST or None, instance=val)
#     if form.is_valid():
#         a = form.cleaned_data['useraname']
#         # form.save()
#
#         messages.success(request, '{} Your profile was updated.'.format(a)) # ignored
#         return redirect('accounts:change_profile')
#     return render(request,  'accounts/profile/change_profile.html',
#      {'form':form})



class ChangeEmailView(LoginRequiredMixin, FormView):
    template_name = 'accounts/profile/change_email.html'
    form_class = ChangeEmailForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        initial['email'] = self.request.user.email
        return initial

    def form_valid(self, form):
        user = self.request.user
        email = form.cleaned_data['email']

        if settings.ENABLE_ACTIVATION_AFTER_EMAIL_CHANGE:
            code = get_random_string(20)

            act = Activation()
            act.code = code
            act.user = user
            act.email = email
            act.save()

            send_activation_change_email(self.request, email, code)

            messages.success(self.request, _('To complete the change of email address, click on the link sent to it.'))
        else:
            user.email = email
            user.save()

            messages.success(self.request, _('Email successfully changed.'))

        return redirect('accounts:change_email')


class ChangeEmailActivateView(View):
    @staticmethod
    def get(request, code):
        act = get_object_or_404(Activation, code=code)

        # Change the email
        user = act.user
        user.email = act.email
        user.save()

        # Remove the activation record
        act.delete()

        messages.success(request, _('You have successfully changed your email!'))

        return redirect('accounts:change_email')


class RemindUsernameView(GuestOnlyView, FormView):
    template_name = 'accounts/remind_username.html'
    form_class = RemindUsernameForm

    def form_valid(self, form):
        user = form.user_cache
        send_forgotten_username_email(user.email, user.username)

        messages.success(self.request, _('Your username has been successfully sent to your email.'))

        return redirect('accounts:remind_username')


class ChangePasswordView(BasePasswordChangeView):
    template_name = 'accounts/profile/change_password.html'

    def form_valid(self, form):
        # Change the password
        user = form.save()

        # Re-authentication
        login(self.request, user)

        messages.success(self.request, _('Your password was changed.'))

        return redirect('accounts:change_password')


class RestorePasswordConfirmView(BasePasswordResetConfirmView):
    template_name = 'accounts/restore_password_confirm.html'

    def form_valid(self, form):
        # Change the password
        form.save()

        messages.success(self.request, _('Your password has been set. You may go ahead and log in now.'))

        return redirect('accounts:log_in')


class RestorePasswordDoneView(BasePasswordResetDoneView):
    template_name = 'accounts/restore_password_done.html'


class LogOutView(LoginRequiredMixin, BaseLogoutView):
    template_name = 'accounts/log_out.html'
