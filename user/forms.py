from django.forms import ModelForm
from core.models import User

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = (
            'permission',
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
            'phone_number'
        )