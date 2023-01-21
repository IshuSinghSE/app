from django import forms
from .models import post, category, Comment
from django.utils.translation import gettext_lazy as _
from django.db.migrations.state import get_related_models_tuples


choices = category.objects.all().values_list('name','name')
choice_list = []

for item in choices:
   choice_list.append(item)


class PostForm(forms.ModelForm):
	class Meta:
		model = post 
		fields = ('title','author','category','body','image', 'snippet', 'status')
		widgets = {
		'title': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
		'author': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'id':'author', 'type':'hidden'}),
		'category': forms.Select(choices=choice_list,attrs={'class': 'form-control form-control-lg'}),
		'body': forms.Textarea(attrs={'class': 'form-control form-control-lg'}),
		'image': forms.FileInput(attrs={'class': 'form-control form-control-lg','accept':'image/*' }),
		'snippet': forms.Textarea(attrs={'class': 'form-control form-control-lg'}),
		'status': forms.Select(attrs={'class': 'form-control form-control-lg'}),

		}

class EditForm(forms.ModelForm):
	class Meta:
		model = post 
		fields = ('title','category','body','image', 'snippet', 'status')
		widgets = {
		'title': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
		'author': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
		'category': forms.Select(choices=choice_list, attrs={'class': 'form-control form-control-lg'}),
		'body': forms.Textarea(attrs={'class': 'form-control form-control-lg'}),
		'image': forms.FileInput(attrs={'class': 'form-control form-control-lg', 'accept':'image/*' }),
		'snippet': forms.Textarea(attrs={'class': 'form-control form-control-lg'}),
		'status': forms.Select(attrs={'class': 'form-control form-control-lg'}),


		}


class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment

		fields = ['body', 'parent']

		labels = {
			'body' : _(''),
		}

		widgets = {
			'body': forms.Textarea(attrs={'class':'form-control', 'placeholder':"Your comment", 'value':"comment_form"}),
			#'email': forms.EmailInput(),
		}


class ContactForm(forms.Form):
	name = forms.CharField(widget = forms.TextInput(attrs={'class':'form-control', 'placeholder':"Your Name"}),max_length=255)
	email = forms.EmailField(widget = forms.TextInput(attrs={'class':'form-control', 'placeholder':"Your Email"}),max_length=255)
	subject = forms.CharField(widget = forms.TextInput(attrs={'class':'form-control', 'placeholder':"Subject"}),max_length=255)
	message = forms.CharField(widget= forms.Textarea(attrs={'class':'form-control', 'placeholder':"Your message"}), max_length=255)

	class Meta:
		fields = ['name', 'email', 'subject', 'message' ]

		labels = {
			'name' : _(''),}