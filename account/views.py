from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.generic import DetailView, CreateView, View
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, PasswordResetForm

from django.urls import reverse_lazy
from .forms import SignUpForm, UserEditForm, PasswordEditForm, ProfilePageForm, ResetPasswordForm
from theblog.models import profile, post, category, link 
from django.core.paginator import Paginator
from hitcount.views import HitCountDetailView

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin 
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode

from django.contrib.auth.models import User
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from .tokens import account_activation_token

def login_user(request):

	#form_class = UserLoginForm
	logout(request)
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)

		if user is not None:
				if user.is_active:
					login(request, user)
					messages.success(request, ("Welcome " + username + " have Logged in Successfuly! "))
					return HttpResponseRedirect('/')
		else:
			messages.error(request, ("Something went wrong, Try Again! "))
			return redirect('login')

	else:	
		return render(request, 'registration/login.html', {})


def logout_user(request):
	logout(request)
	messages.success(request, "You have Logged Out Successfuly! ")
	return HttpResponseRedirect('/')


class UserSignUp(generic.CreateView):
	form_class = SignUpForm
	template_name = 'registration/register.html'
	success_url = reverse_lazy('login')

	def get(self, request, *args, **kwargs):
		form =self.form_class()
		return render(request, self.template_name, {'form':form})
        
	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.is_active = False
			user.save()
			current_site = get_current_site(request)
			subject = 'Activate Your MySite Account'
			message = render_to_string('registration/account_activation_email.html', {
                'user': user,
				'name': current_site.name,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
			user.email_user(subject, message)
			messages.success(request, ('Please Confirm your email to complete registration.'))
			return redirect('login')
            
		return render(request, self.template_name, {'form': form})
            
class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.email_confirmed = True
            user.save()
            login(request, user)
            messages.success(request, ('Your account have been confirmed.'))
            return redirect('index')
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('index')

            


class ResetPasswordView(PasswordResetView):
	form_class = PasswordResetForm
	template_name = 'registration/password_reset.html'
	email_template_name = 'registration/password_reset_email.html'
	subject_template_name = 'registration/password_reset_subject.txt'
	success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
	success_url = reverse_lazy('login') 
	

# class PasswordResetConfirmView(PasswordResetConfirmView):

# class PasswordResetCompleteView(PasswordResetCompleteView):
#--------------------------------------------------------------------------------------------------------------------------------------------------------#


# Create your views here.
class ShowProfile(DetailView):
	model = profile 
	template_name = 'registration/user_profile.html'

	def get_context_data(self, *args, **kwargs):
	    users = profile.objects.all()
	    context = super(ShowProfile, self).get_context_data(*args, **kwargs)
	    context.update({'posts': post.objects.filter(publish__isnull=False, status='published', approved=True).all().order_by('-publish',)})
	    context.update({'approve': post.objects.filter(publish__isnull=False, status='published', approved=False).all().order_by('-publish',)})
	    context.update({'popular_posts': post.objects.filter(approved=True, status='published').order_by('-hit_count_generic__hits')[0:5],})
		
	    page_user = get_object_or_404(profile, id=self.kwargs['pk'])
	    context["link"] = link
	    context["page_user"] = page_user
	    return context

class DraftProfile(DetailView):
	model = profile 
	template_name = 'registration/user_draft.html'

	def get_context_data(self, *args, **kwargs):
	    users = profile.objects.all()
	    context = super(DraftProfile, self).get_context_data(*args, **kwargs)
	    context.update({'draft': post.objects.filter(publish__isnull=False, status='draft').all().order_by('-publish',)})
	    context.update({'popular_posts': post.objects.filter(approved=True, status='published').order_by('-hit_count_generic__hits')[0:5],})
		
	    page_user = get_object_or_404(profile, id=self.kwargs['pk'])
	    context["page_user"] = page_user
	    return context



class EditProfilePage(generic.UpdateView):
	model = profile
	template_name = 'registration/edit_profile_page.html'
	form_class = ProfilePageForm
	# fields = ['bio', 'profile_pic', 'website_url', 'facebook_url', 'instagram_url', 'twitter_url', 'pinterest_url']
	success_url = reverse_lazy('index')
	
	def edit(self, request):

		messages.success(request, "You have Logged Out Successfuly! ")
		return redirect(reverse_lazy('index'))
	


class CreateProfilePage(generic.CreateView):
	model = profile
	template_name = 'registration/create_profile_page.html'
	form_class = ProfilePageForm

	def form_valid(self, form, request):
		form.instance.user = self.request.user
		return super().form_valid(form)

		messages.success(request, "You have created account Successfuly! ")
		return redirect('index')



	
class EditProfile(generic.UpdateView):
	form_class = UserEditForm
	template_name = 'registration/edit_profile.html'
	success_url = reverse_lazy('index')

	def get_object(self):
		return self.request.user

class PasswordEditView(PasswordChangeView):
	form_class = PasswordEditForm
	template_name='registration/change_password.html'
	success_message = "Successfully Changed Your Password"
	#success_url = reverse_lazy('index')
	success_url = reverse_lazy('password_success')

def password_success(request):
	messages.success(request, ("Password changed Successfuly! "))
	return render(request, 'registration/password_success.html')
