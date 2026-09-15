from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, ServiceBooking, Vehicle


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "password1", "password2")


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ("make", "model", "registration_number", "year", "color", "mileage")
        widgets = {"year": forms.NumberInput(attrs={"min": 1900}), "mileage": forms.NumberInput(attrs={"min": 0})}


class BookingForm(forms.ModelForm):
    class Meta:
        model = ServiceBooking
        fields = ("vehicle", "service_type", "preferred_date", "preferred_time", "notes")
        widgets = {
            "preferred_date": forms.DateInput(attrs={"type": "date"}),
            "preferred_time": forms.TimeInput(attrs={"type": "time"}),
            "notes": forms.Textarea(attrs={"rows": 4, "placeholder": "Tell us about any concerns..."}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["vehicle"].queryset = Vehicle.objects.filter(owner=user) if user else Vehicle.objects.none()


class ProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()

    class Meta:
        model = Profile
        fields = ("phone", "address")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["username"].initial = self.instance.user.username
            self.fields["first_name"].initial = self.instance.user.first_name
            self.fields["last_name"].initial = self.instance.user.last_name
            self.fields["email"].initial = self.instance.user.email

    def clean_username(self):
        username = self.cleaned_data["username"]
        existing_user = User.objects.filter(username__iexact=username).exclude(pk=self.instance.user.pk)
        if existing_user.exists():
            raise forms.ValidationError("That username is already in use. Please choose another one.")
        return username

    def save(self, commit=True):
        profile = super().save(commit=False)
        profile.user.username = self.cleaned_data["username"]
        profile.user.first_name = self.cleaned_data["first_name"]
        profile.user.last_name = self.cleaned_data["last_name"]
        profile.user.email = self.cleaned_data["email"]
        if commit:
            profile.user.save()
            profile.save()
        return profile
