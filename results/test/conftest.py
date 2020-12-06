#!/usr/bin/python3
# coding : utf-8


import pytest
from selenium import webdriver

from django.contrib.auth.models import User

from django.core.management import call_command
from results.management.commands.populatedb import Command

from django.urls import reverse

from results.models import Favorite
from results.models import Profile


def pytest_collection_modifyitems(config, items):
    # TestPopulateDB should be first
    # TestLoadlanguages should be second
    list_items = items.copy()
    desired_order = [
        'test_popu_invalid',
        'test_popu_valid',
        'test_popu_update',
        'test_load_tag']
    d_o_mirror = list()
    for i in items:
        if i.name in desired_order:
            # get test function
            d_o_mirror.append(list_items.pop(list_items.index(i)))
    # sort them
    d_o_mirror = sorted(
        d_o_mirror,
        key=lambda i: desired_order.index(i.name))
    # insert them in order at the beginning of the list
    d_o_mirror.reverse()
    for obj in d_o_mirror:
        list_items.insert(0, obj)
    items[:] = list_items


@pytest.fixture(scope='function')
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
        user = User.objects.create_user(
                username="usertest",
                password="test1password"
            )
        profile = Profile(user=user, lang="fr_FR")
        profile.save()
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


@pytest.fixture(scope="function")
def firefox(django_db_set):
    options = webdriver.FirefoxOptions()
    options.add_argument('-headless')
    with webdriver.Firefox(options=options) as driver:
        yield driver


@pytest.fixture()
def firefox_logged_in(firefox, live_server, login_user):
    client = login_user()
    cookie = client.cookies["sessionid"]
    firefox.get(live_server.url)
    firefox.add_cookie({
        'name': 'sessionid',
        'value': cookie.value,
        'secure': False,
        'path': '/'
        })
    firefox.refresh()
    return firefox
