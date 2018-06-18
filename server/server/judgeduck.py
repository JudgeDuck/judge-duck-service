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
import re
import hashlib

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

def profile_view(req):
	username = req.path[len("/user/profile/"):]
	user = db.do_get_user_info(username)
	if user == None:
		raise Http404()
	is_self = username == req.session.get("username", "")
	email = user["email"]
	args = (
		username,
		email,
		html.escape(user["signature"]),
		get_gravatar_image_src(email),
	)
	doc = htmldocs.profile_self_htmldoc if is_self else htmldocs.profile_htmldoc
	return render_view(req, "%s - 用户信息" % username, doc % args)

def get_gravatar_image_src(email):
	return "https://www.gravatar.com/avatar/%s?d=mm&s=512" % hashlib.md5(email.lower().encode("utf-8")).hexdigest()

def edit_profile_view(req):
	username = req.session.get("username", None)
	if username == None:
		return HttpResponseRedirect("/")
	user = db.do_get_user_info(username)
	if user == None:
		return HttpResponseRedirect("/")
	args = (
		user["email"],
		html.escape(user["signature"]),
	)
	return render_view(req, "更改个人信息", htmldocs.edit_profile_htmldoc % args)

def do_edit_profile(req):
	password = req.POST.get("password", "")
	email = req.POST.get("email", "")
	new_password = req.POST.get("new_password", "")
	signature = req.POST.get("signature", "")
	return json_response(req, db.do_edit_profile(req, password, email, new_password, signature))

def rand_signature_view(req):
	username = req.session.get("username", None)
	if username == None:
		return HttpResponseRedirect("/")
	db.do_rand_signature(username)
	return HttpResponseRedirect("/user/profile/%s" % username)

#

def problems_view(req):
	# TODO: 考虑用户是否 AC 这道题
	plist = db.do_get_problem_list()
	ret = []
	for pid in plist:
		pinfo = db.do_get_problem_info(pid)
		if pinfo == None:
			continue
		name = html.escape(pinfo["name"])
		description = "%s %s, %s" % (html.escape(pinfo["description"]), pinfo["time_limit_text"], pinfo["memory_limit_text"])
		ret.append(htmldocs.problems_problem % (pid, pid, name, description))
	return render_view(req, "题目列表", htmldocs.problems_htmldoc % "\n".join(ret))

def problem_view(req):
	pid = req.path[len("/problem/"):]
	pinfo = db.do_get_problem_info(pid)
	if pinfo == None:
		raise Http404()
	return render_view(req, "%s - 题目" % pinfo["name"], render_problem(pinfo))

def render_problem(pinfo):
	ret = "<h2> %s </h2>" % html.escape(pinfo["name"])
	ret += "<hr />"
	ret += "时间限制： %s <br />" % pinfo["time_limit_text"]
	ret += "空间限制： %s <br />" % pinfo["memory_limit_text"]
	ret += "<br />"
	ret += markdown2.markdown(pinfo["statement"])
	ret += "<hr />"
	ret += htmldocs.problem_page_submit_htmldoc % (pinfo["pid"], html.escape(pinfo["sample_code"]))
	return ret










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
	if re.match("^/user/profile/(.{3,20})$", path):
		return profile_view(req)
	if path == "/user/edit_profile":
		return edit_profile_view(req)
	if path == "/user/do_edit_profile":
		return do_edit_profile(req)
	if path == "/user/rand_signature":
		return rand_signature_view(req)
	
	if path == "/problems":
		return problems_view(req)
	if re.match("^/problem/.*$", path):
		return problem_view(req)
	
	raise Http404()
#



