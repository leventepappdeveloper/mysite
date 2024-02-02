# import the standard Django Forms
# from built-in library
from django import forms


# creating a form
class InputForm(forms.Form):
    stock_symbol = forms.CharField(max_length=200)
    start_date = forms.CharField(max_length=200)
    end_date = forms.CharField(max_length=200)
    days_to_expiry = forms.CharField(max_length=200)
    delta = forms.CharField(max_length=200)
    margin_requirement_rate = forms.CharField(max_length=200)
