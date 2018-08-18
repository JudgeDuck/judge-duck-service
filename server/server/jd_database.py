#encoding=utf-8

# This file is for data store

from . import jd_sql as sql

db_version = "20180814-1"

path_prefix = "jd_data/"
path_temp = path_prefix + "temp/"
path_problems = path_prefix + "problems/"
path_code = path_prefix + "code/"
path_metadata = path_prefix + "metadata/"
path_result = path_prefix + "result/"
path_pending = path_prefix + "pending/"
path_pending_rejudge = path_prefix + "pending_rejudge/"
path_users = path_prefix + "users/"
path_blogs = path_prefix + "blogs/"
path_problem_zips = path_prefix + "problem_zips/"

option_languages = [
	"C",
	"C++",
	"C++11",
]


import re
from random import *
import hashlib
import json

from threading import *
lock = Lock()

from . import jd_utils as utils
import os

blogs = None
last_blog_id = 0


def do_get_beibishi_count():
	lock.acquire()
	fname = path_prefix + "beibishi_count.txt"
	content = utils.read_file(fname)
	ret = utils.parse_int(content, 0)
	ret = ret + 1
	utils.write_file(fname, "%s" % ret)
	lock.release()
	return ret

def do_get_problem_list(problem_class = ""):
	lock.acquire()
	sql.begin()
	# TODO admin mode
	sql.has_error = False
	if problem_class == "":
		res = sql.query("select `pid`, `name`, `description`, `time_limit`, `memory_limit` from `problems` where `hidden` = 0 order by `pid`")
	else:
		res = sql.query("select `pid`, `name`, `description`, `time_limit`, `memory_limit` from `problems` where `hidden` = 0 and `class` = ? order by `pid`", (problem_class, ))
	if sql.has_error:
		res = []
	sql.rollback()
	
	for i in range(len(res)):
		p = dict(res[i])
		p["time_limit_text"] = utils.render_time_ns(p["time_limit"])
		p["memory_limit_text"] = utils.render_memory_kb(p["memory_limit"])
		res[i] = p
	
	lock.release()
	return res

def do_get_problem_info(pid):
	lock.acquire()
	sql.begin()
	# TODO admin mode
	sql.has_error = False
	res = sql.query("select * from `problems` where `hidden` = 0 and `pid` = ?", (pid, ))
	if sql.has_error:
		res = []
	sql.rollback()
	if len(res) != 1:
		ret = None
	else:
		ret = dict(res[0])
		ret["time_limit_text"] = utils.render_time_ns(ret["time_limit"])
		ret["memory_limit_text"] = utils.render_memory_kb(ret["memory_limit"])
	lock.release()
	return ret

#

# return json
def do_submit(req, pid, language, code):
	ret = {"status": "failed"}
	name = req.session.get("username", None)
	if name == None:
		ret["error"] = "请先登录"
		return ret
	
	if not (language in option_languages):
		ret["error"] = "语言不存在"
		return ret
	
	lock.acquire()
	sql.begin()
	sql.has_error = False
	
	sql.query("update `users` set `language` = ? where `username` = ?", (language, name))
	
	pcnt = sql.query_value("select count(*) from `problems` where `pid` = ?", (pid, ))
	
	if sql.has_error:
		sql.rollback()
		lock.release()
		ret["error"] = "系统错误，请联系管理员"
		return ret
	
	if pcnt != 1:
		sql.rollback()
		lock.release()
		ret["error"] = "题目不存在"
		return ret
	
	if len(code) > 100 * 1024:
		sql.rollback()
		lock.release()
		ret["error"] = "代码太长"
		return ret
	
	sql.query(
		"insert into `submissions` (`pid`, `code`, `code_length`, `submit_time`, `player_name`, `language`) values (?,?,?,?,?,?)",
		(pid, code, len(code), utils.get_current_time(), name, language)
	)
	
	if sql.has_error:
		sql.rollback()
		lock.release()
		ret["error"] = "系统错误，请联系管理员"
		return ret
	
	sid = sql.query_value("select last_insert_rowid()")
	
	if sql.has_error:
		sql.rollback()
		lock.release()
		ret["error"] = "系统错误，请联系管理员"
		return ret
	
	sql.commit()
	
	print("sid %s, pid %s, name %s" % (sid, pid, name))
	utils.write_file(path_pending + "%d.txt" % sid, "")
	
	lock.release()
	ret["status"] = "success"
	return ret

def do_get_submission(sid):
	lock.acquire()
	sql.begin()
	# TODO hidden ?
	res = sql.query("select * from `submissions` where `sid` = ?", (sid, ))
	if len(res) != 1:
		sql.rollback()
		lock.release()
		return None
	sql.rollback()
	
	ret = dict(res[0])
	ret["code_length_text"] = utils.render_code_length(ret["code_length"])
	ret["time_text"] = utils.render_time_ns(ret["time"])
	ret["memory_text"] = utils.render_memory_kb(ret["memory"])
	ret["score_text"] = "%.0lf" % ret["score"]
	ret["name"] = ret["player_name"]
	
	lock.release()
	return ret


def do_get_board(pid):
	lock.acquire()
	sql.begin()
	sql.has_error = False
	board = sql.query("select `username` as 'name', `sid`, min(`time`) as `time`, `memory`, `code_length`, `submit_time` from `users`, `submissions` where `username` = `player_name` and `pid` = ? and `status` = 'Accepted' group by `username` order by `time` limit 100", (pid, ))
	if sql.has_error:
		board = []
	sql.rollback()
	
	for i in range(len(board)):
		ret = dict(board[i])
		ret["code_length_text"] = utils.render_code_length(ret["code_length"])
		ret["time_text"] = utils.render_time_ns(ret["time"])
		ret["memory_text"] = utils.render_memory_kb(ret["memory"])
		board[i] = ret
	
	lock.release()
	return board


def encrypt_password(password):
	return hashlib.md5((password + "judge-duck").encode("utf-8")).hexdigest()

def do_register(username, email, password):
	ret = {"status": "failed"}
	user_regex = "^[a-zA-Z0-9_]{3,20}$"
	email_regex = '^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
	pass_regex = "^[a-f0-9]{32,32}$"
	if not re.match(user_regex, username):
		ret["error"] = "用户名必须由 3 ~ 20 个字母、数字或下划线组成！"
		return ret
	if not re.match(email_regex, email):
		ret["error"] = "电子邮件地址不合法！"
		return ret
	if not re.match(pass_regex, password):
		ret["error"] = "密码格式不正确！"
		return ret
	
	lock.acquire()
	sql.begin()
	
	if sql.query_value("select count(*) from `users` where `username` = ?", (username, )) != 0:
		ret["error"] = "用户名已被使用！"
		sql.rollback()
		lock.release()
		return ret
	
	sql.has_error = False
	sql.query(
		"insert into `users` (`username`, `email`, `password`, `signature`, `register_time`) values (?,?,?,?,?)",
		(username, email, encrypt_password(password), rand_signature(), utils.get_current_time())
	)
	
	if sql.has_error:
		ret["error"] = "系统错误，请联系管理员"
		sql.rollback()
		lock.release()
		return ret
	
	sql.commit()
	lock.release()
	return {"status": "success"}

def rand_signature():
	a = [
		"门前大桥下，游过一群鸭，快来快来数一数，二四六七八",
		"31331 33565 6665444 23212",
		"XX XXX XXXXX XXXXXXX XXXXX",
		"奋战三星期，造台评测鸭",
		"常数优化多小才算够~",
		"O(松)算法通过多从容~",
		"咕咕咕",
		"嘎嘎嘎",
		"喵喵喵",
		"愿天下所有的小鸡、小鸭、小朋友们都能健康成长",
		"我好菜啊",
		"我好巨啊",
		"凉凉夜色为你思念成河~ 化作春泥呵护着我~",
	]
	return a[randint(0, len(a) - 1)]

def do_login(req, username, password):
	ret = {"status": "failed"}
	if req.session.get("username", None) != None:
		ret["error"] = "您已经在线了"
		return ret
	lock.acquire()
	sql.begin()
	res = check_user_password(username, password)
	sql.rollback()
	lock.release()
	if not res:
		ret["error"] = "用户名或密码错误"
		return ret
	ret["status"] = "success"
	req.session["username"] = username
	return ret

def check_user_password(username, password):
	pw = sql.query_value("select `password` from `users` where `username` = ?", (username, ))
	if pw == None:
		return False
	if pw != encrypt_password(password):
		return False
	return True

def do_logout(req):
	del req.session["username"]

def do_get_user_info(username):
	lock.acquire()
	sql.begin()
	users = sql.query("select * from `users` where `username` = ?", (username, ))
	sql.rollback()
	
	user = None
	if len(users) == 1:
		user = users[0]
	
	lock.release()
	return user

def do_rand_signature(username):
	lock.acquire()
	sql.begin()
	sql.query("update `users` set `signature` = ? where `username` = ?", (rand_signature(), username))
	sql.commit()
	lock.release()

def do_edit_profile(req, password, email, new_password, signature):
	ret = {"status": "failed"}
	username = req.session.get("username", None)
	if username == None:
		ret["error"] = "请先登录"
		return ret
	email_regex = '^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
	pass_regex = "^[a-f0-9]{32,32}$"
	if not re.match(email_regex, email):
		ret["error"] = "电子邮件地址不合法！"
		return ret
	if (new_password != "") and (not re.match(pass_regex, new_password)):
		ret["error"] = "密码格式不正确！"
		return ret
	signature = signature.split("\n")[0].split("\r")[0]
	if len(signature) > 35:
		ret["error"] = "个性签名太长！"
		return ret
	
	lock.acquire()
	sql.begin()
	if not check_user_password(username, password):
		ret["error"] = "原密码不正确！"
		sql.rollback()
		lock.release()
		return ret
	cnt = sql.query_value("select count(*) from `users` where `username` = ?", (username, ))
	if cnt != 0:
		ret["error"] = "用户名已被使用！"
		sql.rollback()
		lock.release()
		return ret
	sql.has_error = False
	if new_password != "":
		sql.query("update `users` set `password` = ? where `username` = ?", (encrypt_password(new_password), username))
	sql.query("update `users` set `email` = ?, `signature` = ? where `username` = ?", (email, signature, username))
	if sql.has_error:
		ret["error"] = "系统错误，请联系管理员"
		sql.rollback()
		lock.release()
		return ret
	sql.commit()
	lock.release()
	ret["status"] = "success"
	ret["username"] = username
	return ret
	
#

def do_get_submissions(pid, username, score1, score2, st, cnt):
	lock.acquire()
	sql.begin()
	stmt = "select `sid`, `player_name`, `pid`, `score`, `time`, `memory`, `code_length`, `submit_time`, `language`, `status_short` from `submissions` where 1"
	params = []
	if (score1 != 0) or (score2 != 100):
		stmt += " and `score` >= ? and `score` <= ?"
		params.append(score1)
		params.append(score2)
	if pid != "":
		stmt += " and `pid` = ?"
		params.append(pid)
	if username != "":
		stmt += " and `player_name` = ?"
		params.append(username)
	stmt += " order by `sid` desc limit ?, ?"
	params.append(st)
	params.append(cnt)
	res = sql.query(stmt, params)
	sql.rollback()
	
	for i in range(len(res)):
		res[i] = dict(res[i])
		ret = res[i]
		ret["code_length_text"] = utils.render_code_length(ret["code_length"])
		ret["time_text"] = utils.render_time_ns(ret["time"])
		ret["memory_text"] = utils.render_memory_kb(ret["memory"])
		ret["score_text"] = "%.0lf" % ret["score"]
		ret["name"] = ret["player_name"]
	
	lock.release()
	return res

#

def do_get_blogs():
	lock.acquire()
	global blogs
	ret = []
	for bid in reversed(sorted(blogs.keys())):
		ret.append(blogs[bid])
	lock.release()
	return ret

def do_get_blog(bid):
	lock.acquire()
	global blogs
	ret = blogs.get(bid, None)
	lock.release()
	return ret

def do_get_notices():
	lock.acquire()
	global blogs
	tmp = []
	for blog in blogs.values():
		if blog["sticky_level"] <= 0:
			continue
		tmp.append((blog["sticky_level"], -blog["bid"]))
	tmp = sorted(tmp)[:5]
	ret = []
	for row in tmp:
		ret.append(blogs[-row[1]])
	lock.release()
	return ret

def do_post_blog(req, title, content):
	ret = {"status": "failed"}
	lock.acquire()
	username = req.session.get("username", None)
	if username == None:
		lock.release()
		ret["error"] = "请先登录"
		return ret
	title = title.split("\n")[0].split("\r")[0]
	if title == "":
		lock.release()
		ret["error"] = "标题为空"
		return ret
	if len(title) > 50:
		lock.release()
		ret["error"] = "标题太长"
		return ret
	if len(content) > 65536:
		lock.release()
		ret["error"] = "内容太长"
		return ret
	# Write to file
	fname_content = path_temp + "blog_content.txt"
	utils.write_file(fname_content, content)
	fname_metadata = path_temp + "blog_metadata.txt"
	tmp = ""
	tmp += "title %s\n" % title
	tmp += "username %s\n" % username
	cur_time = utils.get_current_time()
	tmp += "post_time %s\n" % cur_time
	tmp += "modified_time %s\n" % cur_time
	tmp += "last_reply_id 0\n"
	utils.write_file(fname_metadata, tmp)
	global last_blog_id
	bid = last_blog_id
	last_blog_id += 1
	
	utils.mkdir(path_blogs + "%s" % bid)
	foldername = path_blogs + "%s/" % bid
	utils.mkdir(foldername + "replies")
	utils.mkdir(foldername + "reply_metadata")
	utils.rename(fname_content, foldername + "content.md")
	utils.rename(fname_metadata, foldername + "metadata.txt")
	update_blog(bid)
	lock.release()
	ret["status"] = "success"
	ret["bid"] = bid
	return ret

def do_edit_blog(req, bid, title, content):
	ret = {"status": "failed"}
	lock.acquire()
	username = req.session.get("username", None)
	if username == None:
		lock.release()
		ret["error"] = "请先登录"
		return ret
	global blogs
	blog = blogs.get(bid, None)
	if blog == None:
		lock.release()
		ret["error"] = "博客不存在"
		return ret
	title = title.split("\n")[0].split("\r")[0]
	if title == "":
		lock.release()
		ret["error"] = "标题为空"
		return ret
	if len(title) > 50:
		lock.release()
		ret["error"] = "标题太长"
		return ret
	if len(content) > 65536:
		lock.release()
		ret["error"] = "内容太长"
		return ret
	# Write to file
	foldername = path_blogs + "%s/" % bid
	meta_content = utils.read_file(foldername + "metadata.txt").split("\n")
	meta = [
		"modified_time %s" % utils.get_current_time(),
		"title %s" % title,
	]
	for s in meta_content:
		tmp = s.split(" ")[0]
		if tmp == "modified_time":
			continue
		if tmp == "title":
			continue
		meta.append(s)
	utils.write_file(path_temp + "blog_meta.txt", "\n".join(meta))
	utils.write_file(path_temp + "blog_content.txt", content)
	utils.rename(path_temp + "blog_content.txt", foldername + "content.md")
	utils.rename(path_temp + "blog_meta.txt", foldername + "metadata.txt")
	update_blog(bid)
	lock.release()
	ret["status"] = "success"
	return ret







def init():
	lock.acquire()
	check_db_version()
	init_users()
	init_problems()
	init_submissions()
	init_blogs()
	lock.release()

def reload():
	init()
#

def check_db_version():
	global db_version
	version = sql.query("select `value` from jd_meta where `key`='version'")[0][0]
	if version != db_version:
		raise "GG, wrong DB version"
	print("DB version checked")

def init_users():
	pass
	# Yeah, nothing to init

def init_problems():
	pass


#

def init_submissions():
	sql.begin()
	sql.query("update `submissions` set `detail` = '', `status` = 'Unknown', `status_short` = '' where `saved` = 0")
	sql.commit()

def get_status_short_from_status(status):
	return {
		"Accepted": "AC",
		"Wrong Answer": "WA",
		"Time Limit Exceeded": "TLE",
		"Memory Limit Exceeded": "MLE",
		"Runtime Error": "RE",
		"Judge Failed": "Failed",
	}.get(status, "Done")

def do_update_sub_using_json(sid, res, save = False):
	time_ns = utils.parse_int("%s" % res["max_time_ns"], 0)
	mem_kb = utils.parse_int("%s" % res["max_mem_kb"], 0)
	score = utils.parse_float(res["score"], 0)
	status = res["status"]
	status_short = res["status_short"]
	if status_short == "":
		status_short = get_status_short_from_status(status)
	detail = json.dumps(res,indent=4,sort_keys=True)
	saved = 1 if save else 0
	lock.acquire()
	sql.begin()
	sql.query(
		"update `submissions` set `time` = ?, `memory` = ?, `score` = ?, `status` = ?, `status_short` = ?, `detail` = ?, `saved` = ? where `sid` = ?",
		(time_ns, mem_kb, score, status, status_short, detail, saved, sid)
	)
	if saved:
		sql.query("update `submissions` set `judge_time` = ? where sid = ?", (utils.get_current_time(), sid))
	sql.commit()
	lock.release()

#

def init_blogs():
	global blogs
	blogs = {}
	n_blogs = len(utils.list_dir(path_blogs))
	global last_blog_id
	last_blog_id = n_blogs
	for i in range(n_blogs):
		update_blog(i)
	print("loaded %s blogs" % n_blogs)

def update_blog(bid):
	global blogs
	foldername = path_blogs + "%s/" % bid
	metadata_name = foldername + "metadata.txt"
	metadata_content = utils.read_file(metadata_name, "").split("\n")
	blog = {
		"bid": bid,
		"title": "",
		"username": "",
		"pid": "",
		"post_time": "",
		"modified_time": "",
		"sticky_level": 0,
		"n_replies": 0,
		"last_reply_id": 0,
		"replies": [],
		"content": "",
	}
	for s in metadata_content:
		pos = s.find(" ")
		if pos == -1:
			s1 = s
			s2 = ""
		else:
			s1 = s[:pos]
			s2 = s[pos + 1:]
		if s1 == "hidden":
			if blogs.get(bid, None) != None:
				del blogs[bid]
			return
		if s1 == "title":
			blog["title"] = s2
		if s1 == "username":
			blog["username"] = s2
		if s1 == "pid":
			blog["pid"] = s2
		if s1 == "post_time":
			blog["post_time"] = s2
		if s1 == "modified_time":
			blog["modified_time"] = s2
		if s1 == "last_reply_id":
			blog["last_reply_id"] = utils.parse_int(s2, 0)
		if s1 == "sticky_level":
			blog["sticky_level"] = utils.parse_int(s2, 0)
	last_reply_id = blog["last_reply_id"]
	replies_path = foldername + "%s/replies/" % bid
	reply_metadata_path = foldername + "%s/reply_metadata/" % bid
	for i in range(1, last_reply_id + 1):
		reply = {
			"rid": i,
			"username": "",
			"reply_time": "",
			"content": "",
		}
		reply_metadata_content = utils.read_file(reply_metadata_path + "%s.txt" % i, "").split("\n")
		if (len(reply_metadata_content) == 1) and reply_metadata_content[0] == "":
			continue
		has_hidden = False
		for s in reply_metadata_content:
			pos = s.find(" ")
			if pos == -1:
				s1 = s
				s2 = ""
			else:
				s1 = s[:pos]
				s2 = s[pos + 1:]
			if s1 == "hidden":
				has_hidden = True
				break
			if s1 == "username":
				reply["username"] = s2
			if s1 == "reply_time":
				reply["reply_time"] = s2
		if has_hidden:
			continue
		reply["content"] = utils.read_file(replies_path + "%s.txt" % i)
		blog["replies"].append(reply)
	blog["n_replies"] = len(blog["replies"])
	blog["content"] = utils.read_file(foldername + "content.md")
	blogs[bid] = blog







init()
