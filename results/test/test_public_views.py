#!/usr/bin/python3
# coding : utf-8

import pytest

from django.urls import reverse


###############################################################################
# results.views.home
# results.views.terms
# results.views.authentification
# results.views.register
# results.views.search_results
# results.views.product
###############################################################################
@pytest.mark.django_db
@pytest.mark.parametrize(
    'view_name, context',
    [
        ('home', {}),
        ("terms", {}),
        ('authentification', {}),
        ('register', {}),
        ('search_results', {'query': 'Petit Nesquik'}),
        ('product', {'code': 3023290008393})
    ]
)
def test_views_public(client, view_name, context, django_db_set):
    """Test public views, expects status_code == 200"""
    url = reverse(view_name)
    if not context:
        response = client.get(url)
    else:
        # some views needs parameters
        response = client.get(url, context)
    assert response.status_code == 200


###############################################################################
# results.views.sign_in
###############################################################################
@pytest.mark.django_db
def test_register_view(client):
    """Test Register View"""
    form_reg = {
        'username': 'usertest',
        'email': 'usertest@gmail.com',
        'password1': 'test1password',
        'password2': 'test1password',
        'first_name': 'user',
        'last_name': 'test'
    }
    url = reverse('register')
    response = client.post(url, form_reg)
    assert response.status_code == 302
    assert response.url == reverse('home')

###############################################################################
# results.views.log_in
###############################################################################
@pytest.mark.django_db
def test_login_view(client, reg_user):
    """Test login view"""
    reg_user()
    form_auth = {
        'username': 'usertest',
        'password': 'test1password'
    }
    url = reverse('authentification')
    response = client.post(url, form_auth)
    assert response.status_code == 200
