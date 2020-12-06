#!/usr/bin/python3
# coding : utf-8

import pytest

from django.template import Template, Context


@pytest.mark.django_db()
def test_custom_tag(django_db_set):
    """Test custom tag 'print_tr' when rendering a template"""
    class Req:
        META = {"HTTP_ACCEPT_LANGUAGE": 'en-US;fr_FR;q=0.8,en;q=0.7'}
        COOKIES = dict()
    context = Context({'request': Req})
    custom_string = "{% load custom_tags %}{% print_tr 'log_in' %}"
    template = Template(custom_string)
    text = template.render(context)
    assert text == 'Sign In'
