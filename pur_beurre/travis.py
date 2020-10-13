#!/usr/bin/python3
# coding : utf-8

from . import *
import os

if os.environ.get("IS_TRAVIS", None):
	# config db for travis
	DATABASES = {
	    'default': {
	        'ENGINE': 'django.db.backends.postgresql',
	        'NAME': '',
	        'USER': 'postgres',
	        'PASSWORD': '',
	        'HOST': '',
	        'PORT': '',
	    }
	}
