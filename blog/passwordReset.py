from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template import loader
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
# from settings import DEFAULT_FROM_EMAIL
from django.conf import settings
from django.views.generic import *
from .forms import PasswordResetRequestForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models.query_utils import Q

class ResetPasswordRequestView(FormView):
    template_name = "registration/password_reset_form.html"    #code for template is given below the view's code
    # success_url = '/account/login'
    success_url = reverse_lazy('password_reset_done')
    form_class = PasswordResetRequestForm

    @staticmethod
    def validate_email_address(email):
        '''
        This method here validates the if the input is an email address or not. Its return type is boolean, True if the input is a email address or False if its not.
        '''
        try:
            validate_email(email)
            return True
        except ValidationError:
            return False

    def post(self, request, *args, **kwargs):
        '''
        A normal post request which takes input from field "email_or_username" (in ResetPasswordRequestForm).
        '''
        form = self.form_class(request.POST)
        if form.is_valid():
            data= form.cleaned_data["email_or_username"]
        if self.validate_email_address(data) is True:                 #uses the method written above
            '''
            If the input is an valid email address, then the following code will lookup for users associated with that email address. If found then an email will be sent to the address, else an error message will be printed on the screen.
            '''
            associated_users= User.objects.filter(Q(email=data)|Q(username=data))
            print(associated_users)
            if associated_users.exists():
                for user in associated_users:
                        c = {
                            'email': user.email,
                            'domain': request.META['HTTP_HOST'],
                            'site_name': 'localhost',
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'user': user,
                            'token': default_token_generator.make_token(user),
                            'protocol': 'http',
                            }
                        subject_template_name='registration/password_reset_subject.txt'
                        # copied from django/contrib/admin/templates/registration/password_reset_subject.txt to templates directory
                        email_template_name='registration/password_reset_email.html'
                        # copied from django/contrib/admin/templates/registration/password_reset_email.html to templates directory
                        subject = loader.render_to_string(subject_template_name, c)
                        # Email subject *must not* contain newlines
                        subject = ''.join(subject.splitlines())
                        email = loader.render_to_string(email_template_name, c)
                        success = send_mail(subject, email, settings.DEFAULT_FROM_EMAIL , [user.email], fail_silently=True)
                if not success:
                    result = self.form_invalid(form)
                    messages.error(request, "Could not send password reset mail. Please try again.")
                    return result
                else:
                    result = self.form_valid(form)
                    messages.success(request, 'On ' + data +"'s email address.")
                    return result
            elif not associated_users.exists():
                # print("not exist") ---> working
                result = self.form_invalid(form)
                messages.error(request, 'No user is associated with this email address')
                return result
        else:
            '''
            If the input is an username, then the following code will lookup for users associated with that user. If found then an email will be sent to the user's address, else an error message will be printed on the screen.
            '''
            associated_users= User.objects.filter(username=data)
            print(associated_users)
            if associated_users.exists():
                for user in associated_users:
                    c = {
                        'email': user.email,
                        'domain': request.META['HTTP_HOST'], #or your domain
                        'site_name': 'localhost',
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'user': user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                        }
                    subject_template_name='registration/password_reset_subject.txt'
                    email_template_name='registration/password_reset_email.html'
                    subject = loader.render_to_string(subject_template_name, c)
                    # Email subject *must not* contain newlines
                    subject = ''.join(subject.splitlines())
                    email = loader.render_to_string(email_template_name, c)
                    success = send_mail(subject, email, settings.DEFAULT_FROM_EMAIL , [user.email], fail_silently=True)
                if not success:
                    result = self.form_invalid(form)
                    messages.error(request, "Could not send password reset mail. Please try again.")
                    return result
                else:
                    result = self.form_valid(form)
                    messages.success(request, 'On ' + data +"'s email address.")
                    return result
            elif not associated_users.exists():
                result = self.form_invalid(form)
                messages.error(request, 'This username does not exist in the system.')
                return result
        messages.error(request, 'Invalid Input')
        return self.form_invalid(form)
