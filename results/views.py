from django.shortcuts import render, redirect, reverse

from django.http import HttpResponseNotFound

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

import json

from datetime import datetime as dt

from results.models import CategoriesProducts as pb_cat_prod
from results.models import Product
from results.models import Favorite

from results.forms import ConnectionForm, RegisterForm


###############################################################################
# Public views
###############################################################################
def index(req):
    return render(req, "index.html")


def terms(req):
    context = {
        "masthead_title": "Mentions légales"
    }
    return render(req, 'terms.html', context)


def search_results(req):
    """This view searchs substitutes with better
    nutrition grades and display them"""
    results_exists = True
    query = req.GET.get('query')
    if not query or not len(query.split()):
        prod = Product.objects.all()
        results_exists = False
    else:
        prod = Product.objects.filter(
            product_name__icontains=query)
    if not prod.exists():
        results_exists = False
        prod = Product.objects.all()
    if results_exists:
        # get cat of first elem in prod
        choosen_nG = prod[0].nutrition_grades
        cat = pb_cat_prod.objects.filter(product=prod[0])[0].category
        # get substitutes for choosen cat
        elem_list = pb_cat_prod.objects.filter(category=cat)
        prod_list = [x.product for x in elem_list]
        # get substitutes with better nutrition_grades than product's
        subs_list = [x for x in prod_list if x.nutrition_grades < choosen_nG]
        # sort them
        sorted_subs_list = sorted(
            subs_list,
            key=lambda i: i.nutrition_grades
        )
        context = {
            'product_searched': prod[0],
            'masthead_title': prod[0].product_name,
            'products': sorted_subs_list
        }
    else:
        # if prod.exists() == False
        # or if results_exists == False
        # all products in db are displayed
        prod_list = prod
        sorted_prod_list = sorted(
            prod_list,
            key=lambda i: i.nutrition_grades
        )
        context = {
            'product_searched': None,
            'masthead_title': "Aucun résultat",
            'products': sorted_prod_list
        }
    return render(req, "results.html", context)


def product(req):
    """This view displays product's page"""
    query = req.GET.get('code')
    if not query:
        prod = Product.objects.all()
    else:
        prod = Product.objects.filter(
            code=query)
    if not prod:
        return HttpResponseNotFound()
    else:
        prod = prod[0]
        req100 = json.loads(prod.req100.replace('-', ''))
        ng = prod.nutrition_grades.upper()
        ng_image = f"/static/assets/img/Nutri-{ng}.png"
        context = {
            'masthead_title': prod.product_name,
            'ng_image': ng_image,
            'product_searched': prod,
            'req100': req100
        }
    return render(req, 'product.html', context)


def log_in(req):
    error = False
    if req.method == "POST":
        form = ConnectionForm(req.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            # Vérification
            user = authenticate(
                username=username,
                password=password)
            if user:
                login(req, user)
            else:
                error = True
    else:
        form = ConnectionForm()
    return render(req, 'authentification.html', locals())


def sign_in(req):
    error = False
    if req.method == "POST":
        form = RegisterForm(req.POST)
        if form.is_valid():
            temp = req.POST.copy()
            temp["username"] = temp["email"]
            form = RegisterForm(temp)
            if form.is_valid():
                form.save()
                return redirect(reverse('home'))
    else:
        form = RegisterForm()
    return render(req, 'register.html', locals())


###############################################################################
# @login_required
###############################################################################
@login_required
def substitute(req):
    """This view saves a substitute in Favorite
    or displays saved substitute"""
    if req.method == "POST":
        query = req.POST.get('code')
        if not query:
            return redirect(reverse('home'))
        else:
            prod = Product.objects.filter(
                code__contains=int(query))
        if not prod.exists():
            return redirect(reverse('home'))
        user = User.objects.filter(username__contains=req.user)[0]
        fav = Favorite(
            user_id=user,
            product_id=prod[0],
            updated_timestamp=int(dt.now().timestamp()))
        fav.save()
        return redirect(reverse('home'))
    else:
        user = User.objects.filter(
            username__contains=req.user)[0]
        subs = Favorite.objects.filter(user_id=user)
        context = {
            "subs": [x.product_id for x in subs],
            "masthead_title": "Mes Aliments"
        }
        return render(req, "substitute.html", context)


@login_required
def account(req):
    """This view displays user's informations"""
    f_name = req.user.first_name
    l_name = req.user.last_name
    context = {
        'masthead_title': f"{f_name} {l_name}"
    }
    return render(req, 'account.html', context)


@login_required
def log_out(req):
    logout(req)
    return redirect(reverse('home'))
