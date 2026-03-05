from django import forms

from .models import Customer


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('first_name', 'last_name', 'email', 'company')
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'First name',
                'class': 'w-full px-4 py-2 border rounded-lg',
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Last name',
                'class': 'w-full px-4 py-2 border rounded-lg',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Email (optional)',
                'class': 'w-full px-4 py-2 border rounded-lg',
            }),
            'company': forms.TextInput(attrs={
                'placeholder': 'Company (optional)',
                'class': 'w-full px-4 py-2 border rounded-lg',
            }),
        }


class CSVImportForm(forms.Form):
    csv_file = forms.FileField(
        label='CSV File',
        widget=forms.FileInput(attrs={
            'accept': '.csv',
            'class': 'w-full px-4 py-2 border rounded-lg',
        }),
    )
