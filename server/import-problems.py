#encoding=utf-8

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

from server import jd_sql as sql
from server import jd_utils as utils

import markdown2

def add_problems():
	sql.begin()
	li = utils.list_dir(path_problems)
	for pid in li:
		if pid[:1] == ".":
			continue
		if not add_problem(pid):
			continue
	sql.commit()

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
		"hidden": 0,
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
			prob["hidden"] = 1
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
	
	prob["statement_html"] = markdown2.markdown(prob["statement"])
	
	p = prob
	
	sql.query(
		"insert into `problems` (`pid`, `name`, `description`, `time_limit`, `memory_limit`, `statement`, `statement_html`, `sample_code`, `class`, `hidden`) values (?,?,?,?,?,?,?,?,?,?)",
		(p["pid"], p["name"], p["description"], p["time_limit"], p["memory_limit"], p["statement"], p["statement_html"], p["sample_code"], p["class"], p["hidden"])
	)
	
	return True

add_problems()
print("done")
