#encoding=utf-8

import sqlite3
import threading

lock = threading.Lock()

operation_lock = threading.Lock()
operation_lock.acquire()

result_lock = threading.Lock()
result_lock.acquire()

has_modifications = False

operation = None
result = None

has_error = False

class myThread(threading.Thread):
	def __init__(self, name, func):
		threading.Thread.__init__(self)
		self.name = name
		self.func = func
	def run(self):
		self.func()

def sql_thread_func():
	conn = sqlite3.connect('jd.sqlite3', isolation_level = None)
	conn.row_factory = sqlite3.Row
	conn.execute("PRAGMA temp_store = MEMORY")
	cur = conn.cursor()
	while True:
		global operation_lock
		global operation
		global result_lock
		global result
		global has_error
		operation_lock.acquire()
		result = None
		try:
			if operation != None:
				type = operation["type"]
				op = None
				params = ()
				if type == "begin":
					op = "begin"
				elif type == "commit":
					op = "commit"
				elif type == "rollback":
					op = "rollback"
				elif type == "query":
					op = operation["statement"]
					params = operation["parameters"]
				cur.execute(op, params)
				result = cur.fetchall()
		except Exception as e:
			has_error = True
			print(e)
		result_lock.release()

print("Starting SQL thread")
sql_thread = myThread("sql-thread", sql_thread_func)
sql_thread.start()

def do_operation(op):
	global operation_lock
	global operation
	global result_lock
	global result
	operation = op
	operation_lock.release()
	result_lock.acquire()
	return result


def begin():
	lock.acquire()
	global has_modifications
	has_modifications = False

def query(statement, parameters = ()):
	global has_modifications
	if (not has_modifications) and (statement[:6].lower() != "select"):
		has_modifications = True
		do_operation({
			"type": "begin",
		})
	return do_operation({
		"type": "query",
		"statement": statement,
		"parameters": parameters,
	})

def query_value(statement, parameters = ()):
	try:
		return query(statement, parameters)[0][0]
	except:
		return None

def commit():
	global has_modifications
	if has_modifications:
		do_operation({
			"type": "commit",
		})
		has_modifications = False
	end()

def rollback():
	global has_modifications
	if has_modifications:
		do_operation({
			"type": "rollback",
		})
		has_modifications = False
	end()

def end():
	global has_modifications
	if has_modifications:
		rollback()
		return
	lock.release()
