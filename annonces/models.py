from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=200, null=True)
    dob = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=200, null=True)
    profile_picture = models.ImageField(null=True, blank=True, upload_to='images/')
    category = models.CharField(max_length=200, null=True)
    subcategory = models.CharField(max_length=200, null=True)
    country = models.CharField(max_length=200, null=True)
    region = models.ForeignKey('Regions', on_delete=models.CASCADE, null=True)
    ville = models.ForeignKey('Villes', on_delete=models.CASCADE, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return "Profile of user {}".format(self.user.username)

class Catalogue(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    catalogue_picture = models.ImageField(null=True, blank=True, upload_to='images/')
    nom = models.CharField(max_length=120, null=True)

    def __str__(self):
        return self.nom

class Categories(models.Model):
    category_name = models.CharField(max_length=200)
    category_picture = models.ImageField(null=True, blank=True, upload_to='images/')
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.category_name

class Subcategories(models.Model):
    category = models.ForeignKey('Categories', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    category_picture = models.ImageField(null=True, blank=True, upload_to='images/')
    status = models.IntegerField(null=True)

    def __str__(self):
        return self.name


class Services(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    service_title = models.CharField(max_length=100, null=True)
    service_amount = models.CharField(max_length=100, null=True)
    service_location = models.CharField(max_length=200, null=True)
    service_category = models.ForeignKey('Categories', on_delete=models.CASCADE)
    service_subcategory = models.ForeignKey('Subcategories', on_delete=models.CASCADE)
    service_description = models.TextField(max_length=200, null=True)
    service_status = models.CharField(max_length=50, null=True)
    service_image = models.ImageField(null=True, blank=True, upload_to='images/')
    date_created = models.DateTimeField(auto_now_add=True, null=True)

class Offers(models.Model):
    offer_name = models.CharField(max_length=100, null=True)
    service = models.ForeignKey('Services', on_delete=models.CASCADE)

class Galleries(models.Model):
    service = models.ForeignKey('Services', on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to='images/')

class Reviews(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    service = models.ForeignKey('Services', on_delete=models.CASCADE)
    content = models.TextField(max_length=200)
    review = models.IntegerField(null=True, default=0)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

class Bookings(models.Model):
    service = models.ForeignKey('Services', on_delete=models.CASCADE)
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    service_location = models.CharField(max_length=250, null=True)
    booking_date = models.CharField(max_length=100, null=True)
    booking_time = models.CharField(max_length=100, null=True)
    booking_notes = models.TextField(max_length=200, null=True)
    booking_status = models.CharField(max_length=200, null=True)

class Days(models.Model):
    monday = models.CharField(max_length=100, null=True)
    tuesday = models.CharField(max_length=100, null=True)
    wednesday = models.CharField(max_length=100, null=True)
    thursday = models.CharField(max_length=100, null=True)
    friday = models.CharField(max_length=100, null=True)
    saturday = models.CharField(max_length=100, null=True)
    sunfay = models.CharField(max_length=100, null=True)
    alldays = models.CharField(max_length=100, null=True)

class Times(models.Model):
    fromTime = models.TimeField()
    toTime = models.TimeField()

class Availabilities(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    days = models.ForeignKey('Days', on_delete=models.CASCADE)
    times = models.ForeignKey('Times', on_delete=models.CASCADE)

class Annonces(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    annonce_name = models.CharField(max_length=200)
    annonce_description = models.CharField(max_length=200)
    annonce_photo = models.ImageField(null=True, blank=True, upload_to='images/')
    villes = models.ForeignKey('Villes', null=True, on_delete=models.SET_NULL)
    #likes = models.IntegerField(null=True, default=0)
    #likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='announce_likes', blank=True)
    category = models.ForeignKey('Categories', null=True, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def get_absolute_url(self):
        return reversed("annonces:detail_announce", args=[self.id])

    def total_likes(self):
        return self.likes.count()

class Annonce_images(models.Model):
    annonce = models.ForeignKey('Annonces', null=True, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to='images/')

class Products(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # code = models.CharField(null=True, max_length=30)
    product_name = models.CharField(max_length=200)
    product_price = models.DecimalField(null=True, decimal_places=2, max_digits=10)
    product_quantity = models.IntegerField(null=True)
    product_description = models.TextField(null=True)
    product_image = models.ImageField(null=True)
    villes = models.ForeignKey('Villes', null=True, on_delete=models.CASCADE)
    status = models.IntegerField(null=True, default=0)
    #product_color = models.CharField(max_length=50, null=True)
    #product_size = models.CharField(max_length=200, null=True)
    category = models.ForeignKey('Categories', null=True, on_delete=models.CASCADE)
    catalogue = models.ForeignKey('Catalogue', null=True, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

class Product_images(models.Model):
    product = models.ForeignKey('Products', null=True, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to='images/')

    def __str__(self):
        return self.product.product_name + " Image"

class Comments(models.Model):
    annonce = models.ForeignKey('Annonces', null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

class Annonceproperty(models.Model):
    annonce = models.ForeignKey(Annonces, null=True, on_delete=models.CASCADE)
    number_like = models.IntegerField(null=True)

class Newsletters(models.Model):
    email_address = models.EmailField(max_length=200)
    subscribe = models.TextField(null=True, default=10)


class Messages(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    client = models.CharField(max_length=200, null=True)
    name = models.CharField(max_length=200, null=True)
    subject = models.CharField(max_length=200, null=True)
    contact = models.CharField(max_length=200, null=True)
    contenu = models.TextField(max_length=200, null=True)
    statut = models.TextField(default=10, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

class Regions(models.Model):
    name = models.CharField(max_length=100, null=True)

class Villes(models.Model):
    region = models.OneToOneField(Regions, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Descriptions(models.Model):
    content = models.TextField(max_length=200, null=True)

class Contacts(models.Model):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)
    subject = models.CharField(max_length=100, null=True)
    message = models.TextField(max_length=200, null=True)

class Testimonies(models.Model):
    name = models.CharField(max_length=200, null=True)
    picture = models.ImageField(null=True, blank=True, upload_to='images/')
    position = models.CharField(max_length=200, null=True) # job
    content = models.TextField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Questions(models.Model):
    title = models.CharField(max_length=200, null=True)
    content = models.TextField(max_length=250, null=True)

    def __str__(self):
        return self.title

class Webinfo(models.Model):
    phone = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, null=True)
    address = models.CharField(max_length=120)
    town = models.CharField(max_length=200, null=True)
    country = models.CharField(max_length=200, null=True)
    webname = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.town
