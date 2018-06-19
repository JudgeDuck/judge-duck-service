import os
import datetime

def get_file_mtime(name, fallback = ""):
	try:
		return datetime.datetime.fromtimestamp(os.stat(name).st_mtime + 3600 * 8).strftime('%Y-%m-%d %H:%M:%S')
	except:
		return fallback

for name in os.listdir("jd_data/metadata/"):
	filename = "jd_data/metadata/" + name
	f = open(filename, "r")
	s = f.read().split("\n")
	f.close()
	jtime = get_file_mtime("jd_data/result/" + name, None)
	content = "player_name %s\nsubmit_time %s\npid %s\n" % (s[0], s[1], s[2])
	if jtime != None:
		content += "judge_time %s\n" % jtime
	f = open(filename, "w")
	f.write(content)
	f.close()
