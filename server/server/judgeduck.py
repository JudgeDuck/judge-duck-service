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
import json

from . import jd_htmldocs as htmldocs
from . import jd_database as db
from . import jd_utils as utils

from . import jd_judge

def render_view(req, title, content):
	res = HttpResponse(content_type="text/html")
	if title != "":
		title += " - "
	title += "Judge Duck Online"
	username = req.session.get("username", None)
	if username != None:
		res.write(htmldocs.header_online_htmldoc % (html.escape(title), username, username))
	else:
		res.write(htmldocs.header_htmldoc % html.escape(title))
	res.write(content)
	res.write(htmldocs.footer_htmldoc % utils.get_current_time())
	return res

def json_response(req, info):
	return HttpResponse(json.dumps(info), content_type="application/json")

def index_view(req):
	return render_view(req, "", htmldocs.index_htmldoc)

def faq_view(req):
	faq_content = utils.read_file("jd_data/faq.md")
	faq_html = markdown2.markdown(faq_content)
	return render_view(req, "常见问题及解答", htmldocs.faq_htmldoc % faq_html)

def register_view(req):
	return render_view(req, "注册", htmldocs.register_htmldoc)

def do_register(req):
	username = req.POST.get("username", "")
	email = req.POST.get("email", "")
	password = req.POST.get("password", "")
	return json_response(req, db.do_register(username, email, password))

def login_view(req):
	if req.session.get("username", None) != None:
		return HttpResponseRedirect("/")
	return render_view(req, "登录", htmldocs.login_htmldoc)

def do_login(req):
	username = req.POST.get("username", "")
	password = req.POST.get("password", "")
	return json_response(req, db.do_login(req, username, password))

def logout_view(req):
	db.do_logout(req)
	return HttpResponseRedirect("/")






def entry(req):
	path = req.path
	
	if path[:6] == "/libs/":
		return static_view_serve(req, path = path[6:], document_root = "./jd_static/libs")
	if path[:5] == "/css/":
		return static_view_serve(req, path = path[5:], document_root = "./jd_static/css")
	if path[:4] == "/js/":
		return static_view_serve(req, path = path[4:], document_root = "./jd_static/js")
	if path[:8] == "/images/":
		return static_view_serve(req, path = path[8:], document_root = "./jd_static/images")
	
	if path == "/":
		return index_view(req)
	if path == "/faq":
		return faq_view(req)
	
	if path == "/user/register":
		return register_view(req)
	if path == "/user/do_register":
		return do_register(req)
	if path == "/user/login":
		return login_view(req)
	if path == "/user/do_login":
		return do_login(req)
	if path == "/user/logout":
		return logout_view(req)
	
	raise Http404()
#



