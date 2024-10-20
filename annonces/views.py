from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.utils.datetime_safe import datetime
from django.utils.translation import gettext as _
from django.utils.crypto import get_random_string

import json

from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponseRedirect
from .filters import AnnounceFilter

from django.utils import translation


from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.mail import EmailMessage

from .forms import *
from .models import *
from .decorators import unauthenticated_user, allowed_users, prestataire_only
from .functions import account_activation_token
from django.views import View

from django.contrib import messages

# Create your views here.
def signupPage(request):
    return render(request, 'annonces/signup.html')

@unauthenticated_user
def registerPage(request):
    form = CreateUserForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            email_subject = 'Activate your account'
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            Profile.objects.create(user=user)
            current_site = get_current_site(request)
            message = render_to_string('annonces/activate_account.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.id)),#.decode(),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(email_subject, message, to=[to_email])
            email.send()
            username = form.cleaned_data.get('username')
            # user type to create its account
            user_group = form.cleaned_data.get('group')
            if user_group is None:
                group = Group.objects.get(name=user_group)
            else:
                group = Group.objects.get(name='user')
            user.groups.add(group)

            messages.success(request, 'We have sent you an email, Please confirm your email address to complete ' + username)
            return redirect('login')
    else:
        form = CreateUserForm()
    return render(request, 'annonces/register.html', {'form': form})

def activate_account(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('login')
    else:
        return redirect('signup')

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        user_is_client = Group.objects.get(name="user").user_set.all()
        user_is_prestataire = Group.objects.get(name="prestataire").user_set.all()

        if user is not None:
            if user.is_active:
                if user in user_is_client:
                    login(request, user)
                    messages.success(request, 'You logged in !')
                    return redirect('user_page')
                else:
                    login(request, user)
                    messages.success(request, 'You logged in !')
                    return redirect('dashboard')
            else:
                messages.info(request, 'Your account is not activated !!!')
        else:
            messages.info(request, 'Username or password is incorrect')

    context = {}
    return render(request, 'annonces/login.html', context)

@login_required(login_url='login')
@prestataire_only
def show_profile(request, pk):
    #profile = get_object_or_404(Profile, user_id=pk)
    profile = Profile.objects.get(user_id=pk)
    context = {'profile': profile}
    return render(request, 'annonces/prestataire/profile/show.html', context)

@login_required(login_url='login')
@prestataire_only
def edit_profile(request, pk):
    # user_profile = Profile.objects.get(user_id=pk)
    # form = ProfileForm(instance=user_profile)
    if request.method == 'POST':
        user_form = UserEditForm(data=request.POST or None, instance=request.user)
        profile_form = ProfileEditForm(data=request.POST or None, instance=request.user.profile, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            # return redirect('show_profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    context = {'user_form': user_form, 'profile_form': profile_form}
    return render(request, 'annonces/prestataire/profile/edit.html', context)

def logoutUser(request):
    logout(request)
    messages.success(request, 'Successfully deconnected from dashboard')
    return redirect('home')

# Prestataire view
@login_required(login_url='login')
#@prestataire_only
def dashboard(request):
    #bookingcount = Annonces.objects.filter(user_id=request.user.id).count()
    servicescount = Services.objects.filter(user_id=request.user.id).count()
    messages_count = Messages.objects.filter(statut=0).count()
    context = {'servicescount': servicescount, 'messages_count': messages_count}
    return render(request, 'annonces/provider/dashboard.html', context)

# CATALOGUE PRESTATAIRE
@login_required(login_url='login')
@prestataire_only
def list_catalogue(request):
    catalogues = Catalogue.objects.filter(user_id=request.user.id)
    context = {'catalogues': catalogues}
    return render(request, 'annonces/prestataire/catalogues/index.html', context)

@login_required(login_url='login')
@prestataire_only
def create_catalogue(request):
    form = CatalogueForm()
    if request.method == 'POST' and request.FILES['catalogue_picture']:
        form = CatalogueForm(request.POST, request.FILES)
        if form.is_valid():
            form.nom = request.POST.get('nom')
            form.user = request.user.id
            form.catalogue_picture = request.POST.get('catalogue_picture')
            form.save()
            return redirect('list_catalogue')
    # form = CatalogueForm()
    context = {'form': form}
    return render(request, 'annonces/prestataire/catalogues/create.html', context)

@login_required(login_url='login')
@prestataire_only
def edit_catalogue(request, pk):
    catalogue = Catalogue.objects.get(id=pk)
    form = CatalogueForm(instance=catalogue)

    if request.method == 'POST':
        form = CatalogueForm(request.POST, request.FILES, instance=catalogue)
        if form.is_valid():
            form.save()
            return redirect('list_catalogue')
    context = {'form': form, 'catalogue': catalogue}
    return render(request, 'annonces/prestataire/catalogues/edit.html', context)

@login_required(login_url='login')
@prestataire_only
def delete_catalogue(request, pk):
    catalogue = Catalogue.objects.get(id=pk)
    catalogue.delete()
    return redirect('list_catalogue')

# ANNOUNCE PRESTATAIRE
@login_required(login_url='login')
@prestataire_only
def create_announce(request):
    #category = request.category.id
    #form = AnnonceForm(instance=Categories)
    form = AnnonceForm()
    category = Categories.objects.get(id=request.POST.get('category'))
    user = User.objects.get(id=request.user.id)
    if request.method == 'POST' and request.FILES['annonce_photo']:
        #form = AnnonceForm(request.POST, request.FILES, instance=Categories)
        form = AnnonceForm(request.POST, request.FILES)
        files = request.FILES.getlist('image[]')
        if form.is_valid():
            annonce = form.save(commit=False)
            annonce.category = category
            annonce.annonce_name = request.POST.get('annonce_name')
            annonce.annonce_description = request.POST.get('annonce_description')
            annonce.annonce_photo = request.FILES['annonce_photo']
            annonce.user = user
            annonce.villes = request.POST.get('ville')
            #annonce.likes = 0
            annonce.save()
            for f in files:
                annonce_image = AnnonceImage(request.POST, request.FILES)
                annonce_image = Annonce_images(annonce=annonce, image=f)
                annonce_image.save()
            return redirect('list_announce')

        form = AnnonceForm()
    categories = Categories.objects.all()
    villes = Villes.objects.all()
    context = {'form': form, 'categories': categories, 'villes': villes}
    return render(request, 'annonces/prestataire/announces/create.html', context)


@login_required(login_url='login')
@prestataire_only
def list_announces(request):
    announces = Annonces.objects.all().filter(user_id=request.user.id)
    context = {'announces': announces}
    return render(request, 'annonces/prestataire/announces/index.html', context)

@login_required(login_url='login')
@prestataire_only
def update_announce(request, pk):
    announce = Annonces.objects.get(id=pk)
    form = AnnonceForm(instance=announce)
    if request.method == 'POST':
        form = AnnonceForm(request.POST, request.FILES, instance=announce)
        if form.is_valid():
            form = AnnonceForm(request.POST, request.FILES)
            form.save()
            return redirect('list_announce')
    context = {'form': form, 'announce': announce}
    return render(request, 'annonces/prestataire/announces/edit.html', context)

@login_required(login_url='login')
@prestataire_only
def delete_announce(request, pk):
    annonce = Annonces.objects.get(id=pk)
    annonce.delete()
    return redirect('list_announce')


# PRODUCT PRESTATAIRE
@login_required(login_url='login')
@prestataire_only
def list_products(request):
    products = Products.objects.filter(user_id=request.user.id)
    context = {'products': products}
    return render(request, 'annonces/prestataire/products/index.html', context)

@login_required(login_url='login')
@prestataire_only
def create_product(request):
    user = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        category = Categories.objects.get(id=request.POST.get('category'))
        catalogue = Catalogue.objects.get(id=request.POST.get('catalogue'))
        villes = Villes.objects.get(id=request.POST.get('villes'))
        form = ProductForm(request.POST, request.FILES)
        files = request.FILES.getlist('image[]')
        if form.is_valid():
            product = form.save(commit=False)
            product.user = user
            # product.code = get_random_string(5)
            product.category = category
            product.catalogue = catalogue
            product.product_name = request.POST.get('product_name')
            product.product_price = request.POST.get('product_price')
            product.product_description = request.POST.get('product_description')
            product.product_image = request.FILES['product_image']
            product.villes = villes
            product.status = 1
            product.save()
            for f in files:
                product_image = ProductImage(request.POST, request.FILES)
                product_image = Product_images(product=product, image=f)
                product_image.save()
            messages.success(request, 'Service added successfully.')
            return redirect('list_products')
    else:
        form = ProductForm()
    catalogues = Catalogue.objects.all()
    categories = Categories.objects.all()
    villes = Villes.objects.all()
    context = {'form': form, 'catalogues': catalogues,
               'categories': categories, 'villes': villes}
    return render(request, 'annonces/prestataire/products/create.html', context)

@login_required(login_url='login')
@prestataire_only
def edit_product(request, pk):
    product = Products.objects.get(id=pk)
    form = ProductForm(instance=product)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form = ProductForm(request.POST, request.FILES)
            form.save()
            return redirect('list_products')
    catalogues = Catalogue.objects.all()
    categories = Categories.objects.all()
    villes = Villes.objects.all()
    context = {'form': product, 'catalogues': catalogues,
               'categories': categories, 'villes': villes}
    return render(request, 'annonces/prestataire/products/edit.html', context)

@login_required(login_url='login')
@prestataire_only
def delete_product(request, pk):
    product = Products.objects.get(id=pk)
    product.delete()
    return redirect('list_products')

# MESSAGES PRESTATAIRE
@login_required(login_url='login')
@prestataire_only
def presta_show_messages(request):
    messages = Messages.objects.filter(user_id=request.user.id)
    context = {'messages': messages}
    return render(request, 'annonces/prestataire/messages/index.html', context)

@login_required(login_url='login')
def delete_message(request, pk):
    message = Messages.objects.get(id=pk)
    message.delete()
    return redirect('presta_show_messages')

@login_required(login_url='login')
def presta_view_message(request, pk):
    message = Messages.objects.get(id=pk)
    return render(request, 'annonces/prestataire/messages/show.html', {'message': message})

@login_required(login_url='login')
def view_message(request, pk):
    message = Messages.objects.get(id=pk)
    return render(request, 'annonces/client/messages/show.html', {'message': message})

@login_required(login_url='login')
def reply_message(request, pk):
    message = Messages.objects.get(id=pk)
    # form = MessageForm(instance=message)
    # if request.method == 'POST':
    #     form = MessageForm(request.POST, instance=message)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('presta_show_messages')
    context = {'message': message}
    return render(request, 'annonces/client/messages/reply.html', context)

@login_required(login_url='login')
@prestataire_only
def presta_reply_message(request, pk):
    message = Messages.objects.get(id=pk)
    form = MessageForm(instance=message)
    if request.method == 'POST':
        form = MessageForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            return redirect('presta_show_messages')
    context = {'message': message}
    return render(request, 'annonces/prestataire/messages/reply.html', context)

@login_required(login_url='login')
@prestataire_only
def reply_to_message(request):
    form = MessageForm()
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('presta_show_messages')

@login_required(login_url='login')
@prestataire_only
def comments(request):
    comments = Comments.objects.all()
    context = {'comments': comments}
    return render(request, 'annonces/prestataire/comments/index.html', context)

@login_required(login_url='login')
@prestataire_only
def reply_comment(request, pk):
    comment = Comments.objects.get(id=pk)
    context = {'comment': comment}
    return render(request, 'annonces/prestataire/comments/reply.html', context)

@login_required(login_url='login')
def reply_to_comment(request):
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.content = request.POST.get('content')
            form.annonce = request.POST.get('annonce_id')
            form.user = request.user.id
            #form.reply = request.POST.get('reply_id')
            form.save()
            return redirect('comments')
    return redirect('comments')

#User view
@login_required(login_url='login')
def user_page(request):
    # messages = get_object_or_404(Messages, user_id=request.user.id)
    context = {}
    return render(request, 'annonces/customer/main.html', context)

@login_required(login_url='login')
def user_modify(request, pk):
    user_profile = Profile.objects.get(user_id=pk)
    form = ProfileForm(instance=user_profile)
    if request.method == 'POST':
        if form.is_valid():
            form = ProfileForm(request.POST, request.FILES)
            form.save()
            return redirect('show_profile')
    context = {'profile': user_profile}
    return render(request, 'annonces/client/profile/edit.html', context)

@login_required(login_url='login')
def user_show_profile(request, pk):
    profile = Profile.objects.get(user_id=pk)
    context = {'profile': profile}
    return render(request, 'annonces/client/profile/show.html', context)

@login_required(login_url='login')
def show_messages(request, pk):
    messages = Messages.objects.all().filter(user_id=request.user.id, statut=0)
    message_inbox_count = Messages.objects.all().filter(user_id=request.user.id, statut=0).count()
    message_sent_count = Messages.objects.all().filter(user_id=request.user.id, statut=1).count()
    context = {'messages': messages, 'message_inbox_count': message_inbox_count, 'message_sent_count': message_sent_count}
    return render(request, 'annonces/client/messages/index.html', context)

@login_required(login_url='login')
def sent_messages(request, pk):
    messages = Messages.objects.all().filter(user_id=pk)
    context = {'messages': messages}
    return render(request, 'annonces/client/messages/sent.html', context)

@login_required(login_url='login')
def see_message(request, pk):
    message = Messages.objects.get(id=pk)
    message.statut = 1
    message.save()
    context = {'message': message}
    return render(request, 'annonces/client/messages/show.html', context)


# FRONT PAGE VIEW

def products(request):
    context = {}
    return render(request, 'annonces/produits.html', context)

def annonces(request):
    categories = Categories.objects.all().order_by('-id')
    villes = Villes.objects.all()
    annonces = annonces.objects.all()
    annonces_likes = annonces.likes.all()
    context = {'annonces': annonces_likes,
               'categories': categories,
               'villes': villes}
    return render(request, 'annonces/annonces.html', context)

def about(request):
    return render(request, 'annonces/about.html')

def contact(request):
    return render(request, 'annonces/contact.html')

def detail_announce(request, pk):
    annonce = get_object_or_404(Annonces, pk=pk)
    #annonce = get_object_or_404(Annonces, id=request.POST.get('annonce'))
    comments = Comments.objects.filter(annonce=annonce).order_by('-id')
    annonces = Annonces.objects.filter(user=annonce.user.id)
    annonce_images = Annonce_images.objects.filter(annonce=annonce)
    user = get_object_or_404(User, id=request.user.id)
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=annonce)
        if form.is_valid():
            # comment = form.save(commit=False)
            form.user = user
            form.annonce = annonce
            form.content = request.POST.get('content')
            form.save()
            messages.success(request, 'comment added successfully')
            return redirect('detail_announce', annonce.id)
        else:
            messages.warning(request, 'unable to post your comment')
            return redirect('detail_announce', annonce.id)
    context = {'annonce': annonce,
               'comments': comments,
               'annonces': annonces,
               'annonce_images': annonce_images,
               }
    return render(request, 'annonces/single.html', context)

def product_detail(request, pk):
    product = get_object_or_404(Products, pk=pk)
    product_images = Product_images.objects.filter(product=product)
    catalogues = Catalogue.objects.filter(user=product.user.id)
    context = {'product': product, 'product_images': product_images,
               'catalogues': catalogues}
    return render(request, 'annonces/product_detail.html', context)

def see_catalogue(request, pk):
    catalogue = get_object_or_404(Catalogue, pk=pk)
    products = Products.objects.filter(catalogue=catalogue, status=1)
    paginator = Paginator(products, 5)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    context = {'catalogue': catalogue, 'products': products}
    return render(request, 'annonces/list_catalogue.html', context)

def contact_us(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been send successfully !!!')
            return redirect('contact')

def send_message(request):
    form = MessageForm()
    client_email = request.POST.get('client')
    annonce_email = request.POST.get('annonce_email')
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            message = 'Your message has been sent successfully'
            email_subject = 'Message sent'
            email = EmailMessage(email_subject, message, to=[client_email])
            email.send()
            ## send notification to merchant
            email2 = EmailMessage('Message received', 'You have received a message for your announcemnt in CamerBusiness',
                                  to=[annonce_email])
            email2.send()
            messages.success(request, 'Message send successfully')
            return redirect('home')

def send_message_product(request):
    """
    function used to send message in the platform to a user and notify them through email
    :param request:
    :return:
    """
    form = MessageForm()
    message = request.POST.get('contenu')
    client_email = request.POST.get('client')
    contact = request.POST.get('contact')
    name = request.POST.get('name')
    subject = request.POST.get('subject')
    user = request.POST.get('user')
    status = request.POST.get('statut')
    merchant_email = request.POST.get('merchant_email')
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            message = 'Your message has been sent successfully'
            email_subject = 'Message sent'
            email = EmailMessage(email_subject, message, to=[client_email])
            email.send()
            ## send notification to merchant
            email2 = EmailMessage('Message received', 'You have recived a message for your product in CamerBusiness', to=[merchant_email])
            email2.send()
            return redirect('home')


def post_comment(request, pk):
    annonce = get_object_or_404(Annonces, id=request.POST.get('annonce'))
    user = get_object_or_404(User, id=request.user.id)
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=annonce)
        if form.is_valid():
            #comment = form.save(commit=False)
            form.user = user
            form.annonce = annonce
            form.content = request.POST.get('content')
            form.save()
            messages.success(request, 'comment added successfully')
            return redirect('detail_announce', annonce.id)
        else:
            messages.warning(request, 'unable to post your comment')
            return redirect('detail_announce', annonce.id)
            #return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    #return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return redirect('detail_announce', annonce.id)


def like_announce(request):
    annonce = get_object_or_404(Annonces, id=request.POST.get('id'))
    is_liked = False
    if annonce.likes.filter(id=request.user.id).exists():
        annonce.likes.remove(request.user)
        is_liked = False
    else:
        annonce.likes.add(request.user)
        is_liked = True
    context = {'announce': annonce,
               'is_liked': is_liked,
               'total_likes': annonce.total_likes(),
               }
    if request.is_ajax():
        html = render_to_string('annonces/like_section.html', context, request=request)
        return JsonResponse({'form': html})
    #return HttpResponseRedirect(annonce.get_absolute_url())

def get_subcategories(request):
    category = request.GET.get('category_id')
    subcategories = Subcategories.objects.filter(category=category).order_by('name')
    context = {'subcategories': subcategories}
    return render(request, 'annonces/provider/profile/get_subcategories.html', context)
    # return JsonResponse(list(subcategories.values('id', 'name')), safe=False)

def sort_by(request):
    order = request.POST.get('order')
    if order == 'announce':
        data = Annonces.objects.order_by()
    elif order == 'date':
        data = Annonces.objects.filter(date_created = datetime.now)
    else:
        data = Products.objects.order_by()
    data_filtered = data.order_by()
    # else:
    #     annonces == Annonces.objects.filter()
    #     products = Products.objects.filter(product_price=order)
    #context = {'products': products, 'annonces': annonces}
    return data_filtered

def autocomplete(request):
    if request.is_ajax():
        q = request.GET.get('item', '')
        places = Products.objects.filter(product_name__icontains=q)
        announces = Annonces.objects.filter(annonce_name__icontains=q)
        results = []
        for pl in places:
            place_json = {}
            place_json = pl.product_name
            results.append(place_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def search(request):
    category = request.POST.get('category')
    town = request.POST.get('town')
    #radio = request.POST.get('inlineRadioOptions')
    annonces = Annonces.objects.filter(category=category, villes=town)
    #annonces_likes = annonce.likes.all()
    products = Products.objects.filter(category=category, villes=town, status=1)
    villes = Villes.objects.all()
    categories = Categories.objects.all()
    context = {'products': products, 'annonces': annonces,
               'villes': villes, 'categories': categories
               }
    return render(request, 'annonces/search_result.html', context)

def search_by_category(request, pk):
    """Function to search announces or products according to its category"""
    announces = Annonces.objects.filter(category=pk)
    products = Products.objects.filter(category=pk, status=1)
    #items = [products, announces]
    #print(items)
    paginator = Paginator(announces, 2)
    page = request.GET.get('page')
    # ?page=2
    announces = paginator.get_page(page)
    context = {'annonces': announces, 'products': products}
    return render(request, "annonces/search_result.html", context)

def signup_news(request):
    form = NewsletterForm()
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

## FOR NEW DESIGN
#front end

def home(request):
    categories = Categories.objects.all()
    services = Services.objects.filter(user=request.user.id, service_status='active')
    paginator = Paginator(services, 9)
    page = request.GET.get('page')
    services = paginator.get_page(page)
    context = {'categories': categories,
               'services': services,
               }
    return render(request, 'annonces/main.html', context)


def list_services(request):
    services = Services.objects.filter(user=request.user.id, service_status='active')
    paginator = Paginator(services, 9)
    page = request.GET.get('page')
    services = paginator.get_page(page)
    context = {'services': services}
    return render(request, 'annonces/myservices.html', context)

def service_detail(request, id):
    service = get_object_or_404(Services, id=id)
    context = {'service': service}
    return render(request, 'annonces/detailservice.html', context)

def bookservice(request, id):
    service = get_object_or_404(Services, id=id)
    context = {'service': service}
    return render(request, 'annonces/bookservice.html', context)

#user section
def categories(request):
    return 'ok'

def mybookings(request):
    return 'ok'

## PROVIDER SECTION
def myservices(request):
    services = Services.objects.filter(user=request.user.id, service_status='active')
    paginator = Paginator(services, 9)
    page = request.GET.get('page')
    services = paginator.get_page(page)
    context = {'services': services}
    return render(request, 'annonces/provider/myservices/myservices.html', context)

def inactiveservice(request):
    return render(request, 'annonces/provider/myservices/inactive.html')

def postservice(request):
    user = User.objects.get(id=request.user.id)
    #category = Categories.objects.get(id=request.POST.get('service_category'))
    #subcategory = Subcategories.objects.get(category=category)
    form = ServiceForm()
    if request.method == 'POST':
        files = request.FILES.getlist('image[]')
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save(commit=False, )
            service.user = user
            service.service_title = request.POST.get('service_title')
            service.service_amount = request.POST.get('service_amount')
            service.service_location = request.POST.get('service_location')
            service.service_description = request.POST.get('service_description')
            service.service_category = request.POST.get('service_category')
            service.service_subcategory = request.POST.get('service_subcategory')
            service.service_status = request.POST.get('service_status')
            service.service_image = request.FILES['service_image']
            service.save()
            for f in files:
                gallery = Gallery(request.POST, request.FILES)
                gallery = Galleries(service=service, image=f)
                gallery.save()
            return redirect('myservices')
    else:
        form = ServiceForm()
    categories = Categories.objects.all()
    subcategories = Subcategories.objects.all()
    cities = Villes.objects.all()
    context = {'categories': categories, 'subcategories': subcategories,
               'cities': cities}
    return render(request, 'annonces/provider/myservices/addservice.html', context)

def save_service(request):
    user = User.objects.get(id=request.user.id)
    category = Categories.objects.get(id=request.POST.get('service_category'))
    subcategory = Subcategories.objects.get(id=request.POST.get('service_subcategory'))
    form = ServiceForm()
    if request.method == 'POST':
        files = request.FILES.getlist('image[]')
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save(commit=False, )
            service.user = user
            service.service_title = request.POST.get('service_title')
            service.service_amount = request.POST.get('service_amount')
            service.service_location = request.POST.get('service_location')
            service.service_description = request.POST.get('service_description')
            service.service_category = category
            service.service_subcategory = subcategory
            service.service_status = request.POST.get('service_status')
            service.service_image = request.FILES['service_image']
            service.save()
            for f in files:
                gallery = Gallery(request.POST, request.FILES)
                gallery = Galleries(service=service, image=f)
                gallery.save()
            return redirect('myservices')
    else:
        form = ServiceForm()
    categories = Categories.objects.all()
    subcategories = Subcategories.objects.all()
    cities = Villes.objects.all()
    context = {'categories': categories, 'subcategories': subcategories,
               'cities': cities}
    return render(request, 'annonces/provider/myservices/addservice.html', context)

def bookinglist(request):
    bookings = Bookings.objects.all()
    context = {'bookings': bookings}
    return render(request, 'annonces/provider/bookings/index.html', context)

def availability(request):
    return render(request, 'annonces/provider/availability/create.html')

def profilesetting(request):
    if request.method == 'POST':
        user_form = UserEditForm(data=request.POST or None, instance=request.user)
        profile_form = ProfileEditForm(data=request.POST or None, instance=request.user.profile, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            # return redirect('show_profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    context = {'user_form': user_form, 'profile_form': profile_form}
    regions = Regions.objects.all()
    categories = Categories.objects.all()
    context = {'regions': regions, 'categories': categories}
    return render(request, 'annonces/provider/profile/settings.html', context)

## Ajax request to  fetch city from region
def fetch_city(request):
    region_id = request.GET.get('region_id')
    cities = Villes.objects.filter(region=region_id).order_by('name')
    context = {'cities': cities}
    return render(request, 'annonces/provider/profile/ajax_cities.html', context)

def review(request):
    return render(request, 'annonces/provider/reviews/reviews.html')