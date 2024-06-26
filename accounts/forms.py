
from .models import User , UserProfile
from django import forms
from .validators import allow_only_images_validator
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['first_name', 'last_name' , 'username' ,'email' , 'phone_number', 'password']
    def clean(self):
        cleaned_data = super(UserForm , self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                'Password and Confirm Password does not match!'
            )


class UserProfileForm(forms.ModelForm):
    profile_picture = forms.FileField(widget=forms.FileInput(attrs={'class' : 'btn btn-info'}) , validators=[allow_only_images_validator])
    cover_photo = forms.FileField(widget=forms.FileInput(attrs={'class' : 'btn btn-info'}), validators=[allow_only_images_validator])
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder' :'Start Typing...','required':'required','readonly':'readonly'}))
    # latitude = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    # longitude = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    class Meta:
        model = UserProfile
        fields = ['profile_picture' ,'cover_photo' ,'address' ,'country' ,'state','city','pincode','latitude','longitude']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields.keys():
            if field_name == 'latitude' or field_name == 'longitude' or field_name == 'address':
                self.fields[field_name].widget.attrs['readonly'] = True



class UserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name' , 'last_name' , 'phone_number']


