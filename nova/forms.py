from django.utils import timezone
from datetime import timedelta
from django import forms


# Formulaire pour l'envoie de message
class ContactForm(forms.Form):
    full_name = forms.CharField(
        label="Nom Complet",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    contact = forms.CharField(
        label="Contact",
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    email = forms.EmailField(
        label="Email",
        max_length=254,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "autocomplete": "True",
            }
        ),
    )
    message = forms.CharField(
        required=True,
        max_length=255,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 8,
                "cols": 30,
            }
        ),
    )


# Formulaire pour la réservation
class ReservationForm(forms.Form):
    full_name = forms.CharField(
        label="Nom Complet",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    contact = forms.CharField(
        label="Contact",
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    email = forms.EmailField(
        label="Email",
        max_length=254,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "autocomplete": "True",
            }
        ),
    )
    datearrivee = forms.DateField(
        label="Date de arrivée",
        widget=forms.DateInput(
            format="%d %B, %Y",
            attrs={
                "class": "form-control",
                "id": "checkout_date",
                "min": str(timezone.now().date()),
                "max": str((timezone.now() + timedelta(days=365)).date()),
            },
        ),
        input_formats=["%d %B, %Y"],
    )
    datedepart = forms.DateField(
        label="Date de départ",
        widget=forms.DateInput(
            format="%d %B, %Y",
            attrs={
                "class": "form-control", 
                "id": "checkout_date",
                "min": str(timezone.now().date()),
                "max": str((timezone.now() + timedelta(days=365)).date()),
            },
        ),
        input_formats=["%d %B, %Y"],
    )
    adultes = forms.IntegerField(
        label="Adultes",
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "number",
            }
        ),
    )
    enfants = forms.IntegerField(
        label="Enfants",
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "number",
            }
        ),
    )
    message = forms.CharField(
        label="Notes",
        required=True,
        max_length=255,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 8,
                "cols": 30,
            }
        ),
    )
