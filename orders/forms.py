from django import forms
from orders.models import Order
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from phonenumber_field.formfields import PhoneNumberField

PAYMENT_OPTIONS = [
    ('Mpesa', 'Mpesa'),
    ('Credit card', 'Credit card'),
]


class PaymentForm(forms.Form):
    payment_options = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_OPTIONS,
                                        label='Choose Your Payment Method')

    class Meta:
        model = Order
        fields = ['payment_options']

