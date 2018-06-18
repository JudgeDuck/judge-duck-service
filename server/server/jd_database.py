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


import re
from random import *

from threading import *
lock = Lock()

from . import jd_utils as utils
import os

users = None
problems = None
submissions = None
last_sub_id = 0


def get_problem_list():
	lock.acquire()
	ret = []
	for pid in problems:
		ret.append(pid)
	lock.release()
	return sorted(ret)

def get_problem_info(pid):
	lock.acquire()
	ret = problems.get(pid, None)
	lock.release()
	return ret

#

# return sid
def submit(pid, name, code):
	lock.acquire()
	pinfo = problems.get(pid, None)
	if pinfo == None:
		lock.release()
		return None
	name = name.strip().split("\n")[0].split("\r")[0]
	global last_sub_id
	sid = last_sub_id
	print("sid %s, pid %s, name %s" % (sid, pid, name))
	try:
		code_to_write = code
		utils.write_file(path_temp + "code.txt", code_to_write)
		utils.write_file(path_temp + "code_copy.txt", code_to_write)
		meta = name + "\n"
		meta += utils.get_current_time() + "\n"
		meta += pid + "\n"
		utils.write_file(path_temp + "meta.txt", meta)
		os.rename(path_temp + "meta.txt", path_metadata + "%d.txt" % sid)
		os.rename(path_temp + "code.txt", path_code + "%d.txt" % sid)
		os.rename(path_temp + "code_copy.txt", path_pending + "%d.txt" % sid)
		update_submission(sid)
		last_sub_id += 1
		lock.release()
		return sid
	except:
		lock.release()
		return None

def get_submission(sid):
	lock.acquire()
	ret = submissions.get(sid, None)
	lock.release()
	return ret


def get_board(pid):
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
			board_map[player_name] = [time_ms, sub["sid"], player_name, sub["submit_time"], sub["judge_time"]]
	board = []
	for i in board_map:
		board.append(board_map[i])
	board = sorted(board)[:100]
	lock.release()
	return board



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
	if not re.match(pass_regex, password):
		ret["error"] = "密码格式不正确！"
	
	lock.acquire()
	global users
	if users.get(username, None) != None:
		ret["error"] = "用户名已被使用！"
		lock.release()
		return ret
	user = {
		"username": username,
		"email": email,
		"password": password,
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
	]
	return a[randint(0, len(a) - 1)]





def init():
	lock.acquire()
	init_users()
	init_problems()
	init_submissions()
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

def update_submission(sid):
	name = path_result + "%d.txt" % sid
	res_str = utils.read_file(name)
	res_arr = res_str.split("\n")
	ok1 = False
	ok2 = False
	time_ms = None
	time_ms_prefix = "time_ms = "
	time_ms_prefix_len = len(time_ms_prefix)
	#code_content = read_file("code/%d.txt" % id)
	#code_first_row = code_content.split("\n")[0]
	
	metadata_content = utils.read_file(path_metadata + "%d.txt" % sid).split("\n")
	player_name = "咕咕咕"
	submit_time = "不存在的"
	pid = ""
	try:
		player_name = metadata_content[0]
		submit_time = metadata_content[1]
		pid = metadata_content[2]
	except:
		return
	
	#if code_first_row[:len(name_magic)] == name_magic:
	#	player_name = code_first_row[len(name_magic):]
	
	sub = {
		"sid": sid,
		"pid": pid,
		"status": "Pending",
		"time": 1e100,
		"time_text": "NaN",
		"name": player_name,
		"submit_time": submit_time,
		"judge_time": utils.get_file_mtime(path_result + "%d.txt" % sid, "")
	}
	
	if res_str != "":
		sub["status"] = "Judge Failed"
	
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
	if ok1 and ok2 and time_ms != None:
		if time_ms > 0 and time_ms < 100 * 1000:
			sub["status"] = "Accepted"
	if ok2 and (not ok1):
		sub["status"] = "Wrong Answer"
	global submissions
	submissions[sid] = sub









init()
