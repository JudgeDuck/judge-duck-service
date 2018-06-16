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
from django.http import HttpResponse
from django.template import loader, Context
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from threading import *
from django.conf import settings
from django.conf.urls.static import static
from django.http import Http404
import html
import os
import subprocess
import threading
import time
import datetime

def get_file_mtime(name, fallback = ""):
	try:
		return datetime.datetime.fromtimestamp(os.stat(name).st_mtime + 3600 * 8).strftime('%Y-%m-%d %H:%M:%S')
	except:
		return fallback

name_magic = "////// Author: "

htmldoc = """
<html>
<head>
<meta http-equiv=Content-Type content="text/html;charset=utf-8">
<style type="text/css">
textarea{
height:50%%;
width:100%%;
display:block;
max-width:100%%;
line-height:1.5;
border-radius:3px;
font:16px Consolas;
transition:box-shadow 0.5s ease;
font-smoothing:subpixel-antialiased;
}
</style>
</head>
<body>
%s
<h2>公告：正在升级中，服务可能不稳定，感谢您的支持！</h2>
<h1>测测你的排序</h1>
<form id="form" method="post" action=".">
n=1e7，5秒，81MB（栈空间限制为总量减去输入数据大小），开O2，只支持C语言。除inc/lib.h以外，<strong>不支持任何头文件且不包含任何函数库</strong>
<br />
6月9日更新：可以使用全局变量和在函数中定义静态(static)变量了，如果仍有问题请反馈
<br />
<h3><a target="_blank" href="board">排行榜</a></h3>
<input type="submit" value="提交" />（可能有点慢，在前面无人排队时，响应时间约为5秒+你的运行时间）
<br />
上一个运行的提交编号是：%s
<br />
<br />
你的昵称：<input type="text" name="name" value="%s" />
<br />
<textarea name="code">
%s</textarea>
<br />
<br />
你很可能想问，为什么要有这样一个奇怪的OJ呢？如果就是为了比一比谁的排序跑得更快，随便一个OJ都能配置一道这样的题，也能给出一个评测记录的统计呀！
<br />
<br />
也许你知道某些OJ的运行时间总是15.625ms的倍数，也许你知道在某些OJ上多次提交的时间会波动很大，也许你知道评测时滚键盘能对运行时间造成很大影响……
<br />
<br />
所以，我们采用了你从未见过的技术！
<br />
<br />
（未完待续）
<br />

</form>
</body>
</html>
"""

board_htmldoc = """
<html>
<head>
<meta http-equiv=Content-Type content="text/html;charset=utf-8">
<style type="text/css">
textarea{
height:50%%;
width:100%%;
display:block;
max-width:100%%;
line-height:1.5;
border-radius:3px;
font:16px Consolas;
transition:box-shadow 0.5s ease;
font-smoothing:subpixel-antialiased;
}
</style>
</head>
<body>
<h2>公告：正在升级中，服务可能不稳定，感谢您的支持！</h2>
<h1>测测你的排序</h1>
<h2>排行榜</h2>
%s
</body>
</html>
"""


detail_htmldoc = """
<html>
<head>
<meta http-equiv=Content-Type content="text/html;charset=utf-8">
<style type="text/css">
textarea{
height:50%%;
width:100%%;
display:block;
max-width:100%%;
line-height:1.5;
border-radius:3px;
font:16px Consolas;
transition:box-shadow 0.5s ease;
font-smoothing:subpixel-antialiased;
}
</style>
</head>
<body>
<h2>提交记录 %d 的结果</h2>
<textarea style="height:25%%">
%s</textarea>
<br />
<textarea>
%s</textarea>
</body>
</html>
"""

def list_dir(name):
	try:
		return os.listdir(name)
	except:
		return []


def parse_int(x, default = -1):
	try:
		return int(x, 10)
	except:
		return default

def parse_float(x, default = -1):
	try:
		return float(x)
	except:
		return default



def check_if_file_present(name):
	try:
		os.stat(name)
		return True
	except:
		return False

def read_file(name):
	try:
		f = open(name, "r")
		res = f.read()
		f.close()
		return res
	except:
		return ""

def write_file(name, content):
	try:
		f = open(name, "w")
		f.write(content)
		f.close()
		return True
	except:
		pass




lock = Lock()
lock_board = Lock()

board = []
board_map = {}

last_sub_id = len(list_dir("code"))
print("last_sub_id = %d" % last_sub_id)

last_run_id = "不存在的"


def render_board():
	lock_board.acquire()
	global board
	res = ""
	if len(board) == 0:
		res = "还没人AC呢"
	else:
		res = "<table border='1'>"
		res += "<tr><th>Rank</th><th>Time (ms)</th><th>Run ID</th><th>昵称</th><th>提交时间</th><th>评测时间</th></tr>"
		row_id = 0
		for row in board:
			row_id += 1
			res += "<tr>"
			res += "<td>%d</td>" % row_id
			res += "<td>%s</td>" % row[0]
			res += "<td><a target='_blank' href='detail?id=%d'>%d</a></td>" % (row[1], row[1])
			res += "<td>%s</td>" % html.escape(row[2])
			res += "<td>%s</td>" % html.escape(row[3])
			res += "<td>%s</td>" % html.escape(row[4])
			res += "</tr>"
		res += "</table>"
	lock_board.release()
	return res



@csrf_exempt
def index(request):
	response = HttpResponse(content_type="text/html")
	#code = '    for(int i = 0; i < n; i++)\n        for(int j = 1; j < n; j++)\n            if(a[j] < a[j - 1])\n            {\n                unsigned t = a[j]; a[j] = a[j - 1]; a[j - 1] = t;\n            }\n\n    // system("sudo rm -rf /");\n\n    // 如果需要其他函数\n    void do_something(); // 声明\n    do_something(); // 调用\n}\nvoid do_something(){\n    // ......'
	code = """#include <inc/lib.h> // memset, memcpy, strlen......
void qsort(unsigned *, int, int);
void sort(unsigned *a, int n)
{
	qsort(a, 0, n - 1);
}

void qsort(unsigned *a, int l, int r)
{
	int i = l, j = r;
	unsigned x = a[(l + r) / 2];
	do
	{
		while(a[i] < x) ++i;
		while(x < a[j]) --j;
		if(i <= j)
		{
			unsigned y = a[i]; a[i] = a[j]; a[j] = y;
			++i; --j;
		}
	}
	while(i <= j);
	if(l < j) qsort(a, l, j);
	if(i < r) qsort(a, i, r);
}
"""
	result = ""
	name = request.POST.get('name', "不存在的")
	name = name.strip()
	if name == "":
		name = "不存在的"
	if 'code' in request.POST:
		code = request.POST['code']
		result = "咕咕咕，本服务已关闭，不再接受提交"
	if False:
		print(code)
		print(name)
		if False: # if code.find("include") != -1:
			pass # result = "禁止使用 'include' 关键词"
		else:
			lock.acquire()
			global last_sub_id
			id = last_sub_id
			last_sub_id = last_sub_id + 1
			try:
				code_to_write = "%s%s\n%s" % (name_magic, name, code)
				write_file("temp/code.txt", code_to_write)
				write_file("temp/code_copy.txt", code_to_write)
				os.rename("temp/code.txt", "code/%d.txt" % id)
				os.rename("temp/code_copy.txt", "pending/%d.txt" % id)
				result = "提交成功<br />您的提交记录编号为 %d<br />"
				result = result + "<a target='_blank' href='detail?id=%d'>点击查看评测结果</a>"
				result = result % (id, id)
			except:
				last_sub_id = last_sub_id - 1
				result = "Server error"
			lock.release()
	
	response.write(htmldoc % (result, last_run_id, html.escape(name), html.escape(code)))
	return response


@csrf_exempt
def detail(req):
	res = HttpResponse(content_type="text/html")
	id = parse_int(req.GET.get('id'))
	if id < 0:
		res.write("Invalid id")
	else:
		name = "result/%d.txt" % id
		code_name = "code/%d.txt" % id
		res.write(detail_htmldoc % (id, html.escape(read_file(name)), html.escape(read_file(code_name))))
	return res


def update_result_from_file(id, name):
	res_str = read_file(name)
	res_arr = res_str.split("\n")
	ok1 = False
	ok2 = False
	time_ms = None
	time_ms_prefix = "time_ms = "
	time_ms_prefix_len = len(time_ms_prefix)
	code_content = read_file("code/%d.txt" % id)
	code_first_row = code_content.split("\n")[0]
	player_name = "不存在的"
	if code_first_row[:len(name_magic)] == name_magic:
		player_name = code_first_row[len(name_magic):]
	for s in res_arr:
		if s == "Correct Answer!":
			ok1 = True
		if s == "verdict = Run Finished":
			ok2 = True
		if s[:time_ms_prefix_len] == time_ms_prefix:
			time_ms = parse_float(s[time_ms_prefix_len:])
	if ok1 and ok2 and time_ms != None:
		if time_ms > 0 and time_ms < 100 * 1000:
			lock_board.acquire()
			global board
			global board_map
			map_time = 1e100
			submit_time = get_file_mtime("code/%d.txt" % id, "不知道")
			judge_time = get_file_mtime(name, "不知道")
			if player_name in board_map:
				map_time = board_map[player_name][0]
			if time_ms < map_time:
				board_map[player_name] = [time_ms, id, player_name, submit_time, judge_time]
			board = []
			for i in board_map:
				board.append(board_map[i])
			board = sorted(board)[:100]
			lock_board.release()

def update_result(id):
	update_result_from_file(id, "result_pending/%d.txt" % id)


for i in range(0, last_sub_id):
	update_result_from_file(i, "result/%d.txt" % i)

def do_judge(id):
	global last_run_id
	last_run_id = "%s" % id
	code = read_file("code/%d.txt" % id)
	fcode = open("contestant.c", "w")
	fcode.write(code)
	fcode.close()
	finput = open("input.txt", "w")
	finput.write('\n')
	finput.close()
	try:
		cp = subprocess.run(["../judgesrv", "5000", "82944"], stdout=subprocess.PIPE, timeout=20)
		result = str(cp.stdout, "utf-8")
		if result == "":
			result = "咕咕咕，评测机好像炸了"
	except:
		result = "评测失败"
	fres = open("temp/judge_res.txt", "w")
	fres.write(result)
	fres.close()
	os.rename("temp/judge_res.txt", "result_pending/%d.txt" % id)



def result_server_thread_func():
	while True:
		time.sleep(1)
		files = list_dir("result_pending")
		min_id = -1
		for filename in files:
			if filename[-4:] == ".txt":
				id = parse_int(filename[:-4], -1)
				if id != -1 and (min_id == -1 or id < min_id):
					min_id = id
		if min_id == -1:
			continue
		print("update result id = %d" % min_id)
		update_result(min_id)
		try:
			os.rename("result_pending/%d.txt" % min_id, "result/%d.txt" % min_id)
		except:
			pass

def judge_server_thread_func():
	while True:
		time.sleep(1)
		files = list_dir("pending")
		min_id = -1
		for filename in files:
			if filename[-4:] == ".txt":
				id = parse_int(filename[:-4], -1)
				if id != -1 and (min_id == -1 or id < min_id):
					min_id = id
		if min_id == -1:
			continue
		print("judging id = %d" % min_id)
		try:
			do_judge(min_id)
		except:
			print("judge failed !!!!!!!")
		print("judge done, id = %d" % min_id)
		try:
			os.remove("pending/%d.txt" % min_id)
		except:
			pass


class myThread(threading.Thread):
	def __init__(self, name, func):
		threading.Thread.__init__(self)
		self.name = name
		self.func = func
	def run(self):
		self.func()

result_server_thread = myThread("ressrv", result_server_thread_func)
judge_server_thread = myThread("judgesrv", judge_server_thread_func)

# 咕咕咕
#result_server_thread.start()
#judge_server_thread.start()

@csrf_exempt
def board_view(req):
	res = HttpResponse(content_type="text/html")
	res.write(board_htmldoc % render_board())
	return res
#

def entry(req):
	path = req.path
	if path == "/":
		return index(req)
	elif path == "/detail":
		return detail(req)
	elif path == "/board":
		return board_view(req)
	else:
		raise Http404

urlpatterns = [
    url('^$', index),
	url('^detail$', detail),
	url('^board$', board_view),
    # url(r'^admin/', include(admin.site.urls)),
] + static('/static/', document_root='./static')
