from django import forms
from .models import Ohb_items,Items_Counts


class items_CountsForm(forms.ModelForm):


    class Meta:
        model = Items_Counts
        fields=('item_create','item_los','item','date')
        #fields=('item_create','date')


        widgets = {
            # 'summary': forms.TextInput(attrs={
                # 'class': 'form-control',
            # }),
            'date': forms.HiddenInput,
            'item': forms.HiddenInput,
        }
        
class NoForm(forms.ModelForm):
    class Meta:
        model=Ohb_items
        fields =('item_no',)

        