#!/usr/bin/python3
# coding : utf-8

import pytest
from selenium import webdriver
# https://github.com/mozilla/geckodriver/releases/download/v0.28.0/geckodriver-v0.28.0-linux64.tar.gz
from django.urls import reverse
from django.template import Template, Context


@pytest.mark.django_db()
def test_webdriver(live_server, firefox):
    firefox.get(live_server.url)
    assert firefox.title == "Pur Beurre -"


@pytest.mark.django_db()
def test_custom_tag(live_server, firefox, django_db_set):
    class Req:
        META = {"HTTP_ACCEPT_LANGUAGE": 'en-US;fr_FR;q=0.8,en;q=0.7'}
    context = Context({'request': Req})
    template = Template(
        "{% load custom_tags %}{% print_tr 'log_in' %}")
    text = template.render(context)
    assert text == 'Log In'
