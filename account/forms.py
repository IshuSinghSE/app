from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, PasswordResetForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django import forms
from theblog.models import profile

class SignUpForm(UserCreationForm):
	email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}))
	first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}))
	last_name = forms.CharField(max_length=100, help_text='Enter a valid email address', widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}))

	class Meta:
		model = User 
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control form-control-lg'	
		self.fields['password1'].widget.attrs['class'] = 'form-control form-control-lg'
		self.fields['password2'].widget.attrs['class'] = 'form-control form-control-lg'

	# def cleaned(self):
		# cleaned_data=super.cleaned()
		# if user.objects.filter(username=cleaned_data["username"].exists()):
			# raise ValidationError("The username is taken, please try another one!")


class UserEditForm(forms.ModelForm):
	username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}))
	first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}))
	last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}))
	email = forms.EmailField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'type':'email'}))	
	#last_login = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}))
	#is_superuser = forms.CharField(max_length=100, widget=forms.CheckboxInput(attrs={'class': 'form-check form-check-lg'}))
	#is_staff = forms.CharField(max_length=100, widget=forms.CheckboxInput(attrs={'class': 'form-check form-check-lg'}))
	#is_active = forms.CharField(max_length=100, widget=forms.CheckboxInput(attrs={'class': 'form-check form-check-lg'}))
	#date_joined = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'type':'readonly'}))

	class Meta:
		model = User 
		fields = ('username', 'first_name', 'last_name', 'email')

		def __init__(self, *args, **kwargs):
			super(UserChangeForm, self).__init__(*args, **kwargs)
	

class PasswordEditForm(PasswordChangeForm):
	old_password= forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg'}))
	new_password1 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg'}))
	new_password2 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg'}))	
	
	class Meta:
		model = User 
		fields = ('old_password','new_password1','new_password2')	

	def __init__(self, *args, **kwargs):
		super(PasswordChangeForm, self).__init__(*args, **kwargs)
		self.fields['new_password1'].label = "New password"	
		self.fields['new_password2'].label = "Comfirm password"

class ResetPasswordForm(PasswordResetForm):

	email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}))

	class Meta:
		model = User
		fields = ('email')

	def __init__(self, *args, **kwargs):
		super(ResetPasswordForm, self).__init__(*args, **kwargs)

	

class ProfilePageForm(forms.ModelForm):
	class Meta:
		model = profile
		fields = ('profile_pic', 'bio', 'facebook_url', 'instagram_url', 'twitter_url', 'pinterest_url', 'website_url')
		
		widgets = {
			'bio': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
			'profile_pic': forms.FileInput(attrs={'class': '', 'accept':'image/*' , 'class':'file-upload' }),
			'facebook_url': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
			'instagram_url': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
			'twitter_url': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
			'pinterest_url': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
			'website_url': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),

			}

'''
class UserLoginForm(UserChangeForm):
	username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}))
	password= forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg'}))
	
	class Meta:
		model = User 
		fields = ('username', 'password')

	def __init__(self, *args, **kwargs):
		super(UserChangeForm, self).__init__(*args, **kwargs)

	

'''
