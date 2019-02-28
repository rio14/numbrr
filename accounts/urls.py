from django.urls import path
from mgmt.views import *
from .views import *
app_name = 'accounts'

urlpatterns = [
    path('log-in/', LogInView.as_view(), name='log_in'),
    path('log-out/', LogOutView.as_view(), name='log_out'),
    path('add_customer/', add_customer, name='add_customer'),
    path('send_msg/', send_msg, name='send_msg'),
    path('add_staff/', add_staff, name='add_staff'),
    path('add_branch/<name>/', add_branch, name='add_branch'),

    path('resend/activation-code/', ResendActivationCodeView.as_view(), name='resend_activation_code'),

    # path('sign-up/', SignUpView.as_view(), name='sign_up'),
    path('sign-up/', register, name='sign_up'),
    path('activate/<code>/', ActivateView.as_view(), name='activate'),

    path('restore/password/', RestorePasswordView.as_view(), name='restore_password'),
    path('restore/password/done/', RestorePasswordDoneView.as_view(), name='restore_password_done'),
    path('restore/<uidb64>/<token>/', RestorePasswordConfirmView.as_view(), name='restore_password_confirm'),

    path('remind/username/', RemindUsernameView.as_view(), name='remind_username'),

    path('change/profile/', ChangeProfileView.as_view(), name='change_profile'),
    # path('change/profile/', edit_profile, name='change_profile'),
    path('change/password/', ChangePasswordView.as_view(), name='change_password'),
    path('change/email/', ChangeEmailView.as_view(), name='change_email'),
    path('change/email/<code>/', ChangeEmailActivateView.as_view(), name='change_email_activation'),
]
