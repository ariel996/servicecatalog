from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from bootstrap_datepicker_plus import DatePickerInput
from annonces.models import *
from django import forms

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'

class AnnonceForm(ModelForm):
    class Meta:
        model = Annonces
        fields = '__all__'

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletters
        fields = ['email_address', 'subscribe']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = '__all__'
        widgets = {
            'product_name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'product_description': forms.Textarea(
                attrs={
                    'class': 'form-control'
                }
            )
        }

class CatalogueForm(forms.ModelForm):
    class Meta:
        model = Catalogue
        fields = '__all__'

class MessageForm(forms.ModelForm):
    class Meta:
        model = Messages
        fields = '__all__'

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = '__all__'

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contacts
        fields = '__all__'

class ProductImage(forms.ModelForm):
    class Meta:
        model = Product_images
        fields = '__all__'

class AnnonceImage(forms.ModelForm):
    class Meta:
        model = Annonce_images
        fields = '__all__'

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Services
        fields = '__all__'

class Gallery(forms.ModelForm):
    class Meta:
        model = Galleries
        fields = '__all__'