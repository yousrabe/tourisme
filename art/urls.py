from django.conf.urls import url
from . import views
app_name = "art"
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^errorlogin$', views.error, name='error'),
    url(r'^produits$', views.produits_view, name='produits_view'),
    url(r'^logout$', views.logout_view, name='logout_view'),
    url(r'^tunisie$', views.tunisie_view, name='tunisie_view'),
    url(r'^about$', views.about_view, name='about_view'),
    url(r'^contact$', views.contact_view, name='contact_view'),
    url(r'^event$', views.event_view, name='event_view'),
    url(r'^produit/tapis/$', views.cat_view_tapis, name='cat_view_tapis'),
    url(r'^produit/habits/$', views.cat_view_habits, name='cat_view_habits'),
    url(r'^produit/posaique/$', views.cat_view_mosaique, name='cat_view_mosaique'),
    url(r'^produit/bijoux/$', views.cat_view_bijoux, name='cat_view_bijoux'),
    url(r'^produit/cuterie/$', views.cat_view_poterie, name='cat_view_poterie'),
    url(r'^produit/moivre/$', views.cat_view_cuivre, name='cat_view_cuivre'),
    url(r'^produit/ceramique/$', views.cat_view_ceramique, name='cat_view_ceramique'),
    url(r'^produit/tapis/(?P<id>\w{0,50})/$', views.single_view, name='single_view'),
    url(r'^produit/habits/(?P<id>\w{0,50})/$', views.single_view, name='single_view'),
    url(r'^produit/poterie/(?P<id>\w{0,50})/$', views.single_view, name='single_view'),
    url(r'^produit/mosaique/(?P<id>\w{0,50})/$', views.single_view, name='single_view'),
    url(r'^produit/bijoux/(?P<id>\w{0,50})/$', views.single_view, name='single_view'),
    url(r'^produit/cuivre/(?P<id>\w{0,50})/$', views.single_view, name='single_view'),
    url(r'^produit/ceramique/(?P<id>\w{0,50})/$', views.single_view, name='single_view'),
    url(r'^produit/(?P<id>\w{0,50})/$', views.single_view, name='single_view'),
    url(r'^savePanier$', views.savePanier, name='savePanier'),
    url(r'^reclamation$', views.reclamation, name='reclamation'),
    url(r'^facture$', views.facture, name='facture'),
]


										