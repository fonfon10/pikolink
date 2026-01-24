from django import forms
from .models import Customer, Link


class CustomerCreateForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["first_name", "last_name", "email", "company_name", "comments"]


class LinkCreateForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = ["destination_url", "campaign_name", "notes", "customer"]

