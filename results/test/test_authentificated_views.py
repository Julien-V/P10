#!/usr/bin/python3
# coding : utf-8

import pytest

from bs4 import BeautifulSoup

from django.urls import reverse

from results.models import Favorite
from results.models import Profile

###############################################################################
# results.views.substitute
###############################################################################
@pytest.mark.django_db
def test_add_subs(login_user, django_db_set):
    """Adding a susbstitute to fav"""
    context = {"code": 3023290008393}
    client = login_user()
    url = reverse('substitute')
    response = client.post(url, context)
    # we should be redirected to "/"
    assert response.status_code == 302
    assert response.url == reverse('home')
    # product code should be in Favorite
    user = client.session['_auth_user_id']
    subs = Favorite.objects.filter(user_id=user)
    prods_code = [x.product_id.code for x in subs]
    assert context['code'] in prods_code


@pytest.mark.django_db
def test_get_subs(subs_added, django_db_set):
    """Get favorite list"""
    client = subs_added()
    url = reverse('substitute')
    response = client.get(url)
    assert response.status_code == 200
    page = BeautifulSoup(response.content, features="html.parser")
    product_col = page.find("div", {'id': 'product-col'})
    assert product_col.find("p").contents[0] == "Sveltesse choco noir"


###############################################################################
# results.views.log_out
###############################################################################
@pytest.mark.django_db
def test_logout_view(login_user, django_db_set):
    client = login_user()
    url = reverse('deauthentification')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('home')


###############################################################################
# results.views.log_out
###############################################################################
@pytest.mark.django_db
def test_ch_lang_view(login_user, django_db_set):
    client = login_user()
    user = client.session['_auth_user_id']
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        print("Profile DoesNotExist")
    old_lang = profile.lang
    url = reverse('ch_lang')
    context = {'lang': 'en_GB'}
    response = client.post(url, context)
    assert response.status_code == 200
    assert response.content.decode() == 'True'
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        print("Profile still DoesNotExist")
    assert old_lang != profile.lang
