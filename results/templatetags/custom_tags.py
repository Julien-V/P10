#!/usr/bin/python3
# coding : utf-8

import logging

from django import template

from results.models import Translation
from results.utils import detect_lang

###############################################################################
# Logs
###############################################################################
logger = logging.getLogger(__name__)
logger.setLevel(20)


register = template.Library()


@register.simple_tag(takes_context=True)
def print_tr(context, tag):
    """This function gets Translation model by tag (from DB)
    and return translated text in the better available language.

    # How to use :
    === template.html
    * {% load custom_tags %}
    * <!-- Some HTML -->
    * <p id="log_in">{% print_tr "log_in"}</p>

    :param context: dict(), view context (i believe)
    :param tag: str(), tag name

    :return tag: str(), tag if tag DoesNotExist in DB
    :return: str(), tag translated in language_detected[0]
    :return: str(), tag translated in french (default)
    """
    try:
        text = Translation.objects.get(tag=tag)
    except Translation.DoesNotExist:
        logger.warning(f"Tagname '{tag}' DoesNotExist")
        return tag
    # get Translation fields by calling text._meta.get_fields():
    lang_available = [f.name for f in text._meta.get_fields() if '_' in f.name]
    # :lang_available is a list(available_lang_for_var text)
    lang_detected, extra = detect_lang(context["request"], lang_available)
    if lang_detected is not None:
        if lang_detected in lang_available:
            return getattr(text, lang_detected)
        else:
            logger.warning(
                f"print_tr : lang_detected but not available", extra=extra)
            return getattr(text, "fr_FR")
    else:
        return getattr(text, "fr_FR")
