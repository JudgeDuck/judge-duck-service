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

def add_users():
	sql.begin()
	li = utils.list_dir(path_users)
	for filename in li:
		if filename[-4:] != ".txt":
			continue
		username = filename[:-4]
		add_user(username)
	sql.commit()

def add_user(username):
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
	sql.query(
		"insert into `users` (`username`, `email`, `password`, `signature`, `language`) values (?,?,?,?,?)",
		(user["username"], user["email"], user["password"], user["signature"], user["language"])
	)

add_users()
print("done")
