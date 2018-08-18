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
from . import old_urls
import html
import os
import subprocess
import threading
import time
import datetime
from django.http import Http404

from . import new_oj
from . import judgeduck

@csrf_exempt
def entry(req):
	req.jd_start_time = time.time()
	host = req.META["HTTP_HOST"]
	if host == "judge-duck.online:10086":
		return HttpResponseRedirect("https://judge-duck.online" + req.path)
	return judgeduck.entry(req)

#

def handler404(req, exception):
	host = req.META["HTTP_HOST"]
	return judgeduck.handle_404(req)

def handler500(req):
	host = req.META["HTTP_HOST"]
	return judgeduck.handle_500(req)

urlpatterns = [url("", entry)]



#urlpatterns = [
#url("^judge-duck.online:10086/", include(judgeduck)),
#url("^[^/]+/jd/", include(judgeduck)),
#url("^[^/]+/old/", include(old_urls)),
#url("^[^/]+/new/", include(new_oj)),
#url("^[^/]+/", include(new_oj)),
#url("^", entry),
#url("^", include(new_oj)),
#url("^new/", include(new_oj)),
#url("^jd/", include(judgeduck)),
#url('^$', old_urls.index),
#url('^detail$', old_urls.detail),
#url('^board$', old_urls.board_view),
#url("^old/", include(old_urls)),
# url(r'^admin/', include(admin.site.urls)),
#]
# + static('/static/', document_root='./static')
