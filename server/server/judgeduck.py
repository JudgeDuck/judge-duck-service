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
import urllib
import json

from . import jd_htmldocs as htmldocs
from . import jd_database as db
from . import jd_utils as utils

from . import jd_judge

jd_judge.start()

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
	render_time = "%.0lf ms" % ((time.time() - req.jd_start_time) * 1000.0)
	res.write(htmldocs.footer_htmldoc % (utils.get_current_time(), render_time))
	return res

def json_response(req, info):
	return HttpResponse(json.dumps(info), content_type="application/json")

def index_view(req):
	index_content = utils.read_file("jd_data/index.md")
	index_html = markdown2.markdown(index_content)
	return render_view(req, "", htmldocs.index_htmldoc % (render_notices(), index_html))

def render_notices():
	notices = db.do_get_notices()
	ret = []
	for blog in notices:
		bid = blog["bid"]
		title = html.escape(blog["title"])
		post_time = blog["post_time"]
		
		tmp = "<tr>"
		tmp += "<td> <a href='/blog/%s'> %s </a> </td>" % (bid, title)
		tmp += "<td> %s </td>" % post_time
		tmp += "</tr>"
		ret.append(tmp)
	return "\n".join(ret)

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
	problem_class = req.GET.get("class", "")
	problem_classes = [
		"",
		"traditional",
		"model",
		"contest",
	]
	problem_classes_names = [
		"全部题目",
		"传统题",
		"模板题",
		"比赛题",
	]
	if not problem_class in problem_classes:
		problem_class = ""
	doc_classes = []
	for idx in range(len(problem_classes)):
		class_id = problem_classes[idx]
		class_name = problem_classes_names[idx]
		active_str = 'class="active"' if class_id == problem_class else ''
		href_str = "/problems?class=%s" % class_id
		if class_id == "":
			href_str = "/problems"
		doc_classes.append(
			'<li role="presentation"%s><a href="%s">%s</a></li>' % (active_str, href_str, class_name)
		)
	doc_classes = "".join(doc_classes)
	
	plist = db.do_get_problem_list(req, problem_class)
	ret = []
	for pinfo in plist:
		pid = pinfo["pid"]
		name = html.escape(pinfo["name"])
		description = "%s %s, %s" % (html.escape(pinfo["description"]), pinfo["time_limit_text"], pinfo["memory_limit_text"])
		
		votes = pinfo["votes"]
		value = pinfo["value"]
		
		vote_content = []
		vote_content.append(
			"""<a id="vote_up_%s" href="javascript:judgeduck.vote_problem('%s', %s, %s)" class="pull-left glyphicon glyphicon-triangle-top" style="color:%s; font-weight:%s;"></a>""" % (
				pid, pid, "1" if value == 0 else "0", value, "#ccc" if value != 1 else "green", "normal" if value != 1 else "bold"
			)
		)
		vote_content.append("""<span id="vote_value_%s" style="color:%s">%s</span>""" % (
			pid, "green" if votes > 0 else "#ccc" if votes == 0 else "red", ("+%s" if votes > 0 else "%s") % votes
		))
		vote_content.append(
			"""<a id="vote_down_%s" href="javascript:judgeduck.vote_problem('%s', %s, %s)" class="pull-right glyphicon glyphicon-triangle-bottom" style="color:%s; font-weight:%s;"></a>""" % (
				pid, pid, "-1" if value == 0 else "0", value, "#ccc" if value != -1 else "red", "normal" if value != -1 else "bold"
			)
		)
		
		ret.append(htmldocs.problems_problem % (pid, pid, name, description, "".join(vote_content)))
	return render_view(req, "题目列表", htmldocs.problems_htmldoc % (doc_classes, "\n".join(ret)))

def do_vote_problem(req):
	pid = req.POST.get("pid", "")
	value = utils.parse_int(req.POST.get("value", ""), 0)
	return json_response(req, db.do_vote_problem(req, pid, value))

def problem_view(req):
	pid = req.path[len("/problem/"):]
	pinfo = db.do_get_problem_info(pid)
	if pinfo == None:
		raise Http404()
	return render_view(req, "%s - 题目" % pinfo["name"], render_problem(req, pinfo))

def render_problem(req, pinfo):
	lang = "C++"
	username = req.session.get("username", None)
	if username != None:
		user = db.do_get_user_info(username)
		lang = user["language"]
	languages = db.option_languages
	languages_doc = "\n".join(["<option%s> %s </option>" % (" selected" if k == lang else "", k) for k in languages])
	ret = "<h2> %s <a href='/problem/%s/board' class=' pull-right btn btn-success'> 排行榜 </a> </h2>" % (html.escape(pinfo["name"]), pinfo["pid"])
	ret += "<hr />"
	ret += "时间限制： %s <br />" % pinfo["time_limit_text"]
	ret += "空间限制： %s <br />" % pinfo["memory_limit_text"]
	ret += "<br />"
	ret += pinfo["statement_html"]
	ret += "<hr />"
	ret += htmldocs.problem_page_submit_htmldoc % (pinfo["pid"], languages_doc, html.escape(pinfo["sample_code"]))
	return ret

def problem_board_view(req):
	pid = req.path[len("/problem/"):-len("/board")]
	pinfo = db.do_get_problem_info(pid)
	if pinfo == None:
		raise Http404()
	board = db.do_get_board(pid)
	return render_view(req, "%s - 排行榜" % pinfo["name"], render_problem_board(pinfo, board))

def render_problem_board(pinfo, board):
	ret = "<h2> %s - 排行榜 </h2>" % (html.escape(pinfo["name"]))
	ret += "<hr />"
	if len(board) == 0:
		ret += "<p> 还没有人 AC 呢 </p>"
		return ret
	tmp_arr = []
	rank = 0
	for sub in board:
		rank += 1
		sid = sub["sid"]
		username = sub["name"]
		time_text = sub["time_text"]
		memory_text = sub["memory_text"]
		code_length_text = sub["code_length_text"]
		submit_time = sub["submit_time"]
		
		tmp = "<tr>"
		tmp += "<td> %s </td>" % rank
		tmp += "<td> <a href='/submission/%s'> %s </a> </td>" % (sid, sid)
		tmp += "<td style='font-size:13px'> <a href='/user/profile/%s'> %s </a> </td>" % (username, username)
		tmp += "<td style='font-size:13px'> %s </td>" % time_text
		tmp += "<td style='font-size:13px'> %s </td>" % memory_text
		tmp += "<td style='font-size:13px'> %s </td>" % code_length_text
		tmp += "<td style='font-size:13px'> %s </td>" % submit_time
		tmp += "</tr>"
		tmp_arr.append(tmp)
	
	tmp = htmldocs.problem_board_htmldoc % "\n".join(tmp_arr)
	return ret + tmp

def submissions_view(req):
	pid = req.GET.get("pid", "")
	username = req.GET.get("username", "")
	score1 = req.GET.get("score1", "0")
	score2 = req.GET.get("score2", "100")
	score1 = utils.parse_int(score1, 0)
	score2 = utils.parse_int(score2, 100)
	if score1 < 0:
		score1 = 0
	if score1 > 100:
		score1 = 100
	if score2 < 0:
		score2 = 0
	if score2 > 100:
		score2 = 100
	if score1 > score2:
		score2 = score1
	my_button = ""
	my_username = req.session.get("username", None)
	if my_username != None:
		my_button = htmldocs.submissions_my_button % my_username
	doc = htmldocs.submissions_htmldoc
	
	page = req.GET.get("page", "1")
	page = utils.parse_int(page, 1)
	if page <= 0:
		page = 1
	if page >= 100000000:
		page = 100000000
	subs = db.do_get_submissions(pid, username, score1, score2, (page - 1) * 10, 10 * 5)
	n_subs = len(subs)
	n_pages = page - 1 + (n_subs + 10 - 1) // 10
	
	subs = subs[:10]
	
	if n_pages < 1:
		n_pages = 1
	
	if page > n_pages:
		page = n_pages + 1
	
	pagination = ""
	if n_pages > 1:
		start_page = max(page - 4, 1)
		end_page = min(start_page + 8, n_pages)
		start_page = max(end_page - 8, 1)
		href_str = "/submissions?pid=%s&username=%s&score1=%s&score2=%s&page=" % (
			urllib.parse.quote(pid),
			urllib.parse.quote(username),
			score1,
			score2,
		)
		
		pagination += '<ul class="pagination">'
		if page > start_page:
			pagination += '<li><a href="%s%s" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>' % (
				href_str,
				page - 1
			)
		else:
			pagination += '<li class="disabled"><a aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>'
		
		for i in range(start_page, end_page + 1):
			if i == page:
				pagination += '<li class="active"><span>%s</span></li>' % page
			else:
				pagination += '<li><a href="%s%s">%s</a></li>' % (href_str, i, i)
		
		if page < end_page:
			pagination += '<li><a href="%s%s" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>' % (
				href_str,
				page + 1
			)
		else:
			pagination += '<li class="disabled"><a aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>'
	
	args = (
		html.escape(pid),
		html.escape(username),
		score1,
		score2,
		my_button,
		render_submissions(subs),
		pagination,
	)
	return render_view(req, "提交记录", doc % args)

def render_submissions(subs):
	ret = []
	for sub in subs:
		sid = sub["sid"]
		username = sub["name"]
		pid = sub["pid"]
		pinfo = db.do_get_problem_info(pid)
		pname = ""
		if pinfo != None:
			pname = html.escape(pinfo["name"])
		score = sub["score_text"]
		time_text = sub["time_text"]
		memory_text = sub["memory_text"]
		code_length_text = sub["code_length_text"]
		submit_time = sub["submit_time"]
		tmp = "<tr>"
		tmp += "<td> <a href='/submission/%s'> %s </a> </td>" % (sid, sid)
		tmp += "<td style='font-size:13px'> <a href='/user/profile/%s'> %s </a> </td>" % (username, username)
		tmp += "<td style='font-size:13px'> <a href='/problem/%s'> %s </a> </td>" % (pid, pid)
		tmp += "<td> %s </td>" % sub["status_short"]
		tmp += "<td> %s </td>" % score
		tmp += "<td style='font-size:13px'> %s </td>" % time_text
		tmp += "<td style='font-size:13px'> %s </td>" % memory_text
		tmp += "<td style='font-size:13px'> %s </td>" % code_length_text
		tmp += "<td style='font-size:13px'> %s </td>" % sub["language"]
		tmp += "<td style='font-size:13px'> %s </td>" % submit_time
		tmp += "</tr>"
		ret.append(tmp)
	return "\n".join(ret)

def submission_view(req):
	sid = utils.parse_int(req.path[len("/submission/"):])
	sub = db.do_get_submission(sid)
	if sub == None:
		raise Http404()
	
	username = sub["name"]
	pid = sub["pid"]
	pinfo = db.do_get_problem_info(pid)
	pname = ""
	if pinfo != None:
		pname = html.escape(pinfo["name"])
	score = sub["score_text"]
	status = sub["status"]
	time_text = sub["time_text"]
	memory_text = sub["memory_text"]
	code_length_text = sub["code_length_text"]
	submit_time = sub["submit_time"]
	judge_time = sub["judge_time"]
	
	detail1 = "\n".join([
		"<td style='font-size:13px'> <a href='/user/profile/%s'> %s </a> </td>" % (username, username),
		"<td> <a href='/problem/%s'> %s </a> </td>" % (pid, pid + ". " + pname),
		"<td> %s </td>" % status,
		"<td> %s </td>" % score,
		"<td style='font-size:13px'> %s </td>" % time_text,
		"<td style='font-size:13px'> %s </td>" % memory_text,
		"<td style='font-size:13px'> %s </td>" % sub["language"],
		"<td style='font-size:13px'> %s </td>" % code_length_text,
	])
	
	detail2 = "\n".join([
		"<td style='font-size:13px'> %s </td>" % submit_time,
		"<td style='font-size:13px'> %s </td>" % judge_time,
	])
	
	res_content = sub["detail"]
	code_content = sub["code"]
	
	try:
		res = json.loads(res_content)
		res = res["details"]
	except:
		res = []
	
	if len(res) == 0:
		res_show = ""
	else:
		res_show = []
		res_show.append('<div class="row"><div class="col-xs-12">')
		detail_idx = 0
		for detail in res:
			detail_idx += 1
			detail_id_DOM = "detail_%s" % detail_idx
			detail_name = html.escape(detail["name"])
			detail_time = html.escape(detail["time_ns"])
			detail_memory = html.escape(detail["mem_kb"])
			detail_score = html.escape("%s" % detail["score"])
			detail_status = html.escape("%s" % detail["status"])
			detail_alert_type = {
				"Accepted": "alert-success",
				"Compile OK": "alert-success",
				"Wrong Answer": "alert-danger",
				"Time Limit Exceeded": "alert-warning",
				"Memory Limit Exceeded": "alert-info",
				"Runtime Error": "alert-danger",
			}.get(detail["status"], "alert-danger")
			res_show.append("".join([
				'<div class="alert %s">' % detail_alert_type,
				'<div class="text-center row">',
				'<table class="table table-borderless" style="margin:0px"><tr>'
				'<td class="col-xs-2" style="vertical-align:middle;padding-left:20px;padding-right:20px"><b>%s</b></td>' % detail_name,
				'<td class="col-xs-2" style="vertical-align:middle">%s</td>' % detail_time,
				'<td class="col-xs-2" style="vertical-align:middle">%s</td>' % detail_memory,
				'<td class="col-xs-2" style="vertical-align:middle">%s</td>' % detail_status,
				'<td class="col-xs-2" style="vertical-align:middle">Score: %s</td>' % detail_score,
				'<td class="col-xs-2" style="vertical-align:middle">',
				'<a data-toggle="collapse" href="#%s" aria-expanded="false" aria-controls="%s">' % (detail_id_DOM, detail_id_DOM),
				'显示更多',
				'</a>',
				'</td>',
				'</tr></table>',
				'</div>',
				'<div class="collapse" id="%s">' % detail_id_DOM,
				'<br />',
				'<textarea class="form-control" style="background-color: white" rows="8" readonly>%s</textarea>' % html.escape(detail["detail"]),
				'</div>',
				'</div>',
			]))
		res_show.append('</div></div>')
		res_show = "".join(res_show)
		res_show = '<label for="result"> 评测结果 </label>' + res_show
	
	doc = htmldocs.submission_htmldoc
	args = (
		sid,
		detail1,
		detail2,
		html.escape(code_content),
		res_show,
	)
	return render_view(req, "提交记录 %s" % sid, doc % args)

def do_submit(req):
	pid = req.POST.get("pid", "")
	language = req.POST.get("language", "")
	code = req.POST.get("code", "")
	return json_response(req, db.do_submit(req, pid, language, code))

#

def blogs_view(req):
	# TODO: args
	blogs = db.do_get_blogs()
	doc = htmldocs.blogs_htmldoc
	args = (
		render_blogs(blogs),
		"",  # TODO: pagination
	)
	return render_view(req, "博客", doc % args)

def render_blogs(blogs):
	ret = []
	for blog in blogs:
		bid = blog["bid"]
		pid = blog["pid"]
		title = html.escape(blog["title"])
		username = blog["username"]
		post_time = blog["post_time"]
		n_replies = blog["n_replies"]
		tmp = "<tr>"
		tmp += "<td> <a href='/blog/%s'> %s </a> </td>" % (bid, title)
		tmp += "<td style='font-size:13px'> <a href='/user/profile/%s'> %s </a> </td>" % (username, username)
		tmp += "<td style='font-size:13px'> %s </td>" % post_time
		tmp += "<td> %s </td>" % n_replies
		#if pid != "":
		#	tmp += "<td> <a href='/problem/%s'> %s </a> </td>" % (pid, pid)
		#else:
		#	tmp += "<td> </td>"
		tmp += "</tr>"
		ret.append(tmp)
	return "\n".join(ret)

def blog_view(req):
	bid = utils.parse_int(req.path[len("/blog/"):], -1)
	blog = db.do_get_blog(bid)
	if blog == None:
		raise Http404()
	return render_view(req, "%s - 博客" % blog["title"], render_blog(req, blog))

def render_blog(req, blog):
	username = blog["username"]
	post_time = blog["post_time"]
	modified_time = blog["modified_time"]
	bid = blog["bid"]
	
	ret = "<h2>"
	ret += " %s " % html.escape(blog["title"])
	ret += "</h2>"
	ret += "<p>"
	ret += "由 <a href='/user/profile/%s'> %s </a> 于 %s 发表" % (username, username, post_time)
	if modified_time > post_time:
		ret += "，最后修改于 %s" % modified_time
	if req.session.get("username", "") == username:
		ret += "&nbsp; <a href='/blog/%s/edit'>修改</a>" % bid
	ret += "</p>"
	ret += "<hr />"
	ret += markdown2.markdown(blog["content"])
	return ret

def blog_post_view(req):
	return render_view(req, "发表新博客", htmldocs.blog_post_htmldoc)

def do_post_blog(req):
	title = req.POST.get("title", "")
	content = req.POST.get("content", "")
	return json_response(req, db.do_post_blog(req, title, content))

def blog_edit_view(req):
	doc = htmldocs.blog_edit_htmldoc
	username = req.session.get("username", None)
	if username == None:
		raise Http404()
	bid = utils.parse_int(req.path[len("/blog/"):-len("/edit")], -1)
	blog = db.do_get_blog(bid)
	if blog == None:
		raise Http404()
	args = (
		bid,
		html.escape(blog["title"]),
		json.dumps(blog["content"]),
	)
	return render_view(req, "编辑博客", doc % args)

def do_edit_blog(req):
	bid = utils.parse_int(req.POST.get("bid", "-1"), -1)
	title = req.POST.get("title", "")
	content = req.POST.get("content", "")
	return json_response(req, db.do_edit_blog(req, bid, title, content))

def beibishi_view(req):
	return render_view(req, "背笔试！", htmldocs.beibishi_htmldoc % db.do_get_beibishi_count())








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
	
	if path == "/rerererereload":
		if req.session.get("username", "") != "wys":
			raise Http404()
		jd_judge.judge_lock.acquire()
		db.init()
		jd_judge.judge_lock.release()
		return HttpResponseRedirect("/")
	
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
	if path == "/problems/do_vote":
		return do_vote_problem(req)
	if re.match("^/problem/[^/]+/board$", path):
		return problem_board_view(req)
	if re.match("^/problem/[^/]+$", path):
		return problem_view(req)
	if path == "/submissions":
		return submissions_view(req)
	if re.match("^/submission/(0|[1-9][0-9]*)$", path):
		return submission_view(req)
	if path == "/do_submit":
		return do_submit(req)
	
	if path == "/blogs":
		return blogs_view(req)
	if re.match("^/blog/(0|[1-9][0-9]*)$", path):
		return blog_view(req)
	if path == "/blog/post":
		return blog_post_view(req)
	if path == "/blog/do_post":
		return do_post_blog(req)
	if re.match("^/blog/(0|[1-9][0-9]*)/edit$", path):
		return blog_edit_view(req)
	if path == "/blog/do_edit":
		return do_edit_blog(req)
	
	if path == "/beibishi":
		return beibishi_view(req)
	
	raise Http404()
#

def handle_404(req):
	return render_view(req, "找不到页面", "<h2> 找不到此页面 </h2> <hr /> <p> 您是从哪里点进来的…… </p>")

def handle_500(req):
	return render_view(req, "服务器错误", "<h2> 服务器错误 </h2> <hr /> <p> 服务器好像出错了……TAT <br /> 请联系管理员 </p>")

