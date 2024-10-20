import django_filters

from .models import Annonces, Products

class AnnounceFilter(django_filters.FilterSet):
    class Meta:
        model = Annonces
        fields = ['annonce_name', 'category', 'villes']


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Products
        fields = ['product_price']
