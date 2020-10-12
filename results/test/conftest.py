#!/usr/bin/python3
# coding : utf-8


import pytest

from django.contrib.auth.models import User

from django.core.management import call_command
from results.management.commands.populatedb import Command

from django.urls import reverse

from results.models import Favorite


def pytest_collection_modifyitems(config, items):
    list_items = items.copy()
    # TestPopulateDB should be first
    for i in items:
        if "test_popu_" in getattr(i, 'name'):
            to_move = list_items.pop(list_items.index(i))
            if getattr(list_items[0], 'name') == 'test_popu_invalid':
                list_items.insert(1, to_move)
            else:
                list_items.insert(0, to_move)
    items[:] = list_items


@pytest.fixture(scope='session')
def django_db_set(django_db_setup, django_db_blocker):
    """This fixture load data saved with './manage.py dumpdata'
    command"""
    with django_db_blocker.unblock():
        call_command('loaddata', 'results_data.json')
        pass


@pytest.fixture
def reg_user():
    """This fixture registers usertest"""
    def make_reg():
        User.objects.create_user(
                username="usertest",
                password="test1password"
            )
    return make_reg


@pytest.fixture
def login_user(client, reg_user):
    """This fixture registers and log in usertest"""
    def make_login():
        reg_user()
        client.login(
            username='usertest',
            password='test1password'
        )
        return client
    return make_login


@pytest.fixture
def subs_added(login_user):
    """This fixture adds a substitute in Favorite"""
    def make_subs():
        context = {"code": 3023290008393}
        client = login_user()
        url = reverse('substitute')
        client.post(url, context)
        # now product's code should be in Favorite
        user = client.session['_auth_user_id']
        subs = Favorite.objects.filter(user_id=user)
        prods_code = [x.product_id.code for x in subs]
        assert context['code'] in prods_code
        return client
    return make_subs


@pytest.fixture
def patch_get_and_load(monkeypatch):
    """This function monkeypatchs Command.get_and_load
    with mock_get_and_load. Create a FakeJSON_file class which is
    used to get a json file
    """
    def mock_get_and_load(*args):
        """This function return var values from class FakeJSON_file
        :return: json file in a dict (json.loads())
        """
        return json_file.values
    monkeypatch.setattr(Command, "get_and_load", mock_get_and_load)

    class FakeJSON_file:
        pass

    json_file = FakeJSON_file()
    json_file.values = None
    return json_file
