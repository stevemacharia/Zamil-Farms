from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile
from django.forms import ImageField

COUNTIES = (
    ('', 'Choose...'),
    ('Nairobi 047', 'Nairobi'),
    ('Mombasa 001', 'Mombasa'),
    ('Kwale002','Kwale'),
    ('Kilifi 003', 'Kilifi'),
    ('Tana River 004', 'Tana River'),
    ('Lamu 005', 'Lamu'),
    ('Taita/Taveta 006', 'Taita/Taveta'),
    ('Garissa 007', 'Garissa'),
    ('Wajir 008', 'Wajir'),
    ('Mandera 009', 'Mandera'),
    ('Marsabit 010', 'Marsabit'),
    ('Isiolo 011', 'Isiolo'),
    ('Meru 012', 'Meru'),
    ('Tharaka-Nithi 013', 'Tharaka-Nithi'),
    ('Embu 014', 'Embu'),
    ('Kitui 015', 'Kitui'),
    ('Machakos 015', 'Machakos'),
    ('Makueni 016', 'Makueni'),
    ('Nyandarua 017', 'Nyandarua'),
    ('Nyeri 018', 'Nyeri'),
    ('Kirinyaga 019', 'Kirinyaga'),
    ('Muranga 020', 'Muranga'),
    ('Kiambu 021', 'Kiambu'),
    ('Turkana 022', 'Turkana'),
    ('West Pokot 023', 'West Pokot'),
    ('Samburu 024', 'Samburu'),
    ('Trans Nzoia 025', 'Trans Nzoia'),
    ('Uasin Gishu 026', 'Uasin Gishu'),
    ('Elgeyo/Marakwet 027', 'Elgeyo/Marakwet'),
    ('Nandi 028', 'Nandi'),
    ('Baringo 029', 'Baringo'),
    ('Laikipia 030', 'Laikipia'),
    ('Nakuru 031', 'Nakuru'),
    ('Narok 032', 'Narok'),
    ('Kajiado 033', 'Kajiado'),
    ('Kericho 034', 'Kericho'),
    ('Bomet 035', 'Bomet'),
    ('Kakamega 036', 'Kakamega'),
    ('Vihiga 038', 'Vihiga'),
    ('Bungoma 039', 'Bungoma'),
    ('Busia 040', 'Busia'),
    ('Siaya 041', 'Siaya'),
    ('Kisumu 042', 'Kisumu'),
    ('Homa Bay 043', 'Homa Bay'),
    ('Migori 044', 'Migori'),
    ('Kisii 045', 'Kisii'),
    ('Nyamira 046', 'Nyamira')
)


# Create your forms here.
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(max_length=20)
    email = forms.EmailField()

    # specify the name of model to use
    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    # phone_number = PhoneNumberField(region="KE")
    phone_number = forms.CharField(required=False)
    address_county = forms.ChoiceField(choices=COUNTIES, label='County', required=False)
    address_city_town = forms.CharField(label='City/Town', required=False)
    profile_pic = ImageField()

    class Meta:
        model = UserProfile
        fields = ['profile_pic', 'phone_number', 'address_county', 'address_city_town']


