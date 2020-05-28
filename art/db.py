
from django.db import models
from django.contrib.auth.models import User


class Client(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Utilisateur associe")
    default_shipping_address = models.ForeignKey("Address",on_delete=models.CASCADE,
                                                 related_name="default_shipping_address",
                                                 null=True,
                                                 verbose_name="Adresse de livraison par défaut"
                                                 )
    default_invoicing_address = models.ForeignKey("Address",on_delete=models.CASCADE,
                                                  related_name="default_invoicing_address",
                                                  null=True,
                                                  verbose_name="Adresse de facturation par défaut"
                                                  )

    def __unicode__(self):
        return self.user.username + " (" + self.user.first_name + " " + self.user.last_name + ")"

    def addresses(self):
        return Address.objects.filter(client_id=self.id)

    def orders(self):
        return Order.objects.filter(client_id=self.id).order_by('-id')




class TVA(models.Model):

    percent = models.FloatField(verbose_name="Taux de TVA (décimal)")

    class Meta:
        verbose_name = 'Taux de TVA'
        verbose_name_plural = 'Taux de TVA'

    def __unicode__(self):
        return str(self.percent * 100) + " %"


class Category(models.Model):

    name = models.CharField(max_length=150, verbose_name="Nom de la catégorie")
    short_desc = models.CharField(max_length=150, verbose_name="Description courte", blank=True)
    parent_category = models.ForeignKey("Category",on_delete=models.CASCADE, null=True, blank=True, verbose_name="Catégorie parente")

    class Meta:
        verbose_name = 'Catégorie de produits'
        verbose_name_plural = 'Catégories de produits'

    def __unicode__(self):
        return self.name

    # noinspection PyMethodFirstArgAssignment
    def breadcrum(self):
        breadcrum = list()
        breadcrum.append(self)

        while self.parent_category:
            breadcrum.insert(0, self.parent_category)
            self = self.parent_category

        return breadcrum

    def childs_categories(self):
        """Retourne les catégories enfant de la catégorie"""
        childs = Category.objects.filter(parent_category_id__exact=self.id)
        return childs

    def all_products(self):
        """ """
        next_main_category = Category.objects.filter(id__gt=self.id, parent_category_id=None).order_by('id').first()

        if not next_main_category:
            products = Product.objects.filter(category_id__gte=self.id)
        else:
            products = Product.objects.filter(category_id__range=(self.id, next_main_category.id-1))
        return products


class Product(models.Model):

    name = models.CharField(max_length=150, verbose_name="Nom du produit")
    category = models.ForeignKey(Category,on_delete=models.CASCADE, verbose_name="Catégorie du produit")
    short_desc = models.CharField(max_length=150, verbose_name="Description courte")
    long_desc = models.TextField(verbose_name="Description longue")
    price = models.FloatField(verbose_name="Prix HT du produit")
    vat = models.ForeignKey(VAT,on_delete=models.CASCADE, verbose_name="Taux de TVA")
    thumbnail = models.ImageField(verbose_name="Miniature du produit", upload_to='art/media', null=True)

    class Meta:
        verbose_name = 'Produit'
        verbose_name_plural = 'Produits'

    def __unicode__(self):
        return self.name

    def price_including_vat(self):
        
        return round(self.price + (self.price * self.vat.percent), 2)


class Photo(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='art/media')




