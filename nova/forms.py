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

    def clean(self):
        cleaned_data = super().clean()

        # Validation du nom
        full_name = self.cleaned_data.get("full_name")
        if full_name and len(full_name) > 100:
            raise forms.ValidationError(
                "Veuillez nous contacter via un autre moyen, le nom ne peut pas dépasser 100 caractères."
            )

        # Validation du contact
        contact = self.cleaned_data.get("contact")
        if contact and len(contact) > 50:
            raise forms.ValidationError(
                "Le contact est trop long (maximum 50 caractères)."
            )

        # Validation de l'email
        email = self.cleaned_data.get("email")
        if email and len(email) > 254:
            raise forms.ValidationError(
                "L'adresse e-mail est trop longue (maximum 254 caractères)."
            )

        # Validation du message
        message = self.cleaned_data.get("message")
        if message and len(message) > 255:
            raise forms.ValidationError(
                "Le message a une longueur excessive (maximum 254 caractères)."
            )

        return cleaned_data


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

    def clean(self):
        cleaned_data = super().clean()

        # Validation du nom
        full_name = self.cleaned_data.get("full_name")
        if full_name and len(full_name) > 100:
            raise forms.ValidationError(
                "Veuillez nous contacter via un autre moyen, le nom ne peut pas dépasser 100 caractères."
            )

        # Validation du contact
        contact = self.cleaned_data.get("contact")
        if contact and len(contact) > 50:
            raise forms.ValidationError(
                "Le contact est trop long (maximum 50 caractères)."
            )

        # Validation de l'email
        email = self.cleaned_data.get("email")
        if email and len(email) > 254:
            raise forms.ValidationError(
                "L'adresse e-mail est trop longue (maximum 254 caractères)."
            )

        # Validation du message
        message = self.cleaned_data.get("message")
        if message and len(message) > 255:
            raise forms.ValidationError(
                "Le message a une longueur excessive (maximum 254 caractères)."
            )

        # Validation de la date d'arrivée et de la date de départ
        date_arrivee = self.cleaned_data.get("datearrivee")
        date_depart = self.cleaned_data.get("datedepart")
        if date_arrivee and date_depart:
            if date_arrivee > date_depart:
                msg = "La date d'arrivée ne peut être supérieur à la date de départ"
                self.add_error("datearrivee", msg)
            if date_depart < date_arrivee:
                msg = "La date de départ ne peut être inférieur à la date arrivée"
                self.add_error("datedepart", msg)

        # Validation du nombre d'adultes
        nombre_adulte = self.cleaned_data.get("adultes")
        if nombre_adulte and nombre_adulte < 0: 
            msg = "Le nombre d'adultes ne peut être une valeur négative !!!"
            self.add_error("adultes", msg)

        # Validation du nombre d'enfants
        nombre_enfant = self.cleaned_data.get("enfants")
        if nombre_enfant and nombre_enfant < 0: 
            msg = "Le nombre d'enfants ne peut être une valeur négative !!!"
            self.add_error("enfants", msg)

        return cleaned_data
