#!/usr/bin/python3
# coding : utf-8

import re

from results.models import User


def detect_lang(req, lang_available=["fr_FR", "en_GB"]):
    """This function detects languages from :
        1/  if User: User's account
            else: HTTP_ACCEPT_LANGUAGE
        2/  cookie "lang"
    :param req: Request object
    :param lang_available: list()
    :return lang, dict(user, meta, cookie):
        """
    lang = None
    user, meta, cookie = (None,)*3
    try:
        username = req.user
    except AttributeError:
        # anonymous user :
        username = ""
    # user.lang or meta
    try:
        user = User.objects.get(username=username)
        # lang = user.lang
        # user_lang = lang
    except User.DoesNotExist:
        user = None
        try:
            meta = req.META['HTTP_ACCEPT_LANGUAGE']
            lang = extract_lang(meta, lang_available)
        except AttributeError:
            meta = None
        except KeyError:
            meta = None
    # get cookie
    cookie = req.COOKIES.get("lang")
    if cookie is not None:
        lang = cookie
    return lang, {
        "lang": lang,
        "user": user,
        "meta": meta,
        "cookie": cookie}


def extract_lang(lang, lang_available):
    """This method extracts languages from a string
    like 'en-US;fr_FR;q=0.8,en;q=0.7'
    :param lang: str() from HTTP_ACCEPT_LANGUAGE
    :param lang_available: list() of available language
    :return: str()
    """
    reg = r"""[a-z]{2}[_][A-Z]{2}"""  # xx_XX
    lang_user = re.findall(reg, lang.replace("-", "_"))
    # code below will list matching languages to
    # first two letters ("en") instead of whole
    # language code ("en_GB", "en_US", etc.).
    # Not really a problem when we've only 2 languages...
    lang_available_user = list()
    for l in lang_user:
        for lat in lang_available:
            if l[:2] in lat:
                lang_available_user.append(lat)
    return lang_available_user[0]
