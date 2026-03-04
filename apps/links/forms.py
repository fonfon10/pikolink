from django import forms

from .models import Link


class LinkCreateForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = ('original_url', 'title')
        widgets = {
            'original_url': forms.URLInput(attrs={
                'placeholder': 'https://example.com/your-long-url',
                'class': 'w-full px-4 py-2 border rounded-lg',
            }),
            'title': forms.TextInput(attrs={
                'placeholder': 'Optional title',
                'class': 'w-full px-4 py-2 border rounded-lg',
            }),
        }
