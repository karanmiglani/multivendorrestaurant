from django import forms
from .models import Category , Product


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name' , 'description']