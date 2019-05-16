#!/usr/bin/env python
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
from django.contrib.auth.models import User

from mysite.models import *

def addDoctors():
	d = Doctor()
	d.name="hopa"
	d.save()
	
addDoctors()