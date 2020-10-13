#!/usr/bin/python3
# coding : utf-8

from . import *
import os

if os.environ.get("IS_TRAVIS", None):
	# secret_key for travis
	SECRET_KEY = "x9zpi2zqh=-!t6y4_e&t_&=b6+lx^%io1gh%ae%8_lf9(cr!%d"
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
