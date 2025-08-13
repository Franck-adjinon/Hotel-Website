from pyexpat.errors import messages 
from .models import ( 
    chambre,
    reservation,
    plat,
    testimony,
    Photo, 
    ServiceClient,
    NewsLetterEmail,
    ContactCompany,
    LienSocialeCompany,
    HotelInfo,
    Article,
)
from .task import send_email_in_background_template
from django.http import BadHeaderError, HttpResponse, Http404, HttpResponseRedirect
from django.template import loader 
from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator

# *Les formulaires
from .forms import ContactForm, ReservationForm

# *gestion des logs
import logging 
# Obtenir un logger nommé selon le nom du module courant
logger = logging.getLogger(__name__)


# TODO : Affichage de la page d'accueil
def index(request):
    template = loader.get_template("index.html")

    # initialisation par défaut
    rooms = []
    pictures = []
    plats = []
    desserts = []
    boissons = []
    Articles = []
    temoignages = []
    site_info = []
    contacts_site = []
    liens_site = []

    # Récupérer les chambres libre
    try:
        rooms = chambre.objects.filter(libre=True).order_by("-date_creation")[:3]
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération des chambres du site")

    # Récupérer les photos
    try:
        pictures = Photo.objects.all().order_by("-date_creation")
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération des photos du site")

    # Récupérer les plats principaux
    try:
        plats = plat.objects.filter(status=True, type_plat="P").order_by(
            "-date_creation"
        )
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération des plats du site")
    # Détermination du nombre d'éléments à afficher à droite et à gauche sur la page
    total_plat = len(plats)
    result_plat = total_plat / 2
    if total_plat % 2 == 0:
        x_plat = result_plat
        y_plat = x_plat
    elif total_plat % 2 != 0:
        x_plat = result_plat
        y_plat = total_plat - x_plat

    # Récupérer les desserts
    try:
        desserts = plat.objects.filter(status=True, type_plat="D").order_by(
            "-date_creation"
        )
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération des desserts du site")
    # Détermination du nombre d'éléments à afficher à droite et à gauche sur la page
    total_dessert = len(desserts)
    result_dessert = total_dessert / 2
    if total_dessert % 2 == 0:
        x_dessert = result_dessert
        y_dessert = x_dessert
    elif total_dessert % 2 != 0:
        x_dessert = result_dessert
        y_dessert = total_dessert - x_dessert

    # Récupérer les boissons
    try:
        boissons = plat.objects.filter(status=True, type_plat="B").order_by(
            "-date_creation"
        )
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération des Boissons du site")
    # Détermination du nombre d'éléments à afficher à droite et à gauche sur la page
    total_boisson = len(boissons)
    result_boisson = total_boisson / 2
    if total_boisson % 2 == 0:
        x_boisson = result_boisson
        y_boisson = x_boisson
    elif total_boisson % 2 != 0:
        x_boisson = result_boisson
        y_boisson = total_boisson - x_boisson

    # Récupérer les témoignages
    try:
        temoignages = testimony.objects.filter(visible=True).order_by("-date_creation")
    except Exception as e:
        logger.error(
            "Erreur inattendue lors de la récupération des témoignages du site"
        )

    # Récupérer les Articles
    try:
        Articles = Article.objects.filter(status=True).order_by("-date_creation")[:3]
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération des articles")

    # Récupérer les informations du site
    try:
        site_info = HotelInfo.objects.latest("-date_creation")
    except HotelInfo.DoesNotExist:
        logger.error("Aucune information retournée")
    except Exception as e:
        logger.error(
            "Erreur inattendue lors de la récupération des informations du site"
        )

    # Récupérer les contacts du site
    try:
        contacts_site = ContactCompany.objects.all()[:3]
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération des contacts du site")

    # Récupérer les liens du site
    try:
        liens_site = LienSocialeCompany.objects.all()
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération des liens du site")

    context = {
        "plats": plats,
        "desserts": desserts,
        "boissons": boissons,
        "x_plat": x_plat,
        "y_plat": y_plat,
        "x_dessert": x_dessert,
        "y_dessert": y_dessert,
        "x_boisson": x_boisson,
        "y_boisson": y_boisson,
        "rooms": rooms,
        "pictures": pictures,
        "temoignages": temoignages,
        "Articles": Articles,
        "site_info": site_info,
        "liens_site": liens_site,
        "contacts_site": contacts_site,
    }

    return HttpResponse(template.render(context, request))


# TODO : Affichage de la page réservation
def reservation_view(request):
    template = loader.get_template("reservation.html")

    # initialisation par défaut
    temoignages = []
    site_info = []
    contacts_site = []
    liens_site = []

    # Récupérer les témoignages
    try:
        temoignages = testimony.objects.filter(visible=True).order_by("-date_creation")
    except Exception as e:
        logger.error(
            "Erreur inattendue lors de la récupération des témoignages du site"
        )

    # Récupérer les informations du site
    try:
        site_info = HotelInfo.objects.latest("-date_creation")
    except HotelInfo.DoesNotExist:
        logger.error("Aucune information retournée")
    except Exception as e:
        logger.error(
            "Erreur inattendue lors de la récupération des informations du site"
        )

    # Récupérer les contacts du site
    try:
        contacts_site = ContactCompany.objects.all()[:3]
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération des contacts du site")

    # Récupérer les liens du site
    try:
        liens_site = LienSocialeCompany.objects.all()
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération des liens du site")

    # Gestion du formulaire
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data["full_name"]
            contact = form.cleaned_data["contact"]
            email = form.cleaned_data["email"]
            datearrivee = form.cleaned_data["datearrivee"]
            datedepart = form.cleaned_data["datedepart"]
            adultes = form.cleaned_data["adultes"]
            enfants = form.cleaned_data["enfants"]
            message = form.cleaned_data["message"]
            # * Enregistrer la réservation
            reservation.objects.create(
                nom=full_name,
                contact=contact,
                email=email,
                date_arrivee=datearrivee,
                date_depart=datedepart,
                nombre_adulte=adultes,
                nombre_enfant=enfants,
                message=message,
                is_confirm=0,
            )
            return redirect("reservation_thanks")
    else:
        form = ReservationForm()

    context = {
        "form": form,
        "temoignages": temoignages,
        "site_info": site_info,
        "liens_site": liens_site,
        "contacts_site": contacts_site,
    }

    return HttpResponse(template.render(context, request))


# TODO : Affichage de la page contact 
def contact(request):
    template = loader.get_template("contact.html")

    # initialisation par défaut
    temoignages = []
    site_info = []
    contacts_site = []
    liens_site = []

    # Récupérer les témoignages
    try:
        temoignages = testimony.objects.filter(visible=True).order_by("-date_creation")
    except Exception as e:
        logger.error(
            "Erreur inattendue lors de la récupération des témoignages du site"
        )

    # Récupérer les informations du site
    try:
        site_info = HotelInfo.objects.latest("-date_creation")
    except HotelInfo.DoesNotExist:
        logger.error("Aucune information retournée")
    except Exception as e:
        logger.error(
            "Erreur inattendue lors de la récupération des informations du site"
        )

    # Récupérer les contacts du site
    try:
        contacts_site = ContactCompany.objects.all()[:3]
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération des contacts du site")

    # Récupérer les liens du site
    try:
        liens_site = LienSocialeCompany.objects.all()
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération des liens du site")

    # Gestion du formulaire
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data["full_name"]
            contact = form.cleaned_data["contact"]
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]
            try:
                # * Avec le template personnalisé
                send_email_in_background_template(full_name, contact, message, email)
            except BadHeaderError:
                return HttpResponse("En-tête non valide trouvé.")
            return redirect("message_thanks")
    else:
        form = ContactForm()

    context = {
        "form": form,
        "temoignages": temoignages,
        "site_info": site_info,
        "liens_site": liens_site,
        "contacts_site": contacts_site,
    }

    return HttpResponse(template.render(context, request))


# TODO : Affichage d'un article
def article_details(request, slug):
    template = loader.get_template("single_article.html")

    # initialisation par défaut
    article = []
    site_info = []
    contacts_site = []
    liens_site = []

    # Récupérer l'article
    try:
        article = Article.objects.get(slug=slug)  # On récupère l'article avec le slug
    except Article.DoesNotExist:
        logger.error("Aucune information retournée")
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération de l'article")

    # Récupérer les informations du site
    try:
        site_info = HotelInfo.objects.latest("-date_creation")
    except HotelInfo.DoesNotExist:
        logger.error("Aucune information retournée")
    except Exception as e:
        logger.error(
            "Erreur inattendue lors de la récupération des informations du site"
        )

    # Récupérer les contacts du site
    try:
        contacts_site = ContactCompany.objects.all()[:3]
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération des contacts du site")

    # Récupérer les liens du site
    try:
        liens_site = LienSocialeCompany.objects.all()
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération des liens du site")

    context = {
        "article": article,
        "site_info": site_info,
        "liens_site": liens_site,
        "contacts_site": contacts_site,
    }

    return HttpResponse(template.render(context, request))


# TODO : Affichage de la page blog
def blog(request):
    template = loader.get_template("events.html")

    # initialisation par défaut
    Articles = []
    site_info = []
    contacts_site = []
    liens_site = []

    # Récupérer les Articles
    try:
        Articles = Article.objects.filter(status=True).order_by("-date_creation")
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération des articles du site")

    paginator = Paginator(Articles, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Récupérer les informations du site
    try:
        site_info = HotelInfo.objects.latest("-date_creation")
    except HotelInfo.DoesNotExist:
        logger.error("Aucune information retournée")
    except Exception as e:
        logger.error(
            "Erreur inattendue lors de la récupération des informations du site"
        )

    # Récupérer les contacts du site
    try:
        contacts_site = ContactCompany.objects.all()[:3]
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération des contacts du site")

    # Récupérer les liens du site
    try:
        liens_site = LienSocialeCompany.objects.all()
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération des liens du site")

    context = {
        "Articles": Articles,
        "site_info": site_info,
        "liens_site": liens_site,
        "contacts_site": contacts_site,
        "page_obj": page_obj,
    }

    return HttpResponse(template.render(context, request))


# TODO : Affichage de la partie 'a propos'
def about(request):
    template = loader.get_template("about.html")

    # initialisation par défaut
    Leadership = []
    pictures = []
    site_info = []
    contacts_site = []
    liens_site = []

    # Récupérer les Agents
    try:
        Leadership = ServiceClient.objects.filter(pinned=True, actif=False).order_by(
            "-date_creation"
        )
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération des leader de l'hôtel")

    # Récupérer les photos
    try:
        pictures = Photo.objects.all().order_by("-date_creation")
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération des photos")

    # Récupérer les informations du site
    try:
        site_info = HotelInfo.objects.latest("-date_creation")
    except HotelInfo.DoesNotExist:
        logger.error("Aucune information retournée")
    except Exception as e:
        logger.error(
            "Erreur inattendue lors de la récupération des informations du site"
        )

    # Récupérer les contacts du site
    try:
        contacts_site = ContactCompany.objects.all()[:3]
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération des contacts du site")

    # Récupérer les liens du site
    try:
        liens_site = LienSocialeCompany.objects.all()
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération des liens du site")

    context = {
        "Leadership": Leadership,
        "pictures": pictures,
        "site_info": site_info,
        "liens_site": liens_site,
        "contacts_site": contacts_site,
    }

    return HttpResponse(template.render(context, request))


# TODO : Affichage des chambres
def rooms(request):
    template = loader.get_template("rooms.html")

    # initialisation par défaut
    rooms = []
    best_rooms = []
    site_info = []
    contacts_site = []
    liens_site = []

    # Récupérer les chambres libre
    try:
        rooms = chambre.objects.filter(libre=True).order_by("-date_creation")
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération des chambres")

    paginator = Paginator(rooms, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Récupérer les chambres libre et qui sont des meilleurs offres
    try:
        best_rooms = chambre.objects.filter(is_best=True, libre=True)
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération des meilleur chambres")

    # Récupérer les informations du site
    try:
        site_info = HotelInfo.objects.latest("-date_creation")
    except Exception as e:
        logger.error(
            "Erreur inattendue lors de la récupération des informations du site"
        )

    # Récupérer les contacts du site
    try:
        contacts_site = ContactCompany.objects.all()[:3]
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération des contacts du site")

    # Récupérer les liens du site
    try:
        liens_site = LienSocialeCompany.objects.all()
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération des liens du site")

    context = {
        "rooms": rooms,
        "best_rooms": best_rooms,
        "site_info": site_info,
        "liens_site": liens_site,
        "contacts_site": contacts_site,
        "page_obj": page_obj,
    }

    return HttpResponse(template.render(context, request))


# TODO : Affichage d'un plat
def plat_details(request, nom):
    template = loader.get_template("single_food.html")

    # Initialisation par défaut
    site_info = None
    contacts_site = []
    liens_site = []

    # Récupérer le plat
    plats = get_object_or_404(plat, nom=nom)

    # Récupérer les informations du site
    try:
        site_info = HotelInfo.objects.latest("-date_creation")
    except HotelInfo.DoesNotExist:
        logger.error("Aucune information retournée")
    except Exception as e:
        logger.error(
            "Erreur inattendue lors de la récupération des informations du site"
        )

    # Récupérer les contacts du site
    try:
        contacts_site = ContactCompany.objects.all()[:3]
    except Exception as e:
        logger.error("Erreur inattendue lors des contact")

    # Récupérer les liens du site
    try:
        liens_site = LienSocialeCompany.objects.all()
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération des liens du site")

    context = {
        "plats": plats,
        "site_info": site_info,
        "liens_site": liens_site,
        "contacts_site": contacts_site,
    }

    return HttpResponse(template.render(context, request))


# TODO : Affichage d'une chambre
def chambre_details(request, pk):
    template = loader.get_template("single_food.html")

    # initialisation par défaut
    chambre_x = []
    site_info = []
    contacts_site = []
    liens_site = []

    # Récupérer la chambre
    try:
        chambre_x = get_object_or_404(chambre, pk=pk)
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération de la chambre")

    # Récupérer les informations du site
    try:
        site_info = HotelInfo.objects.latest("-date_creation")
    except HotelInfo.DoesNotExist:
        logger.error("Aucune information retournée")
    except Exception as e:
        logger.error(
            "Erreur inattendue lors de la récupération des informations du site"
        )

    # Récupérer les contacts du site
    try:
        contacts_site = ContactCompany.objects.all()[:3]
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération des contacts du site")

    # Récupérer les liens du site
    try:
        liens_site = LienSocialeCompany.objects.all()
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération des liens du site")

    context = {
        "chambre_x": chambre_x,
        "site_info": site_info,
        "liens_site": liens_site,
        "contacts_site": contacts_site,
    }

    return HttpResponse(template.render(context, request))


# TODO: Pour Ajouter le visiteur à la newsletter
def add_newsletter(request):
    from_email = request.POST.get("from_email", "")
    if from_email:
        try:
            # * Sauvegarder l'email
            NewsLetterEmail.objects.create(email_visteur=from_email, actif=True)
        except BadHeaderError:
            return HttpResponse("En-tête non valide trouvé.")
        return redirect("news_thanks")
    else:
        messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")


# TODO : Affichage de la page de remerciement pour newsletter
def news_thanks(request):
    template = loader.get_template("news_thanks.html")

    # initialisation par défaut
    site_info = []
    contacts_site = []
    liens_site = []

    new_subscriber_text_intro = "🎉 Merci pour votre inscription !"

    new_subscriber_text_content = "Nous sommes ravis de vous compter parmi nos abonnés. \nVous recevrez bientôt nos dernières actualités, conseils exclusifs et contenus inspirants directement dans votre boîte mail. \n📬 N’oubliez pas de vérifier vos spams et d’ajouter notre adresse à vos contacts !"

    # Récupérer les informations du site
    try:
        site_info = HotelInfo.objects.latest("-date_creation")
    except HotelInfo.DoesNotExist:
        logger.error("Aucune information retournée")
    except Exception as e:
        logger.error(
            "Erreur inattendue lors de la récupération des informations du site"
        )

    # Récupérer les contacts du site
    try:
        contacts_site = ContactCompany.objects.all()[:3]
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération des contacts du site")

    # Récupérer les liens du site
    try:
        liens_site = LienSocialeCompany.objects.all()
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération des liens du site")

    context = {
        "new_subscriber_text_intro": new_subscriber_text_intro,
        "new_subscriber_text_content": new_subscriber_text_content,
        "site_info": site_info,
        "liens_site": liens_site,
        "contacts_site": contacts_site,
    }

    return HttpResponse(template.render(context, request))


# TODO : Affichage de la page de remerciement après envoie de message du client vers le site
def message_thanks(request):
    template = loader.get_template("message_thanks.html")

    thanks_text_intro = "🎉 Merci pour votre message !"

    thanks_text_content = "Nous vous contacterons dans les plus brefs délai"

    # Récupérer les informations du site
    try:
        site_info = HotelInfo.objects.latest("-date_creation")
    except Exception as e:
        pass

    # Récupérer les contacts du site
    try:
        contacts_site = ContactCompany.objects.all()[:3]
    except Exception as e:
        pass

    # Récupérer les liens du site
    try:
        liens_site = LienSocialeCompany.objects.all()
    except Exception as e:
        pass

    context = {
        "thanks_text_intro": thanks_text_intro,
        "thanks_text_content": thanks_text_content,
        "site_info": site_info,
        "liens_site": liens_site,
        "contacts_site": contacts_site,
    }

    return HttpResponse(template.render(context, request))


# TODO : Affichage de la page de remerciement pour les réservations
def reservation_thanks(request):
    template = loader.get_template("reservation_thanks.html")

    new_reservation_text_intro = "Merci pour votre réservation !"

    new_reservation_text_content = "Nous avons bien reçu votre demande et vous en remercions. \n📅 Un récapitulatif de votre réservation vient de vous être envoyé par e-mail. \nNous avons hâte de vous accueillir et restons à votre disposition pour toute question."

    # Récupérer les informations du site
    try:
        site_info = HotelInfo.objects.latest("-date_creation")
    except Exception as e:
        pass

    # Récupérer les contacts du site
    try:
        contacts_site = ContactCompany.objects.all()[:3]
    except Exception as e:
        pass

    # Récupérer les liens du site
    try:
        liens_site = LienSocialeCompany.objects.all()
    except Exception as e:
        pass

    context = {
        "new_reservation_text_intro": new_reservation_text_intro,
        "new_reservation_text_content": new_reservation_text_content,
        "site_info": site_info,
        "liens_site": liens_site,
        "contacts_site": contacts_site,
    }

    return HttpResponse(template.render(context, request))


# TODO: Pour vérifier les chambres disponibles
def verify_disponibility(request):
    template = loader.get_template("disponibility.html")

    # Gestion du formulaire
    if request.method == "POST":
        date_arrivee = request.POST.get("date_arrivee", "")
        date_depart = request.POST.get("date_depart", "")
        nombre_adulte = request.POST.get("nombre_adulte", "")
        nombre_enfant = request.POST.get("nombre_enfant", "")
        if date_arrivee and date_depart and nombre_adulte and nombre_enfant:
            try:
                chambre_disponible = chambre.objects.raw(
                    """
                    SELECT * 
                    FROM nova_chambre 
                    WHERE libre = 1 
                    AND id_chambre NOT IN (SELECT id_chambre 
                    FROM nova_reservation_chambre WHERE is_finish = 0 AND date_arrivee = %s)
                    """,
                    [date_arrivee],
                )
            except BadHeaderError:
                return HttpResponse("En-tête non valide trouvé.")
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")

    # Récupérer les informations du site
    try:
        site_info = HotelInfo.objects.latest("-date_creation")
    except Exception as e:
        logger.error(
            "Erreur inattendue lors de la récupération des informations du site"
        )

    # Récupérer les contacts du site
    try:
        contacts_site = ContactCompany.objects.all()[:3]
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération des contacts du site")

    # Récupérer les liens du site
    try:
        liens_site = LienSocialeCompany.objects.all()
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération des liens du site")

    context = {
        "chambre_disponible": chambre_disponible,
        "site_info": site_info,
        "liens_site": liens_site,
        "contacts_site": contacts_site,
    }

    return HttpResponse(template.render(context, request))
