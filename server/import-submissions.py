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

import json

def add_submissions():
	sql.begin()
	n_subs = len(utils.list_dir(path_code))
	last_sub_id = n_subs
	for i in range(n_subs):
		update_submission(i)
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
	sub["saved"] = 1
	sub["detail"] = json.dumps(res,indent=4,sort_keys=True)

def update_submission(sid, new_judge_time = None):
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
		#if s == "hidden":
		#	if submissions.get(sid, None) != None:
		#		del submissions[sid]
		#	return
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
		"code": utils.read_file(path_code + "%d.txt" % sid),
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
	
	s = sub
	
	sql.query(
		"insert into `submissions` (`sid`, `pid`, `time`, `memory`, `score`, `code`, `code_length`, `submit_time`, `judge_time`, `player_name`, `language`, `status`, `status_short`, `detail`, `saved`) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
		(s["sid"], s["pid"], s["time"], s["memory"], s["score"], s["code"], s["code_length"], s["submit_time"], s["judge_time"], s["name"], s["language"], s["status"], s["status_short"], s["detail"], 1)
	)

add_submissions()
print("done")
