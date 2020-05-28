# -*-coding: UTF-8-*-
from django.db import models
from django.contrib.auth.models import User



class Client(models.Model):
    """
    Un client est une personne inscrite au site dans le but d'effectuer une commande.
    """
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
    adress = models.CharField(max_length=40)
    zip = models.CharField(max_length=40)
    phone = models.CharField(max_length=40)

    def __unicode__(self):
        return self.user.username + " (" + self.user.first_name + " " + self.user.last_name + ")"

    def addresses(self):
        return Address.objects.filter(client_id=self.id)

    def orders(self):
        return Order.objects.filter(client_id=self.id).order_by('-id')

    def __str__(self):
        return str(self.user)


class Address(models.Model):
    """
    Une adresse est liée à un client et pourra être utilisée pour la livraison ou la facturation d'une commande.
    """
    client = models.ForeignKey(Client,on_delete=models.CASCADE)
    MISTER = 'MR'
    MISS = 'MISS'
    MISSES = 'MRS'
    GENDER = (
        (MISTER, 'Monsieur'),
        (MISS, 'Mademoiselle'),
        (MISSES, 'Madame'),
    )
    gender = models.CharField(max_length=4, choices=GENDER, default=MISTER, verbose_name="Civilité")
    first_name = models.CharField(max_length=50, verbose_name="Prénom")
    last_name = models.CharField(max_length=50, verbose_name="Nom")
    company = models.CharField(max_length=50, blank=True, verbose_name="Société")
    address = models.CharField(max_length=255, verbose_name="Adresse")
    additional_address = models.CharField(max_length=255, blank=True, verbose_name="Complément d'adresse")
    postcode = models.CharField(max_length=5, verbose_name="Code postal")
    city = models.CharField(max_length=50, verbose_name="Ville")
    phone = models.CharField(max_length=10, verbose_name="Téléphone")
    mobilephone = models.CharField(max_length=10, blank=True, verbose_name="Téléphone portable")
    fax = models.CharField(max_length=10, blank=True, verbose_name="Fax")
    workphone = models.CharField(max_length=10, blank=True, verbose_name="Téléphone travail")

    class Meta:
        verbose_name = 'Adresse'
        verbose_name_plural = 'Adresses'

    def __unicode__(self):
        return self.first_name + " " + self.last_name + " (" + self.address + ", " + self.postcode + " " + self.city + ")"


class VAT(models.Model):
    """
    Les différents taux de TVA sont associés à des produits.
    """
    percent = models.FloatField(verbose_name="Taux de TVA (décimal)")

    class Meta:
        verbose_name = 'Taux de TVA'
        verbose_name_plural = 'Taux de TVA'

    def __unicode__(self):
        return str(self.percent * 100) + " %"


class Category(models.Model):
    """
    Les catégories permettent d'organiser les produits en rayons d'articles similaires.
    """
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
        """Retourne un fil d'ariane permettant à l'utilisateur d'afficher l'arborescence de la catégorie"""
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
    """
    Les produits sont rangés par catégories et sont référencés dans des lignes de commandes.
    """
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
        """Retourne le prix TTC du produit"""
        return round(self.price + (self.price * self.vat.percent), 2)


class Photo(models.Model):
    """
    Les photos permettent d'illustrer les produits afin d'inciter l'internaute à les acheter.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='art/media')


class Order(models.Model):
    """
    Une commande est passée par un client et comprend des lignes de commandes ainsi que des adresses.
    """
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Client ayant passé commande")
    shipping_address = models.ForeignKey(Address, on_delete=models.CASCADE,
                                         verbose_name="Adresse de livraison",
                                         related_name="order_shipping_address"
                                         )
    invoicing_address = models.ForeignKey(Address,on_delete=models.CASCADE,
                                          verbose_name="Adresse de facturation",
                                          related_name="order_invoicing_address"
                                          )
    order_date = models.DateField(verbose_name="Date de la commande", auto_now=True)
    shipping_date = models.DateField(verbose_name="Date de l'expédition", null=True)
    WAITING = 'W'
    PAID = 'P'
    SHIPPED = 'S'
    CANCELED = 'C'
    STATUS = (
        (WAITING, 'En attente de validation'),
        (PAID, 'Payée'),
        (SHIPPED, 'Expédiée'),
        (CANCELED, 'Annulée'),
    )
    status = models.CharField(max_length=1, choices=STATUS, default=WAITING, verbose_name="Statut de la commande")
    stripe_charge_id = models.CharField(max_length=30, verbose_name="Identifiant de transaction Stripe", blank=True)

    class Meta:
        verbose_name = 'Commande'
        verbose_name_plural = 'Commandes'

    @property
    def total(self):
        total = 0
        order_details = OrderDetail.objects.filter(order_id=self.id)
        for order_detail in order_details:
            total += order_detail.total()
        return round(total,2)

    def article_qty(self):
        order_details = OrderDetail.objects.filter(order_id=self.id)
        return len(order_details)


class OrderDetail(models.Model):
    """
    Une ligne de commande référence un produit, la quantité commandée ainsi que les prix associés.
    Elle est liée à une commande.
    """
    order = models.ForeignKey(Order,on_delete=models.CASCADE, verbose_name="Commande associée")
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    qty = models.IntegerField(verbose_name="Quantité")
    product_unit_price = models.FloatField(verbose_name="Prix unitaire du produit")
    vat = models.FloatField(verbose_name="Taux de TVA")

    class Meta:
        verbose_name = 'Ligne d\'une commande'
        verbose_name_plural = 'Lignes de commandes'

    def total_ht(self):
        return round(self.product_unit_price * float(self.qty), 2)

    def total_vat(self):
        return round(self.product_unit_price * float(self.qty) * self.vat, 2)

    def total(self):
        return round((self.product_unit_price * float(self.qty)) +
                     (self.product_unit_price * float(self.qty) * self.vat), 2)


class CartLine(models.Model):
    """
    Une ligne de panier client.
    """
    client = models.ForeignKey(Client,on_delete=models.CASCADE)
    #user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        verbose_name = 'Commande Passer'
        verbose_name_plural = 'Commande Passer'

    def total_ht(self):
        return round(self.product.price * float(self.quantity), 2)

    def total_vat(self):
        return round(self.product.price * float(self.quantity) * self.product.vat.percent, 2)

    def total(self):
        return round((self.product.price * float(self.quantity)) +
                     (self.product.price * float(self.quantity) * self.product.vat.percent), 2)

    def __str__(self):
        return str(self.client.user)




class Issues(models.Model):
    name = models.CharField(max_length=150, verbose_name="Nom du client")
    desc = models.CharField(max_length=150, verbose_name="Description")
    rec_date = models.DateField(verbose_name="Date de la reclamation", auto_now=True)


    class Meta:
        verbose_name = 'Réclamation'
        verbose_name_plural = 'Reclamation'

    def __unicode__(self):
        return self.name

    def __str(self):
        return str(self.name)

