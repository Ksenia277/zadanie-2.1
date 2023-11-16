from django.contrib.auth.models import User
from django import forms


class ConfirmField(forms.Field):
    def validate(self, value):
        super(ConfirmField, self).validate(value)
        if value==None:
            raise forms.ValidationError(
                "Ошибка: "
                "Поставьте галочку о согласии"
            )


class UserForm(forms.ModelForm):
    username = forms.CharField()
    first_name = forms.CharField()
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())
    confirm = ConfirmField(required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email','password']

    def clean_password2(self):
        if self.cleaned_data.get("password") != self.cleaned_data.get("password2"):
            raise forms.ValidationError(
                "Ошибка: "
                "введеные пароли не совпадают"
            )
