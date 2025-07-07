from django import forms
from authentication.models import CustomUser  
from django.core.exceptions import ValidationError

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}), label="password")
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}), label="confirm password")

    class Meta:
        model = CustomUser   
        fields = ['username', 'email']  

        labels = {
            'username': 'username',
            'email': 'email',
        }

    

    def clean_password_confirm(self):
        pwd = self.cleaned_data.get("password")
        pwd_c = self.cleaned_data.get("password_confirm")
        if pwd and pwd_c and pwd != pwd_c:
            raise ValidationError("Паролі не співпадають.")
        return pwd_c