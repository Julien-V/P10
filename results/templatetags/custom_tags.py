#!/usr/bin/python3
# coding : utf-8

import re
import logging

from django import template

from results.models import Translation

###############################################################################
# Logs
###############################################################################
logger = logging.getLogger(__name__)
logger.setLevel(20)


register = template.Library()


@register.simple_tag(takes_context=True)
def print_tr(context, tagname):
    try:
        text = Translation.objects.get(tag=tagname)
    except Translation.DoesNotExist:
        logger.warning("tagname DoesNotExist")
        return tagname
    # serious rework needed here
    lang_available = [f.name for f in text._meta.get_fields() if '_' in f.name]
    try:
        req = context['request']
        lg = req.META["HTTP_ACCEPT_LANGUAGE"]
    except KeyError:
        return getattr(text, "fr_FR")
    reg = r"""[a-z]{2}[_][A-Z]{2}"""  # xx_XX
    lang_user = re.findall(reg, lg.replace("-", "_"))
    # code below will list matching languages to
    # first two letters ("en") instead of whole
    # language code ("en_GB", "en_US", etc.)
    lang_available_user = list()
    for l in lang_user:
        for lat in lang_available:
            if l[:2] in lat:
                lang_available_user.append(lat)
    if lang_available_user:
        return getattr(text, lang_available_user[0])
    else:
        return getattr(text, "fr_FR")
