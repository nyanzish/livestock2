from django import forms
from .models import Item, Farmer
#DataFlair #File_Upload
class Uploadform(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
        'title',
        'price',
        'discount_price',
        'category',
        'slug',
        'description',
        'image'
        ,]


class Farmerform(forms.ModelForm):
    class Meta:
        model = Farmer
        fields = [
        'firstname',
        'lastname',
        'email',
        'farmname',
        'farmlocation',
        'phone'
        ,]