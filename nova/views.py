from pyexpat.errors import messages
from django.urls import reverse_lazy
from django.core.mail import send_mail
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
from .task import send_email_in_background_template
from django.http import BadHeaderError, HttpResponse, HttpResponseRedirect
from django.template import loader

# *Import generic views
from django.views.generic.detail import DetailView
from django.views.generic import View
from django.utils.timezone import now
from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator


# TODO : Affichage de la page d'accueil
def index(request):
    template = loader.get_template("index.html")

    # Récupérer les chambres libre
    try:
        rooms = chambre.objects.filter(libre=True).order_by("-date_creation")[:3]
    except Exception as e:
        pass

    # Récupérer les photos
    try:
        pictures = Photo.objects.all().order_by("-date_creation")
    except Exception as e:
        pass

    # Récupérer les plats principaux
    try:
        plats = plat.objects.filter(status=True, type_plat="P").order_by(
            "-date_creation"
        )
    except Exception as e:
        pass

    # Récupérer les desserts
    try:
        desserts = plat.objects.filter(status=True, type_plat="D").order_by(
            "-date_creation"
        )
    except Exception as e:
        pass

    # Récupérer les boissons
    try:
        boissons = plat.objects.filter(status=True, type_plat="B").order_by(
            "-date_creation"
        )
    except Exception as e:
        pass

    # Récupérer les témoignages
    try:
        temoignages = testimony.objects.filter(visible=True).order_by("-date_creation")
    except Exception as e:
        pass

    # Récupérer les Articles
    try:
        Articles = Article.objects.filter(status=True).order_by("-date_creation")[:3]
    except Exception as e:
        pass

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
        "plats": plats,
        "desserts": desserts,
        "boissons": boissons,
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

    # Récupérer les témoignages
    try:
        temoignages = testimony.objects.filter(visible=True).order_by("-date_creation")
    except Exception as e:
        pass

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
        "temoignages": temoignages,
        "site_info": site_info,
        "liens_site": liens_site,
        "contacts_site": contacts_site,
    }

    return HttpResponse(template.render(context, request))


# TODO : Affichage de la page contact
def contact(request):
    template = loader.get_template("contact.html")

    # Récupérer les témoignages
    try:
        temoignages = testimony.objects.filter(visible=True).order_by("-date_creation")
    except Exception as e:
        pass

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
        "temoignages": temoignages,
        "site_info": site_info,
        "liens_site": liens_site,
        "contacts_site": contacts_site,
    }

    return HttpResponse(template.render(context, request))


# TODO : Affichage d'un article
def article_details(request, slug):

    # Récupérer l'article
    try:
        article = Article.objects.get(slug=slug)  # On récupère l'article avec le slug
    except Exception as e:
        pass

    template = loader.get_template("single_article.html")

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
        "article": article,
        "site_info": site_info,
        "liens_site": liens_site,
        "contacts_site": contacts_site,
    }

    return HttpResponse(template.render(context, request))


# TODO : Affichage de la page blog
def blog(request):
    template = loader.get_template("events.html")

    # Récupérer les Articles
    try:
        Articles = Article.objects.filter(status=True).order_by("-date_creation")
    except Exception as e:
        pass

    paginator = Paginator(Articles, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

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

    # Récupérer les Agents
    try:
        Leadership = ServiceClient.objects.filter(pinned=True, actif=False).order_by(
            "-date_creation"
        )
    except Exception as e:
        pass

    # Récupérer les photos
    try:
        pictures = Photo.objects.all().order_by("-date_creation")
    except Exception as e:
        pass

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

    # Récupérer les chambres libre
    try:
        rooms = chambre.objects.filter(libre=True).order_by("-date_creation")
    except Exception as e:
        pass

    paginator = Paginator(rooms, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Récupérer les chambres libre et qui sont des meilleurs offres
    try:
        best_rooms = chambre.objects.filter(is_best=True, libre=True)
    except Exception as e:
        pass

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

    # Récupérer le plat
    try:
        plats = plat.objects.get(nom=nom)
    except Exception as e:
        pass

    template = loader.get_template("single_food.html")

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
        "plats": plats,
        "site_info": site_info,
        "liens_site": liens_site,
        "contacts_site": contacts_site,
    }

    return HttpResponse(template.render(context, request))


# TODO : Affichage d'une chambre
def chambre_details(request, pk):

    # Récupérer la chambre
    try:
        chambre_x = chambre.objects.get(pk=pk)
    except Exception as e:
        pass

    template = loader.get_template("single_food.html")

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

    new_subscriber_text_intro = "🎉 Merci pour votre inscription !"

    new_subscriber_text_content = "Nous sommes ravis de vous compter parmi nos abonnés. \nVous recevrez bientôt nos dernières actualités, conseils exclusifs et contenus inspirants directement dans votre boîte mail. \n📬 N’oubliez pas de vérifier vos spams et d’ajouter notre adresse à vos contacts !"

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

    new_reservation_text_intro = "✅ Merci pour votre réservation !"

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


# TODO: Pour la gestion des messages envoyée depuis le formulaire
def email_envoyer(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name", "")
        contact = request.POST.get("contact", "")
        from_email = request.POST.get("email", "")
        message = request.POST.get("message", "")
        if full_name and contact and from_email and message:
            try:
                # * Avec le template personnalisé
                send_email_in_background_template(
                    full_name, contact, message, from_email
                )
            except BadHeaderError:
                return HttpResponse("En-tête non valide trouvé.")
            return redirect("message_thanks")
        else:
            return redirect("contact")


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
        "chambre_disponible": chambre_disponible,
        "site_info": site_info,
        "liens_site": liens_site,
        "contacts_site": contacts_site,
    }

    return HttpResponse(template.render(context, request))


# TODO: Pour la gestion des demandes de réservation envoyée depuis le formulaire
def reservation_envoyer(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name", "")
        contact = request.POST.get("contact", "")
        from_email = request.POST.get("email", "")
        date_arrivee = request.POST.get("date_arrivee", "")
        date_depart = request.POST.get("date_depart", "")
        nombre_adulte = request.POST.get("nombre_adulte", "")
        nombre_enfant = request.POST.get("nombre_enfant", "")
        message = request.POST.get("message", "")
        # Fomatage de la date
        from datetime import datetime
        date_A = datetime.strptime(date_arrivee, "%d %B, %Y").date()
        date_B = datetime.strptime(date_depart, "%d %B, %Y").date() 
        if (
            full_name
            and contact
            and from_email
            and message
            and date_arrivee
            and date_depart
            and nombre_adulte
            and nombre_enfant
        ):
            # * Enregistrer la réservation
            reservation.objects.create(
                nom=full_name,
                contact=contact,
                email=from_email,
                date_arrivee=date_A,
                date_depart=date_B,
                nombre_adulte=nombre_adulte,
                nombre_enfant=nombre_enfant,
                message=message,
                is_confirm=0,
            )
            return redirect("reservation_thanks")
        else:
            return redirect("reservation")
