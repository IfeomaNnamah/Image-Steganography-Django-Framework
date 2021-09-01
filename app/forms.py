from django import forms
from .models import ShareImage, verifykey
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class CreateUserForm(UserCreationForm):
	def __init__(self, *args, **kwargs):
		super(CreateUserForm, self).__init__(*args, **kwargs)
		for name in self.fields.keys():
			self.fields[name].widget.attrs.update({'class': 'form-control',})

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']


class UploadFileForms(forms.Form):
	img = forms.FileField()


class DateInput(forms.DateInput):
	input_type = 'date'


class ShareStegoImageForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(ShareStegoImageForm, self).__init__(*args, **kwargs)
		for name in self.fields.keys():
			self.fields[name].widget.attrs.update({'class': 'form-control',})

	class Meta:
		model = ShareImage
		fields = "__all__"
		widgets = {'sent_date': DateInput(), }

