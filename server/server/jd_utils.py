import html
import os
import subprocess
import threading
import time
import datetime
import hashlib


def md5sum(s):
	return hashlib.md5(s.encode("utf-8")).hexdigest()

def md5sum_b(s):
	return hashlib.md5(s).hexdigest()

def system(name, args, timeout = 5):
	try:
		cp = subprocess.run([name] + args, stdout=subprocess.PIPE, timeout=timeout)
		return str(cp.stdout, "utf-8")
	except:
		return ""

def rename(name1, name2):
	try:
		os.rename(name1, name2)
	except:
		pass

def mkdir(name):
	try:
		# os.mkdir(name)
		os.makedirs(name, exist_ok=True)
	except:
		pass

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

def read_file(name, fallback = ""):
	try:
		f = open(name, "r")
		res = f.read()
		f.close()
		return res
	except:
		return fallback

def read_file_b(name, fallback = b""):
	try:
		f = open(name, "rb")
		res = f.read()
		f.close()
		return res
	except:
		return fallback

def write_file(name, content):
	try:
		f = open(name, "w")
		f.write(content)
		f.close()
		return True
	except:
		pass

def write_file_b(name, content):
	try:
		f = open(name, "wb")
		f.write(content)
		f.close()
		return True
	except:
		pass

def get_file_mtime(name, fallback = ""):
	try:
		return datetime.datetime.fromtimestamp(os.stat(name).st_mtime + 3600 * 8).strftime('%Y-%m-%d %H:%M:%S')
	except:
		return fallback

def get_current_time():
	return datetime.datetime.fromtimestamp(time.time() + 3600 * 8).strftime('%Y-%m-%d %H:%M:%S')


def render_time_ns(tl):
	tl = int(tl + 0.5)
	res = "NaN "
	if tl >= 1e9:
		res = "%.3f s" % (tl * 1e-9)
	elif tl >= 1e6:
		res = "%.3f ms" % (tl * 1e-6)
	elif tl >= 1e3:
		res = "%.2f us" % (tl * 1e-3)
	else:
		res = "%.1f ns" % tl
	res1 = res.split(" ")
	res = res1[0]
	while res[-1] == "0":
		res = res[:-1]
	if res[-1] == ".":
		res = res[:-1]
	return res + " " + res1[1]

def render_memory_kb(ml):
	if ml < 1024:
		return "%s KB" % ml
	elif ml % 1024 == 0:
		return "%s MB" % (ml >> 10)
	else:
		return "%s MB + %s KB" % (ml >> 10, ml % 1024)

def render_time_ms(t):
	return render_time_ns(t * 1e6)

def render_code_length(l):
	if l < 1024:
		return "%s B" % l
	else:
		return "%.2f KB" % (l / 1024.0)
