from django import forms
from .models import Vendor , OpeningHours
from accounts.validators import allow_only_images_validator
class VendorForm(forms.ModelForm):
    vendor_licence = forms.FileField(widget=forms.FileInput(attrs={'class' : 'btn btn-info'}) , validators=[allow_only_images_validator])
    class Meta:
        model = Vendor
        fields = ['vendor_name' , 'vendor_licence']



class OpeningHoursForm(forms.ModelForm):
    class Meta:
        model = OpeningHours
        fields = ('day' , 'from_hours' , 'to_hours' , 'is_closed')