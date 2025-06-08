from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # TODO: Affiche la page d'accueil
    path("", views.index, name="index"),

    # TODO: Affiche la page des chambres
    path("chambres", views.rooms, name="chambres"),

    # TODO: Affiche la page about
    path("nous", views.about, name="nous"),

    # TODO: Affiche la page blog
    path("articles", views.blog, name="articles"),

    # TODO: Affiche un unique article
    path(
        "articles/article_detail/<slug:slug>",
        views.article_details,
        name="article_detail",
    ),

    # TODO: Affiche la page contact
    path("contact", views.contact, name="contact"),

    # TODO: Affiche la page reservation
    path("reservation", views.reservation_view, name="reservation"),

    # TODO: Affiche un unique plat
    path("plat_detail/<str:nom>", views.plat_details, name="plat_detail"),

    # TODO: Affiche une chambre
    path(
        "chambres/chambre_detail/<int:pk>",
        views.chambre_details,
        name="chambre_detail",
    ),

    # TODO: Pour s'ajouter à le visiteur à la newsletter
    path("subscribe_news", views.add_newsletter, name="subscribe_news"),

    # TODO: Affiche la page de remercienement après inscription à la newsletter
    path(
        "news_thanks",
        views.news_thanks,
        name="news_thanks",
    ),

    # TODO: Affiche la page de remercienement après réservation
    path(
        "reservation_thanks",
        views.reservation_thanks,
        name="reservation_thanks",
    ), 
    
    # TODO: Affiche la page de remercienement après envoie de message du client vers le site
    path("message_thanks", views.message_thanks, name="message_thanks"),

    # TODO: Affiche la page de vérification des chambres disponibles
    path("verify_room", views.verify_disponibility, name="verify_room"), 

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
