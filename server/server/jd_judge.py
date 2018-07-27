#encoding=utf-8

import time
import os
import subprocess
import threading
import re
import uuid
import urllib.request, urllib.parse
import json
import base64

from . import jd_htmldocs as htmldocs
from . import jd_database as db
from . import jd_utils as utils

N_MAX_RUNNINGS = 20
PIGEON_URL = utils.read_file("pigeon-url.txt").split("\n")[0]

pendings = {}
runnings = {}
runnings_lock = threading.Lock()


def do_post(url, data_dict):
	while True:
		try:
			data = urllib.parse.urlencode(data_dict).encode()
			req = urllib.request.Request(url, data=data)
			res = urllib.request.urlopen(req)
			return res.read().decode('utf-8')
		except:
			time.sleep(1)



def do_send_problem_file(md5):
	res = do_post(PIGEON_URL + "api/query_file", {"md5": md5})
	try:
		res = json.loads(res)
	except:
		# The pigeon might has gone
		return
	if res["status"] == "success":
		return
	content = base64.b64encode(utils.read_file_b(db.path_problem_zips + md5))
	do_post(PIGEON_URL + "api/send_file", {"md5": md5, "content": content})

def do_send_contestant_files(code_file, language):
	utils.write_file(db.path_temp + "language.txt", language)
	contestant_filename = "contestant.cpp"
	if language == "C":
		contestant_filename = "contestant.c"
	utils.system("cp", [code_file, db.path_temp + contestant_filename])
	zip_filename = db.path_temp + "to_submit.zip"
	utils.system("rm", ["-rf", zip_filename])
	utils.system("zip", ["-j", zip_filename, db.path_temp + "language.txt", db.path_temp + contestant_filename])
	content_b = utils.read_file_b(zip_filename)
	md5 = utils.md5sum_b(content_b)
	content = base64.b64encode(content_b)
	do_post(PIGEON_URL + "api/send_file", {"md5": md5, "content": content})
	return md5

def do_submit_to_pigeon(sid):
	print("Submitting sid = %s" % sid)
	global pendings
	global runnings
	global runnings_lock
	try:
		priority = pendings[sid]
		del pendings[sid]
	except:
		priority = runnings[sid]["priority"]
	task_id = uuid.uuid1().hex
	sub = db.do_get_submission(sid)
	prob = db.do_get_problem_info(sub["pid"])
	task = {
		"task_id": task_id,
		"priority": priority,
		"sid": sid,
		"problem_md5": prob["md5"],
		"sub": sub,
		"language": sub["language"],
	}
	#do_send_problem_file(prob["md5"])
	task["contestant_md5"] = do_send_contestant_files(db.path_code + "%s.txt" % sid, sub["language"])
	res = do_post(PIGEON_URL + "api/submit_task", {
		"taskid": task["task_id"],
		"problem_md5": task["problem_md5"],
		"contestant_md5": task["contestant_md5"],
	})
	runnings_lock.acquire()
	runnings[sid] = task
	runnings_lock.release()

def judge_server_running_thread_func():
	global runnings
	global runnings_lock
	while True:
		time.sleep(1)
		runnings_lock.acquire()
		taskids = []
		tasks = []
		for sid in runnings:
			task = runnings[sid]
			taskids.append(task["task_id"])
			tasks.append(task)
		runnings_lock.release()
		if len(taskids) == 0:
			continue
		taskids_s = "|".join(taskids)
		res = do_post(PIGEON_URL + "api/get_task_results", {"taskids": taskids_s})
		try:
			res = json.loads(res)
		except:
			# gone
			continue
		if len(res) != len(taskids):
			continue
		print(json.dumps(res, indent=4, sort_keys=True))
		for i in range(len(res)):
			result = res[i]
			if result["status"] != "success":
				do_submit_to_pigeon(tasks[i]["sid"])
				continue
			result = result["result"]
			sub = tasks[i]["sub"]
			has_completed = result["has_completed"] == "true"
			db.update_sub_using_json(sub, result, has_completed)
			if has_completed:
				db.update_submission(sub["sid"], utils.get_current_time())
				utils.system("rm", ["-rf", db.path_pending + "%s.txt" % sub["sid"]])
				utils.system("rm", ["-rf", db.path_pending_rejudge + "%s.txt" % sub["sid"]])
				runnings_lock.acquire()
				del runnings[sub["sid"]]
				runnings_lock.release()

def judge_server_thread_func():
	global pendings
	global runnings
	global runnings_lock
	while True:
		time.sleep(0.2)
		runnings_lock.acquire()
		if len(runnings) >= N_MAX_RUNNINGS:
			runnings_lock.release()
			continue
		runnings_lock.release()
		files = utils.list_dir(db.path_pending)
		for filename in files:
			if filename[-4:] != ".txt": continue
			sid = utils.parse_int(filename[:-4], -1)
			if sid == -1: continue
			if runnings.get(sid, None) != None: continue
			if pendings.get(sid, None) != None: continue
			pendings[sid] = 50
		files = utils.list_dir(db.path_pending_rejudge)
		for filename in files:
			if filename[-4:] != ".txt": continue
			sid = utils.parse_int(filename[:-4], -1)
			if sid == -1: continue
			if runnings.get(sid, None) != None: continue
			if pendings.get(sid, None) != None: continue
			pendings[sid] = 30
		if len(pendings) == 0:
			continue
		max_sid = -1
		for sid in pendings:
			if (max_sid == -1) or (pendings[sid] > pendings[max_sid]):
				max_sid = sid
		if max_sid == -1:
			continue
		do_submit_to_pigeon(max_sid)



judge_lock = threading.Lock()


class myThread(threading.Thread):
	def __init__(self, name, func):
		threading.Thread.__init__(self)
		self.name = name
		self.func = func
	def run(self):
		self.func()

def start_thread_func():
	li = db.do_get_problem_list()
	for pid in li:
		pinfo = db.do_get_problem_info(pid)
		md5 = "judgeduck-problems/" + pid
		pinfo["md5"] = md5
		print("md5 of problem %s is %s" % (pid, md5))
	print("Starting judge server threads")
	judge_server_thread = myThread("judgesrv", judge_server_thread_func)
	judge_server_thread.start()
	judge_server_running_thread = myThread("judgesrv-running", judge_server_running_thread_func)
	judge_server_running_thread.start()

def start():
	start_thread = myThread("start-judgesrv", start_thread_func)
	start_thread.start()
