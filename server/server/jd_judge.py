#encoding=utf-8

import time
import os
import subprocess
import threading
import re

from . import jd_htmldocs as htmldocs
from . import jd_database as db
from . import jd_utils as utils


judge_lock = threading.Lock()

def do_judge(sid):
	sub = db.do_get_submission(sid)
	if sub == None:
		print("咕咕咕咕咕咕，好像没有 %s 这条提交记录啊" % sid)
		return
	pid = sub["pid"]
	pinfo = db.do_get_problem_info(pid)
	if pinfo == None:
		print("咕咕咕咕咕，在测提交记录 %s 的函数，发现好像没有 %s 这道题啊" % (sid, pid))
		return
	code = utils.read_file(db.path_code + "%s.txt" % sid)
	language = sub["language"]
	code_file_name = "contestant.c"
	if language != "C":
		code_file_name = "contestant.cpp"
	ok = True
	if re.match('.*\#\s*include\s*"/dev/.*', " ".join(" ".join(code.split("\n")).split("\r"))):
		ok = False
		result = "咕咕咕，非常抱歉！您的代码有可能危害鸭子的生命安全，不予评测"
	if ok:
		fcode = open(code_file_name, "w")
		fcode.write(code)
		fcode.close()
		finput = open("input.txt", "w")
		input_content = utils.read_file(db.path_problems + "%s/input.txt" % pid)
		finput.write(input_content)
		finput.close()
		flib = open("tasklib.cpp", "w")
		flib.write(utils.read_file(db.path_problems + "%s/tasklib.cpp" % pid))
		flib.close()
		for filename in pinfo["files"]:
			f = open(filename, "w")
			f.write(utils.read_file(db.path_problems + ("%s/" % pid) + filename))
			f.close()
		TL = "%s" % pinfo["time_limit"]
		ML = "%s" % pinfo["memory_limit"]
		print("run tl = %s ml = %s lang = %s" % (TL, ML, language))
		try:
			cp = subprocess.run(["../judgesrv", TL, ML, language], stdout=subprocess.PIPE, timeout=20)
			result = str(cp.stdout, "utf-8")
			if result == "":
				result = "咕咕咕，评测机好像炸了"
		except:
			result = "咕咕咕，评测失败"
	print("result = %s" % result)
	fres = open(db.path_temp + "judge_res.txt", "w")
	fres.write(result)
	fres.close()
	os.rename(db.path_temp + "judge_res.txt", db.path_result + "%d.txt" % sid)
	db.update_submission(sid, utils.get_current_time())

def judge_server_thread_func():
	print("jd judge server started")
	while True:
		time.sleep(1)
		judge_lock.acquire()
		files = utils.list_dir(db.path_pending)
		min_id = -1
		for filename in files:
			if filename[-4:] == ".txt":
				id = utils.parse_int(filename[:-4], -1)
				if id != -1 and (min_id == -1 or id < min_id):
					min_id = id
		if min_id == -1:
			judge_lock.release()
			continue
		print("[jd] judging id = %d" % min_id)
		try:
			do_judge(min_id)
		except:
			print("[jd] judge failed !!!!!!!")
		print("[jd] judge done, id = %d" % min_id)
		try:
			os.remove(db.path_pending + "%d.txt" % min_id)
		except:
			pass
		judge_lock.release()




class myThread(threading.Thread):
	def __init__(self, name, func):
		threading.Thread.__init__(self)
		self.name = name
		self.func = func
	def run(self):
		self.func()

judge_server_thread = myThread("judgesrv", judge_server_thread_func)
judge_server_thread.start()
