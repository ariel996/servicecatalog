from django.conf import Settings
from .models import Webinfo, Categories

def website_info(request):
    webinfo = Webinfo.objects.all()
    return {'webinfo': webinfo}

def categories_info(request):
    categories = Categories.objects.all()
    return {'categories': categories}