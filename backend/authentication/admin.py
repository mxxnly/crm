from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('username', 'email')

    def clean_password2(self):
        p1 = self.cleaned_data.get('password1')
        p2 = self.cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords don't match")
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class CustomUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'is_active', 'is_staff')

class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = ('username', 'email', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile)
