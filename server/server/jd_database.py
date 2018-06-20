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


import re
from random import *
import hashlib

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


def do_get_problem_list():
	lock.acquire()
	ret = []
	for pid in problems:
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
def do_submit(req, pid, code):
	ret = {"status": "failed"}
	name = req.session.get("username", None)
	if name == None:
		ret["error"] = "请先登录"
		return ret
	
	lock.acquire()
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
	users[username] = user
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
	}
	keys = [
		"email",
		"password",
		"signature",
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
	for pid in li:
		add_problem(pid)

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
	}
	path = path_problems + pid + "/"
	conf_content = utils.read_file(path + "config.txt").split("\n")
	keys = [
		"name",
		"description",
		"time_limit",
		"memory_limit",
		"files",
	]
	for s in conf_content:
		if s == "hidden":
			# Hide this problem
			return
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
	prob["sample_code"] = utils.read_file(path + "sample.c", "咕咕咕")
	prob["time_limit_text"] = utils.render_time_ns(int(prob["time_limit"]))
	prob["memory_limit_text"] = utils.render_memory_kb(int(prob["memory_limit"]))
	problems[pid] = prob



#

def init_submissions():
	global submissions
	submissions = {}
	n_subs = len(utils.list_dir(path_code))
	global last_sub_id
	last_sub_id = n_subs
	for i in range(n_subs):
		update_submission(i)

def update_submission(sid, new_judge_time = None):
	name = path_result + "%d.txt" % sid
	res_str = utils.read_file(name)
	res_arr = res_str.split("\n")
	ok1 = False
	ok2 = False
	time_ms = None
	time_ms_prefix = "time_ms = "
	time_ms_prefix_len = len(time_ms_prefix)
	memory_kb = None
	memory_kb_prefix = "mem_kb = "
	memory_kb_prefix_len = len(memory_kb_prefix)
	#code_content = read_file("code/%d.txt" % id)
	#code_first_row = code_content.split("\n")[0]
	
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
	]
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
	
	
	#if code_first_row[:len(name_magic)] == name_magic:
	#	player_name = code_first_row[len(name_magic):]
	
	sub = {
		"sid": sid,
		"pid": pid,
		"status": "Pending",
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
	}
	
	sub["code_length_text"] = utils.render_code_length(sub["code_length"])
	
	if res_str != "":
		sub["status"] = "Judge Failed"
	
	global submissions
	for s in res_arr:
		if s == "Correct Answer!":
			ok1 = True
		if s[:len("verdict = ")] == "verdict = ":
			sub["status"] = s[len("verdict = "):]
		if s == "verdict = Run Finished":
			ok2 = True
		if s[:time_ms_prefix_len] == time_ms_prefix:
			time_ms = utils.parse_float(s[time_ms_prefix_len:])
			sub["time"] = time_ms
			sub["time_text"] = utils.render_time_ms(time_ms)
		if s[:memory_kb_prefix_len] == memory_kb_prefix:
			memory_kb = utils.parse_int(s[memory_kb_prefix_len:])
			sub["memory"] = memory_kb
			sub["memory_text"] = utils.render_memory_kb(memory_kb)
		if s.find("compile error") != -1:
			sub["status"] = "Compile Error"
	if ok1 and ok2 and time_ms != None:
		if time_ms > 0 and time_ms < 100 * 1000:
			sub["status"] = "Accepted"
	if ok2 and (not ok1):
		sub["status"] = "Wrong Answer"
	if sub["status"] != "Pending":
		sub["score"] = 100 if sub["status"] == "Accepted" else 0
		sub["score_text"] = "%s" % sub["score"]
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
