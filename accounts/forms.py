from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class PublicSignupForm(UserCreationForm):
    organization_name = forms.CharField(max_length=200)
    email = forms.EmailField()

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop("username", None)

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError("User already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        email = self.cleaned_data["email"].strip().lower()
        user.username = email
        user.email = email
        if commit:
            user.save()
        return user


class InviteSignupForm(UserCreationForm):
    email = forms.EmailField()

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email", "password1", "password2")

    def __init__(self, *args, invitation=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.invitation = invitation
        self.fields.pop("username", None)
        if invitation:
            self.fields["email"].initial = invitation.email
            self.fields["email"].disabled = True

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if self.invitation and email != self.invitation.email.lower():
            raise forms.ValidationError("Email does not match invitation.")
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError("User already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        email = self.cleaned_data["email"].strip().lower()
        user.username = email
        user.email = email
        if commit:
            user.save()
        return user
