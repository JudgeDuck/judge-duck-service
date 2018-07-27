#encoding=utf-8

# This file is for data store

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

users = None
problems = None
submissions = None
last_sub_id = 0
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
	ret = []
	for pid in problems:
		if problem_class != "":
			if problems[pid]["class"] != problem_class: continue
		ret.append(pid)
	lock.release()
	return sorted(ret)

def do_get_problem_info(pid):
	lock.acquire()
	ret = problems.get(pid, None)
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
	user = users.get(name, None)
	user["language"] = language
	write_user_profile(user)
	
	pinfo = problems.get(pid, None)
	if pinfo == None:
		lock.release()
		ret["error"] = "题目不存在"
		return ret
	
	if len(code) > 100 * 1024:
		lock.release()
		ret["error"] = "代码太长"
		return ret
	
	global last_sub_id
	sid = last_sub_id
	print("sid %s, pid %s, name %s" % (sid, pid, name))
	try:
		code_to_write = code
		utils.write_file(path_temp + "code.txt", code_to_write)
		utils.write_file(path_temp + "code_copy.txt", code_to_write)
		meta = "player_name %s\n" % name
		meta += "submit_time %s\n" % utils.get_current_time()
		meta += "pid %s\n" % pid
		meta += "language %s\n" % language
		utils.write_file(path_temp + "meta.txt", meta)
		os.rename(path_temp + "meta.txt", path_metadata + "%d.txt" % sid)
		os.rename(path_temp + "code.txt", path_code + "%d.txt" % sid)
		os.rename(path_temp + "code_copy.txt", path_pending + "%d.txt" % sid)
		update_submission(sid)
		last_sub_id += 1
		lock.release()
		ret["status"] = "success"
		return ret
	except:
		lock.release()
		ret["error"] = "系统错误"
		return ret

def do_get_submission(sid):
	lock.acquire()
	ret = submissions.get(sid, None)
	lock.release()
	return ret


def do_get_board(pid):
	lock.acquire()
	pinfo = problems.get(pid, None)
	if pinfo == None:
		lock.release()
		return []
	board_map = {}
	for i in submissions:
		sub = submissions[i]
		if sub["pid"] != pid:
			continue
		if sub["status"] != "Accepted":
			continue
		player_name = sub["name"]
		time_ms = sub["time"]
		if not (player_name in board_map) or time_ms < board_map[player_name][0]:
			board_map[player_name] = [time_ms, sub["sid"]]
	board = []
	for i in board_map:
		board.append(board_map[i])
	board = sorted(board)[:100]
	ret = []
	for row in board:
		ret.append(submissions[row[1]])
	lock.release()
	return ret


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
	global users
	if users.get(username, None) != None:
		ret["error"] = "用户名已被使用！"
		lock.release()
		return ret
	user = {
		"username": username,
		"email": email,
		"password": encrypt_password(password),
		"signature": rand_signature(),
	}
	write_user_profile(user)
	add_user(username)
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
	res = check_user_password(username, password)
	lock.release()
	if not res:
		ret["error"] = "用户名或密码错误"
		return ret
	ret["status"] = "success"
	req.session["username"] = username
	return ret

def check_user_password(username, password):
	global users
	user = users.get(username, None)
	if user == None:
		return False
	if user["password"] != encrypt_password(password):
		return False
	return True

def do_logout(req):
	del req.session["username"]

def do_get_user_info(username):
	lock.acquire()
	global users
	ret = users.get(username, None)
	lock.release()
	return ret

def do_rand_signature(username):
	lock.acquire()
	global users
	user = users.get(username, None)
	if user != None:
		user["signature"] = rand_signature()
		write_user_profile(user)
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
	if not check_user_password(username, password):
		ret["error"] = "原密码不正确！"
		lock.release()
		return ret
	global users
	user = users.get(username, None)
	if user != None:
		if new_password != "":
			user["password"] = encrypt_password(new_password)
		user["email"] = email
		user["signature"] = signature
		write_user_profile(user)
	lock.release()
	ret["status"] = "success"
	ret["username"] = username
	return ret
	
#

def do_get_submissions(pid, username, score1, score2):
	lock.acquire()
	global submissions
	res = {}
	for sub in submissions.values():
		if (pid != "") and (sub["pid"] != pid):
			continue
		if (username != "") and (sub["name"] != username):
			continue
		score = sub["score"]
		if (score < score1) or (score > score2):
			continue
		res[-sub["sid"]] = sub
	keys = sorted(res.keys())
	ret = []
	for k in keys:
		ret.append(res[k])
	lock.release()
	return ret

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
	init_users()
	init_problems()
	init_submissions()
	init_blogs()
	lock.release()

def reload():
	init()
#

def init_users():
	global users
	users = {}
	li = utils.list_dir(path_users)
	for filename in li:
		if filename[-4:] != ".txt":
			continue
		username = filename[:-4]
		add_user(username)
	print("total %d users" % len(users))

def add_user(username):
	global users
	filename = path_users + username + ".txt"
	content = utils.read_file(filename).split("\n")
	user = {
		"username": username,
		"email": "",
		"password": "",
		"signature": "",
		"language": "C++",
	}
	keys = [
		"email",
		"password",
		"signature",
		"language",
	]
	for s in content:
		match_k = None
		for k in keys:
			if s[:len(k)] == k:
				match_k = k
				break
		if match_k != None:
			val = s[len(match_k) + 1:]
			user[match_k] = val
	users[username] = user

def write_user_profile(user):
	filename = path_users + user["username"] + ".txt"
	temp_filename = path_temp + "tmp_user.txt"
	f = open(temp_filename, "w")
	f.write("\n".join(["%s %s" % (k, user[k]) for k in user]))
	f.close()
	try:
		os.rename(temp_filename, filename)
	except:
		print("Error: write user [%s]'s profile failed" % user["username"])

def init_problems():
	global problems
	problems = {}
	li = utils.list_dir(path_problems)
	utils.mkdir(path_problem_zips)
	utils.system("rm", ["-rf", path_problem_zips + "*"])
	for pid in li:
		if pid[:1] == ".":
			continue
		if not add_problem(pid):
			continue

def add_problem(pid):
	prob = {
		"pid": pid,
		"name": "不知道",
		"description": "不存在的",
		"time_limit": 1000,
		"memory_limit": 4,
		"time_limit_text": "",
		"memory_limit_text": "",
		"files": [],
		"statement": "",
		"class": "",
	}
	path = path_problems + pid + "/"
	conf_content = utils.read_file(path + "config.txt").split("\n")
	keys = [
		"name",
		"description",
		"time_limit",
		"memory_limit",
		"files",
		"class",
	]
	for s in conf_content:
		if s == "hidden":
			# Hide this problem
			return False
		match_k = None
		for k in keys:
			if s[:len(k)] == k:
				match_k = k
				break
		if match_k != None:
			val = s[len(match_k) + 1:]
			if match_k == "time_limit" or match_k == "memory_limit":
				val = int(val)
				if val <= 0:
					val = 1
			if match_k == "files":
				val = val.split(" ")
			prob[match_k] = val
	prob["statement"] = utils.read_file(path + "statement.md", "咕咕咕")
	prob["sample_code"] = utils.read_file(path + "sample.cpp", "咕咕咕")
	prob["time_limit_text"] = utils.render_time_ns(int(prob["time_limit"]))
	prob["memory_limit_text"] = utils.render_memory_kb(int(prob["memory_limit"]))
	problems[pid] = prob
	return True



#

def init_submissions():
	global submissions
	submissions = {}
	n_subs = len(utils.list_dir(path_code))
	global last_sub_id
	last_sub_id = n_subs
	for i in range(n_subs):
		update_submission(i)

def get_status_short_from_status(status):
	return {
		"Accepted": "AC",
		"Wrong Answer": "WA",
		"Time Limit Exceeded": "TLE",
		"Memory Limit Exceeded": "MLE",
		"Runtime Error": "RE",
		"Judge Failed": "Failed",
	}.get(status, "Done")

def update_sub_using_json(sub, res, save = False):
	time_ns = utils.parse_int("%s" % res["max_time_ns"], 0)
	mem_kb = utils.parse_int("%s" % res["max_mem_kb"], 0)
	score = utils.parse_float(res["score"], 0)
	status = res["status"]
	status_short = res["status_short"]
	if status_short == "":
		status_short = get_status_short_from_status(status)
	sub["time"] = time_ns
	sub["time_text"] = utils.render_time_ns(time_ns)
	sub["memory"] = mem_kb
	sub["memory_text"] = utils.render_memory_kb(mem_kb)
	sub["score"] = score
	sub["score_text"] = "%.0lf" % score
	sub["status"] = status
	sub["status_short"] = status_short
	if save:
		utils.write_file(path_result + "%s.txt" % sub["sid"], json.dumps(res,indent=4,sort_keys=True))
		sub["saved"] = True
		sub["detail"] = ""
	else:
		sub["saved"] = False
		sub["detail"] = json.dumps(res,indent=4,sort_keys=True)

def update_submission(sid, new_judge_time = None):
	global submissions
	global problems
	
	metadata_filename = path_metadata + "%d.txt" % sid
	metadata_content = utils.read_file(metadata_filename).split("\n")
	if new_judge_time != None:
		tmp = ["judge_time %s" % new_judge_time]
		for s in metadata_content:
			if s[:len("judge_time ")] == "judge_time ":
				continue
			tmp.append(s)
		metadata_content = tmp
		try:
			f = open(metadata_filename, "w")
			f.write("\n".join(tmp))
			f.close()
		except:
			pass
	
	player_name = "咕咕咕"
	submit_time = "不存在的"
	judge_time = "N/A"
	pid = ""
	keys = [
		"judge_time",
		"player_name",
		"submit_time",
		"pid",
		"language",
	]
	language = "C"
	for s in metadata_content:
		if s == "hidden":
			if submissions.get(sid, None) != None:
				del submissions[sid]
			return
		match_k = None
		match_content = None
		for k in keys:
			if s[:len(k)] == k:
				match_k = k
				match_content = s[len(k) + 1:]
				break
		if match_k == None:
			continue
		if match_k == "judge_time":
			judge_time = match_content
		if match_k == "submit_time":
			submit_time = match_content
		if match_k == "player_name":
			player_name = match_content
		if match_k == "pid":
			pid = match_content
		if match_k == "language":
			language = match_content
	
	
	sub = {
		"sid": sid,
		"pid": pid,
		"status": "Unknown",
		"time": None,
		"time_text": "N/A",
		"memory": None,
		"memory_text": "N/A",
		"score": 0,
		"score_text": "N/A",
		"code_length": len(utils.read_file(path_code + "%d.txt" % sid)),
		"code_length_text": "N/A",
		"name": player_name,
		"submit_time": submit_time,
		"judge_time": judge_time,
		"language": language,
		"status_short": "",
		"saved": True,
	}
	
	sub["code_length_text"] = utils.render_code_length(sub["code_length"])
	
	res = utils.read_file(path_result + "%s.txt" % sid)
	try:
		res = json.loads(res)
		update_sub_using_json(sub, res)
	except:
		pass
	
	submissions[sid] = sub

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
