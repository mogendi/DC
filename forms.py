from django import forms
from django.contrib.auth.models import User
from .models import CustomUser, Post, AvailClasses, Resources, Assignments, AssignmentsHandedIn

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['type_field', 'classes', 'profile_pic']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text']
        widgets = {
            'title': forms.TextInput(attrs={"class": "textinputclass"}),
        }


class ClassForm(forms.ModelForm):
    class Meta:
        model = AvailClasses
        fields = ['className']
        widgets = {
            'className': forms.TextInput(attrs={"class": "textinputclass"}),
        }


class ResourceForm(forms.ModelForm):
    """Form definition for File."""
    class Meta:
        """Meta definition for Fileform."""

        model = Resources
        fields = ['file', 'description']
        widgets = {
            'file': forms.FileInput(attrs={"class": "form-control input"}),
        }


class AssignmentForm(forms.ModelForm):

    class Meta:
        model = Assignments
        fields = ['title', 'due_date']
        widgets = {
            'due_date': forms.DateInput(format='%d/%m/%Y'),
        }


class HandInForm(forms.ModelForm):

    class Meta:
        model = AssignmentsHandedIn
        fields = ['assignment']
