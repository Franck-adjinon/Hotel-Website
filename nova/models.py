from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

#
import os
from dotenv import load_dotenv


# TODO : article pour stocker les articles
class Article(models.Model):
    id_article = models.AutoField(primary_key=True)
    status = models.BooleanField("Publier ?", default=True)
    titre = models.CharField("Titre de l'article", max_length=150, unique=True)
    slug = models.SlugField(default="", null=False, max_length=150)
    lead = models.CharField("lead text", max_length=150)
    content = models.TextField("Contenu principal")
    cover = models.ImageField("Image de couverture", upload_to="Article_cover_image/")
    image = models.ImageField("Image principal", upload_to="Article_main_image/")
    cover_alt_text = models.CharField(
        "Texte alternatif pour accessibilité de l'image de couverture", max_length=125
    )
    image_alt_text = models.CharField(
        "Texte alternatif pour accessibilité de l'image principal", max_length=125
    )
    date_creation = models.DateTimeField("Date Création", auto_now_add=True)

    def save(self, *args, **kwargs):
        # Compression de l'image de couverture
        if self.cover:
            try:
                img = Image.open(self.cover)
                img = img.convert("RGB")  # Assurer compatibilité
                img_io = BytesIO()

                # Toujours compresser l'image
                img.save(img_io, format="WEBP", quality=80)  # Ajuster la qualité 80

                # Remplacer l'image originale par la version compressée
                new_image_name = f"{self.cover.name.split('.')[0]}_compressed.webp"
                self.cover = ContentFile(img_io.getvalue(), new_image_name)
            except Exception as e:
                raise ValueError(
                    f"Erreur lors du traitement de l'image de couverture : {e}"
                )

        # Compression de l'image principal
        if self.image:
            try:
                img = Image.open(self.image)
                img = img.convert("RGB")  # Assurer compatibilité
                img_io = BytesIO()

                # Toujours compresser l'image
                img.save(img_io, format="WEBP", quality=80)  # Ajuster la qualité 80

                # Remplacer l'image originale par la version compressée
                new_image_name = f"{self.image.name.split('.')[0]}_compressed.webp"
                self.image = ContentFile(img_io.getvalue(), new_image_name)
            except Exception as e:
                raise ValueError(
                    f"Erreur lors du traitement de l'image principal : {e}"
                )

        """Envoie un email à tout les abonner de la newsletter"""
        from .task import send_email_abonne 

        is_new = self._state.adding

        super().save(*args, **kwargs)

        if is_new:
            sujet = "Nouvel article"
            mail = os.getenv("EMAIL_HOST_USER")
            titre = self.titre
            texte = self.content
            send_email_abonne(
                sujet=sujet, from_client=mail, titre_article=titre, contenu=texte
            )

    def __str__(self):
        return f"{self.titre} {self.date_creation}"


# TODO : HotelInfo pour stocker les informations de l'hôtel
class HotelInfo(models.Model):
    id_info = models.AutoField(primary_key=True)
    app_name = models.CharField("Nom Hôtel", max_length=50)
    app_adresse = models.CharField("Adresse Hôtel", max_length=50)
    app_mailadresse = models.EmailField("Email Hôtel", max_length=254)
    date_creation = models.DateTimeField("Date Création", auto_now_add=True)

    def __str__(self):
        return f"{self.app_name} {self.app_adresse}"


# TODO : LienSocialeCompany pour stocker les liens sociales de l'hôtel
class LienSocialeCompany(models.Model):
    id_lien = models.AutoField(primary_key=True)
    designation = models.CharField("Nom de la Plateforme", max_length=50, unique=True)
    lien = models.CharField("lien vers le compte", max_length=255)

    def __str__(self):
        return self.lien


# TODO : ContactCompany pour stocker les contacts de l'hôtel
class ContactCompany(models.Model):
    id_contact = models.AutoField(primary_key=True)
    contact = models.CharField("Contact", max_length=50, unique=True)
    date_creation = models.DateTimeField("Date Création", auto_now_add=True)

    def __str__(self):
        return f"{self.contact}"


# TODO : newsletter_email pour stocker les emails donner par les visiteurs du site souhaitant recevoir des emails lors de nouvelles publication sur le blog
class NewsLetterEmail(models.Model):
    id_new = models.AutoField(primary_key=True)
    email_visteur = models.EmailField("Email visiteur", max_length=254, unique=True)
    actif = models.BooleanField("actif ?", default=True)

    def __str__(self):
        return f"{self.email_visteur}"


# TODO : ServiceClient pour stocker les infos des agents qui prendront les message des clients
class ServiceClient(models.Model):
    id_agent = models.AutoField(primary_key=True)
    image = models.ImageField("Image principal", upload_to="Service_Client_image/")
    image_alt_text = models.CharField(
        "Texte alternatif pour accessibilité de l'image", max_length=125
    )
    nom_complet = models.CharField("Nom Complet", max_length=100, unique=True)
    email = models.EmailField('Email', max_length=254, default="johndoe@gmail.com")
    role = models.CharField("Rôle", max_length=50, default="Agent")
    description = models.CharField("Description", max_length=255)
    pinned = models.BooleanField("Épingler ?", default=False)
    actif = models.BooleanField("Agent actif ?", default=True)
    date_creation = models.DateTimeField("Date Création", auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.image:
            try:
                img = Image.open(self.image)
                img = img.convert("RGB")  # Assurer compatibilité
                img_io = BytesIO()

                # Toujours compresser l'image
                img.save(img_io, format="WEBP", quality=80)  # Ajuster la qualité 80

                # Remplacer l'image originale par la version compressée
                new_image_name = f"{self.image.name.split('.')[0]}_compressed.webp"
                self.image = ContentFile(img_io.getvalue(), new_image_name)
            except Exception as e:
                raise ValueError(f"Erreur lors du traitement de l'image : {e}")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nom_complet}"


# TODO : EmailSend pour stocker les mails envoyer au agents du service clients par les clients
class EmailSend(models.Model):
    id_message = models.AutoField(primary_key=True)
    nom = models.CharField("Client", max_length=100)
    contact = models.CharField("Contact", max_length=50)
    email = models.EmailField("Email Client", max_length=254)
    message = models.CharField("Message du Client", max_length=255)
    date_creation = models.DateTimeField("Date Création", auto_now_add=True)

    def __str__(self):
        return f"{self.nom} {self.email}"


# TODO : model pour la gestion des photos
class Photo(models.Model):
    id_photo = models.AutoField(primary_key=True)
    titre = models.CharField("Titre", max_length=255)
    image = models.ImageField("Image", upload_to="photos/")
    date_creation = models.DateTimeField("Date création", auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.image:
            try:
                img = Image.open(self.image)
                img = img.convert("RGB")  # Assurer compatibilité
                img_io = BytesIO()

                # Toujours compresser l'image
                img.save(img_io, format="WEBP", quality=80)  # Ajuster la qualité 80%

                # Remplacer l'image originale par la version compressée
                new_image_name = f"{self.image.name.split('.')[0]}_compressed.webp"
                self.image = ContentFile(img_io.getvalue(), new_image_name)
            except Exception as e:
                raise ValueError(f"Erreur lors du traitement de l'image : {e}")

        super().save(*args, **kwargs)

    def __str__(self):
        return self.titre


# TODO:model pour la gestion des témoignages
class testimony(models.Model):
    id_testimony = models.AutoField(primary_key=True)
    image = models.ImageField("Photo Client", upload_to="testimony_photos/")
    nom_prenom = models.CharField("Nom-Prénom Client", max_length=100)
    temoignage = models.CharField("Témoignage", max_length=250)
    visible = models.BooleanField("Visible ?", default=False)
    date_creation = models.DateTimeField("Date Création", auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.image:
            try:
                img = Image.open(self.image)
                img = img.convert("RGB")  # Assurer compatibilité
                img_io = BytesIO()

                # Toujours compresser l'image
                img.save(img_io, format="WEBP", quality=80)  # Ajuster la qualité 80

                # Remplacer l'image originale par la version compressée
                new_image_name = f"{self.image.name.split('.')[0]}_compressed.webp"
                self.image = ContentFile(img_io.getvalue(), new_image_name)
            except Exception as e:
                raise ValueError(f"Erreur lors du traitement de l'image : {e}")

        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom_prenom


# TODO :  Pour la gestion des réservations
class reservation(models.Model):
    id_reservation = models.AutoField(primary_key=True)
    nom = models.CharField("Nom-Prénom Client", max_length=100)
    contact = models.CharField("Contact Client", max_length=50)
    email = models.EmailField("Email Client", max_length=254)
    date_arrivee = models.DateField("Date Arrivée")
    date_depart = models.DateField("Date Départ")
    nombre_adulte = models.IntegerField("Nombre d'adultes")
    nombre_enfant = models.IntegerField("Nombre d'enfants")
    message = models.CharField("Message Client", max_length=255)
    is_confirm = models.BooleanField("Confirmer ?", default=False)
    date_creation = models.DateTimeField("Date Création", auto_now_add=True)


# TODO : Pour la gestion des plats
class plat(models.Model):
    id_plat = models.AutoField(primary_key=True)
    image = models.ImageField("Image plat", upload_to="Plats_image/")
    nom = models.CharField("Nom Plat", max_length=50, unique=True)
    prix = models.DecimalField("Prix plat", max_digits=10, decimal_places=2)
    type_pl = {
        "P": "Plats Principale",
        "D": "Desserts",
        "B": "Boissons",
    }
    type_plat = models.CharField(max_length=1, choices=type_pl, default="P")
    description = models.CharField("Description", max_length=255)
    status = models.BooleanField("Visible ?", default=True)
    date_creation = models.DateTimeField("Date Création", auto_now_add=True)
    date_update = models.DateTimeField("Date Mise à jour", default=timezone.now)

    def __str__(self):
        return f"{self.nom}"


# TODO : Pour la gestion des chambre
class chambre(models.Model):
    id_chambre = models.AutoField(primary_key=True)
    numero_chambre = models.CharField("Numéro de chambre", default="000")
    prix_nuit = models.DecimalField("Prix chambre", max_digits=10, decimal_places=2)
    image = models.ImageField("Image chambre", upload_to="Chambre_image/")
    type_ch = {
        "S": "Chambre Simple",
        "F": "Chambre familiale",
        "P": "Chambre Présidentielle",
    }
    type_chambre = models.CharField(max_length=1, choices=type_ch, default="S")
    description = models.CharField("Description", max_length=255)
    nombre_lit = models.IntegerField("Nombre de lit")
    libre = models.BooleanField("Libre ?", default=True)
    is_best = models.BooleanField("Meilleur offre ?", default=False)
    date_creation = models.DateTimeField("Date Création", auto_now_add=True)
    date_update = models.DateTimeField("Date Mise à jour", default=timezone.now)

    def __str__(self):
        return f"{self.prix_nuit}"


# TODO :  Pour la gestion des réservations associer au chambre
class reservation_chambre(models.Model):
    id_reservation = models.AutoField(primary_key=True)
    nom = models.CharField("Nom-Prénom Client", max_length=100)
    contact = models.CharField("Contact Client", max_length=50)
    email = models.EmailField("Email Client", max_length=254)
    date_arrivee = models.DateField("Date Arrivée")
    date_depart = models.DateField("Date Départ")
    nombre_adulte = models.IntegerField("Nombre d'adultes")
    nombre_enfant = models.IntegerField("Nombre d'enfants")
    message = models.CharField("Message Client", max_length=255)
    id_chambre = models.ForeignKey(chambre, on_delete=models.CASCADE)
    is_finish = models.BooleanField('Terminer ?', default=False)
    date_creation = models.DateTimeField("Date Création", auto_now_add=True)
