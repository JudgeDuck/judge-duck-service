import os

def add(li, s):
	ret = []
	for x in li:
		ret.append(s + x)
	return ret

l = add(os.listdir("data/result/"), "data/result/") + add(os.listdir("result/"), "result/")

ac_count = 0
tle_count = 0

for name in l:
	f = open(name, "r")
	content = f.read()
	f.close()
	if content.find("Correct Answer!") >= 0:
		ac_count += 1
	if content.find("Time Limit") >= 0:
		tle_count += 1

print("ac_count %d, tle count %d" % (ac_count, tle_count))


