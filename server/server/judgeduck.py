#encoding=utf-8
"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, Context
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from threading import *
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from django.contrib.staticfiles import views as static_views
from django.views.static import serve as static_view_serve
from django.http import Http404
import html
import os
import subprocess
import threading
import time
import datetime
import markdown2

from . import jd_htmldocs as htmldocs
from . import jd_database as db
from . import jd_utils as utils

from . import jd_judge



def index_view(req):
	res = HttpResponse(content_type="text/html")
	res.write(htmldocs.index_htmldoc)
	return res









def entry(req):
	path = req.path
	
	if path[:6] == "/libs/":
		return static_view_serve(req, path = path[6:], document_root = "./jd_static/libs")
	if path[:5] == "/css/":
		return static_view_serve(req, path = path[5:], document_root = "./jd_static/css")
	if path[:8] == "/images/":
		return static_view_serve(req, path = path[8:], document_root = "./jd_static/images")
	
	if path == "/":
		return index_view(req)
	
	raise Http404()
#



