from django.contrib import admin
from django.contrib import admin as django_admin

# Import de 'admin' de unfold
from unfold.admin import ModelAdmin, StackedInline

# Import dans le cadre de la modification de l'interface d'ajout des users et groups de DJANGO admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from unfold.admin import ModelAdmin

# Import pour la mise en place des filtres sur les models
from django.core.validators import EMPTY_VALUES
from django.utils.translation import gettext_lazy as _
from unfold.contrib.filters.admin import (
    FieldTextFilter,
    RangeDateFilter,
    ChoicesCheckboxFilter,
    RelatedDropdownFilter,
    BooleanRadioFilter,
    SliderNumericFilter,
)

# Import pour améliorer la gestion du texte enrichi dans l'interface d'administration Django
from unfold.contrib.forms.widgets import WysiwygWidget

# Récuperation des models
from .models import (
    reservation_chambre,
    chambre,
    reservation,
    plat,
    testimony,
    Photo,
    EmailSend,
    ServiceClient,
    NewsLetterEmail,
    ContactCompany,
    LienSocialeCompany,
    HotelInfo,
    Article,
)
from django.db import models

# unfold paginator
from unfold.paginator import InfinitePaginator

# unregister
admin.site.unregister(User)
admin.site.unregister(Group)
#
from import_export import resources
from import_export.admin import ImportExportModelAdmin, ExportActionModelAdmin
from unfold.contrib.import_export.forms import (
    ExportForm,
    ImportForm,
    SelectableFieldsExportForm,
)


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    # Forms loaded from `unfold.forms`
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass


# TODO : article pour stocker les articles du blog du restaurant
@admin.register(Article)
class ArticleAdmin(ModelAdmin):
    paginator = InfinitePaginator
    show_full_result_count = False

    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        }
    }

    list_display = ("titre", "publish", "create_date")
    prepopulated_fields = {
        "slug": ("titre",)
    }  # mis à jour automatiquement lorsque nous définissons le titre
    search_fields = ("titre",)  # Permet de rechercher par contact

    # ajout de filtrage à l’aide de l’attribut list_filter
    list_filter_submit = True  # Bouton de soumission en bas du filtre
    list_filter = [
        ("titre", FieldTextFilter),
        ("status", BooleanRadioFilter),
        "date_creation",
    ]

    @admin.display(
        ordering="status",
        description="Publier ?",
    )
    def publish(self, obj):
        if obj.status == True:
            return "OUI"
        else:
            return "NON"

    @admin.display(
        ordering="date_creation",
        description="Date Ajout",
    )
    def create_date(self, obj):
        return obj.date_creation


# TODO : HotelInfo pour stocker les infos de l'hôtel
@admin.register(HotelInfo)
class HotelInfoAdmin(ModelAdmin):
    list_display = ("name", "adresse", "Email", "create_date")
    search_fields = ("app_name",)  # Permet de rechercher par app_name

    # ajout de filtrage à l’aide de l’attribut list_filter
    list_filter_submit = True  # Bouton de soumission en bas du filtre
    list_filter = [
        ("app_name", FieldTextFilter),
    ]

    @admin.display(
        ordering="app_name",
        description="Nom",
    )
    def name(self, obj):
        return obj.app_name

    @admin.display(
        ordering="app_adresse",
        description="adresse",
    )
    def adresse(self, obj):
        return obj.app_adresse

    @admin.display(
        ordering="app_mailadresse",
        description="Email",
    )
    def Email(self, obj):
        return obj.app_mailadresse

    @admin.display(
        ordering="date_creation",
        description="Date Ajout",
    )
    def create_date(self, obj):
        return obj.date_creation

    paginator = InfinitePaginator
    show_full_result_count = False

# TODO : testimony pour stocker les témoignagnes
@admin.register(testimony)
class testimonyAdmin(ModelAdmin):
    list_display = ("name", "publish", "create_date")
    search_fields = ("nom_prenom",)  # Permet de rechercher par nom_prenom

    # ajout de filtrage à l’aide de l’attribut list_filter
    list_filter_submit = True  # Bouton de soumission en bas du filtre
    list_filter = [
        ("nom_prenom", FieldTextFilter),
        ("visible", BooleanRadioFilter),
    ]

    @admin.display(
        ordering="nom_prenom",
        description="Nom Prénom",
    )
    def name(self, obj):
        return obj.nom_prenom

    @admin.display(
        ordering="visible",
        description="Visible ?",
    )
    def publish(self, obj):
        if obj.visible == True:
            return "OUI"
        else:
            return "NON"

    @admin.display(
        ordering="date_creation",
        description="Date Ajout",
    )
    def create_date(self, obj):
        return obj.date_creation

    paginator = InfinitePaginator
    show_full_result_count = False

# TODO : LienSocialeCompany pour stocker les lien sociales de l'hôtel
@admin.register(LienSocialeCompany)
class LienSocialeCompanyAdmin(ModelAdmin):
    list_display = ("designation", "lien")
    search_fields = ("designation",)  # Permet de rechercher par designation

    # ajout de filtrage à l’aide de l’attribut list_filter
    list_filter_submit = True  # Bouton de soumission en bas du filtre
    list_filter = [
        ("designation", FieldTextFilter),
    ]
    
    paginator = InfinitePaginator
    show_full_result_count = False

# TODO : ContactCompany pour stocker les contacts de l'hôtel
@admin.register(ContactCompany)
class ContactCompanyAdmin(ModelAdmin):
    list_display = ("contact", "create_date")
    search_fields = ("contact",)  # Permet de rechercher par contact

    # ajout de filtrage à l’aide de l’attribut list_filter
    list_filter_submit = True  # Bouton de soumission en bas du filtre
    list_filter = [
        ("contact", FieldTextFilter),
    ]

    @admin.display(
        ordering="date_creation",
        description="Date Ajout",
    )
    def create_date(self, obj):
        return obj.date_creation

    paginator = InfinitePaginator
    show_full_result_count = False


# TODO : NewsLetterEmail pour stocker les emails des visiteurs pour les articles
@admin.register(NewsLetterEmail)
class NewsLetterEmailAdmin(ModelAdmin):
    list_display = ("mail", "status")
    search_fields = ("email_visteur",)  # Permet de rechercher par email

    # ajout de filtrage à l’aide de l’attribut list_filter
    list_filter_submit = True  # Bouton de soumission en bas du filtre
    list_filter = [
        ("email_visteur", FieldTextFilter),
        ("actif", BooleanRadioFilter),
    ]

    @admin.display(
        ordering="actif",
        description="Actif ?",
    )
    def status(self, obj):
        if obj.actif == True:
            return "OUI"
        else:
            return "NON"

    @admin.display(
        ordering="email_visteur",
        description="Email",
    )
    def mail(self, obj):
        return obj.email_visteur

    paginator = InfinitePaginator
    show_full_result_count = False


# TODO : Gestion des photos
@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "create_date",
    )  # Affiche ces colonnes dans la liste
    search_fields = ("titre",)  # Permet de rechercher par titre
    list_filter_submit = True
    list_filter = [
        ("date_creation", RangeDateFilter),
    ]  # ajout de filtrage à l’aide de l’attribut list_filter

    @admin.display(
        ordering="titre",
        description="Titre photo",
    )
    def title(self, obj):
        return obj.titre

    @admin.display(
        ordering="date_creation",
        description="Date Ajout",
    )
    def create_date(self, obj):
        return obj.date_creation

    paginator = InfinitePaginator
    show_full_result_count = False


# TODO : Gestion des plats
@admin.register(plat)
class platAdmin(ModelAdmin):
    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        }
    }

    list_display = ("nom", "prix", "actif", "create_date")
    search_fields = ("nom",)  # rechercher par designation

    # ajout de filtrage à l’aide de l’attribut list_filter
    list_filter_submit = True
    list_filter = [
        ("nom", FieldTextFilter),
        ("type_plat", ChoicesCheckboxFilter),
        ("status", BooleanRadioFilter),
        ("date_creation", RangeDateFilter),
    ]

    @admin.display(
        ordering="status",
        description="Visible ?",
    )
    def actif(self, obj):
        if obj.status == True:
            return "OUI"
        else:
            return "NON"

    @admin.display(
        ordering="date_creation",
        description="Date Ajout",
    )
    def create_date(self, obj):
        return obj.date_creation

    paginator = InfinitePaginator
    show_full_result_count = False

# TODO : Gestion des agents du service clients
@admin.register(ServiceClient)
class ServiceclientAdmin(ModelAdmin):
    list_display = ("nom_complet", "pin", "status", "create_date")
    search_fields = (
        "nom_complet", 
    )  # Permet de rechercher par nom_complet  

    # ajout de filtrage à l’aide de l’attribut list_filter
    list_filter_submit = True  # Bouton de soumission en bas du filtre
    list_filter = [
        ("nom_complet", FieldTextFilter),
        ("pinned", BooleanRadioFilter),
        ("actif", BooleanRadioFilter),
        ("date_creation", RangeDateFilter),
    ]

    @admin.display(
        ordering="pinned",
        description="Épingler ?",
    )
    def pin(self, obj):
        if obj.pinned == True:
            return "OUI"
        else:
            return "NON"

    @admin.display(
        ordering="actif",
        description="Actif ?",
    )
    def status(self, obj):
        if obj.actif == True:
            return "OUI"
        else:
            return "NON"

    @admin.display(
        ordering="date_creation",
        description="Date Ajout",
    )
    def create_date(self, obj):
        return obj.date_creation

    paginator = InfinitePaginator
    show_full_result_count = False


# TODO : EmailSend pour stocker les emails des visiteurs et en même temps envoyer aux agents du service clients
@admin.register(EmailSend)
class EmailSendAdmin(ModelAdmin):
    list_display = ("nom", "contact", "email", "create_date")
    search_fields = ("email",)  # Permet de rechercher par email

    # ajout de filtrage à l’aide de l’attribut list_filter
    list_filter_submit = True  # Bouton de soumission en bas du filtre
    list_filter = [
        ("email", FieldTextFilter),
    ]

    @admin.display(
        ordering="date_creation",
        description="Date Ajout",
    )
    def create_date(self, obj):
        return obj.date_creation

    paginator = InfinitePaginator
    show_full_result_count = False


# TODO : Gestion des chambres & configuration ramètrages du filtres
class PriceNumericFilter(SliderNumericFilter):
    MAX_DECIMALS = 2
    STEP = 10


@admin.register(chambre)
class chambreAdmin(ModelAdmin):
    list_display = ("room", "price", "nb_lit", "pin", "status", "create_date") 

    # ajout de filtrage à l’aide de l’attribut list_filter
    list_filter_submit = True  # Bouton de soumission en bas du filtre
    list_filter = [
        ("prix_nuit", PriceNumericFilter),
        ("type_chambre", ChoicesCheckboxFilter),
        ("libre", BooleanRadioFilter),
        ("is_best", BooleanRadioFilter),
        ("date_creation", RangeDateFilter),
    ]

    @admin.display(
        ordering="prix_nuit",
        description="Prix par nuit",
    )
    def price(self, obj):
        return obj.prix_nuit

    @admin.display(
        ordering="type_chambre",
        description="Type chambre",
    )
    def type_room(self, obj):
        return obj.type_chambre

    @admin.display(
        ordering="nombre_lit",
        description="Nombre lit",
    )
    def nb_lit(self, obj):
        return obj.nombre_lit

    @admin.display(
        ordering="libre",
        description="Libre ?",
    )
    def pin(self, obj):
        if obj.libre == True:
            return "OUI"
        else:
            return "NON"

    @admin.display(
        ordering="is_best",
        description="Meilleur offre ?",
    )
    def status(self, obj):
        if obj.is_best == True:
            return "OUI"
        else:
            return "NON"

    @admin.display(
        ordering="date_creation",
        description="Date Ajout",
    )
    def create_date(self, obj):
        return obj.date_creation

    @admin.display(
        ordering="type_chambre",
        description="Chambre",
    )
    def room(self, obj):
        if obj.type_chambre == "S":
            return "Simple"
        elif obj.type_chambre == "F":
            return "Familiale"
        elif obj.type_chambre == "P":
            return "Présidentielle"

    paginator = InfinitePaginator
    show_full_result_count = False


# TODO : Gestion des réservation directement sur les chambres
@admin.register(reservation_chambre)
class reservation_chambreAdmin(ModelAdmin): 
    list_display = (
        "room",
        "name",
        "contact",
        "email",
        "date_arrive",
        "date_depart",
        "nb_adult",
        "nb_kids",
        "status",
        "create_date",
    )
    search_fields = (
        "nom",
        "email",
    )  # Permet de rechercher par nom et email

    # ajout de filtrage à l’aide de l’attribut list_filter
    list_filter_submit = True  # Bouton de soumission en bas du filtre
    list_filter = [
        ("is_finish", BooleanRadioFilter),
        ("date_creation", RangeDateFilter),
    ]

    @admin.display(
        ordering="nom",
        description="Nom-Prénom Client",
    )
    def name(self, obj):
        return obj.nom

    @admin.display(
        ordering="date_arrivee",
        description="Arrivée",
    )
    def date_arrive(self, obj):
        return obj.date_arrivee

    @admin.display(
        ordering="date_depart",
        description="Départ",
    )
    def date_depart(self, obj):
        return obj.date_depart

    @admin.display(
        ordering="nombre_adulte",
        description="Nombre adulte",
    )
    def nb_adult(self, obj):
        return obj.nombre_adulte

    @admin.display(
        ordering="nombre_enfant",
        description="Nombre enfant",
    )
    def nb_kids(self, obj):
        return obj.nombre_enfant

    @admin.display(
        ordering="date_creation",
        description="Date Ajout",
    )
    def create_date(self, obj):
        return obj.date_creation

    @admin.display(
        ordering="is_finish",
        description="Terminer ?",
    )
    def status(self, obj):
        if obj.is_finish == True:
            return "OUI"
        else:
            return "NON"

    @admin.display(
        ordering="id_chambre",
        description="Chambre",
    )
    def room(self, obj): 
        if obj.id_chambre.type_chambre == "S" :
            return "Simple"
        elif obj.id_chambre.type_chambre == "F" :
            return "Familiale"
        elif obj.id_chambre.type_chambre == "P" :
            return "Présidentielle"

    paginator = InfinitePaginator
    show_full_result_count = False


# TODO : Gestion des réservation (indirect) :)
@admin.register(reservation)
class reservationAdmin(ModelAdmin):
    list_display = (
        "name",
        "contact",
        "email",
        "date_arrive",
        "date_depart",
        "nb_adult",
        "nb_kids",
        "status",
        "create_date",
    )
    search_fields = (
        "nom",
        "email",
    )  # Permet de rechercher par nom et email

    # ajout de filtrage à l’aide de l’attribut list_filter
    list_filter_submit = True  # Bouton de soumission en bas du filtre
    list_filter = [
        ("is_confirm", BooleanRadioFilter),
        ("date_creation", RangeDateFilter),
    ]

    @admin.display(
        ordering="nom",
        description="Nom-Prénom Client",
    )
    def name(self, obj):
        return obj.nom

    @admin.display(
        ordering="date_arrivee",
        description="Arrivée",
    )
    def date_arrive(self, obj):
        return obj.date_arrivee

    @admin.display(
        ordering="date_depart",
        description="Départ",
    )
    def date_depart(self, obj):
        return obj.date_depart

    @admin.display(
        ordering="nombre_adulte",
        description="Nombre adulte",
    )
    def nb_adult(self, obj):
        return obj.nombre_adulte

    @admin.display(
        ordering="nombre_enfant",
        description="Nombre enfant",
    )
    def nb_kids(self, obj):
        return obj.nombre_enfant

    @admin.display(
        ordering="date_creation",
        description="Date Ajout",
    )
    def create_date(self, obj):
        return obj.date_creation

    @admin.display(
        ordering="is_confirm",
        description="Confirmer ?",
    )
    def status(self, obj):
        if obj.is_confirm == True:
            return "OUI"
        else:
            return "NON"

    paginator = InfinitePaginator
    show_full_result_count = False
