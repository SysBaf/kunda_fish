import os
import json
import platform
import requests as req
from bs4 import BeautifulSoup


print('''
----------------------------
++++	KunFish V. 1.0	++++
++++	By @SysBaf   	++++
++++	              	++++
++++	  2023 year   	++++
----------------------------

Check git repo, for more info > https://github.com/SysBaf/kunda_fish/
''')


def create_prof():
	l = input("Enter login form kundalik.com: ")
	p = input("Now enter password: ")

	f = open("ldata.res", 'w', encoding='utf-8')
	f.write(str(l) + "<|%|>" + str(p))
	f.close()

try:
	f = open("ldata.res", 'r', encoding='utf-8')
	res = f.read()
	f.close()
except FileNotFoundError:
	print("[INF] Can't find account data file (ldata.res). Need to create a profile!")
	create_prof()
	os.system("python " + __file__)
	exit()

try:
	l, p = res.split("<|%|>")
except:
	print("[ERR] Can't split login data correctly!")
	create_prof()
	os.system("python " + __file__)
	exit()


r = req.Session()
r.post('https://login.kundalik.com/login', data={'exceededAttempts': "False", 'ReturnUrl': "", 'login': l, 'password': p, 'Captcha.Input': "", 'Captcha.Id': "5159ba49-6a5b-4aa2-a447-03844fc973f9"})


def get_recent_marks_list():
	page = r.get("https://kundalik.com/userfeed")

	soup = BeautifulSoup(page.text, "html.parser")
	marks_cont = soup.find_all("script")

	for i in marks_cont:
		ts = "__USER__START__PAGE__INITIAL__STATE__"
		ts2 = "partnersRecommendationExperiments\":[]};"
		data = str(i)
		if ts in data:
			sp = data.find(ts)
			ep = data.find(ts2)
			_json_naked = data[sp:ep+len(ts2)]
			json_naked = _json_naked[len(ts)+3:-1]


	js_pr = json.loads(json_naked)

	for i in js_pr['userMarks']['children'][0]['marks']:
		print("--------------------------------")
		print("Subject name:" + i['subject']['name'])
		print("For what: " + i['markTypeText'])
		print("MARK: " + i['marks'][0]['value'])
		print("--------------------------------\n")



def get_all_marks_list(sub=''):
	r.get("https://schools.kundalik.com/marks.aspx?school=1000000248306&tab=week")
	head = {"Referer": "https://schools.kundalik.com/marks.aspx?school=1000000248306&tab=week"}
	page = r.get("https://schools.kundalik.com/marks.aspx?school=1000000248306&index=1&tab=period&homebasededucation=False", headers=head)

	soup = BeautifulSoup(page.text, "html.parser")

	table = soup.find("table")
	trs = table.findAll("tr")

	info = []

	for j in range(2, len(trs)-1, 1):
		inx = 0
		data = trs[j].findAll("td")
		subj = data[1].find("strong").text

		# print("Name: " + str(subj) + "\nMarks: ") #- DEBUG

		_subj = str(subj)

		if _subj[0] == (" " or "\n" or "\t" or "\r"):
			_subj = subj[1:len(subj)]
		elif _subj[len(_subj)-1]  == (" " or "\n" or "\t" or "\r"):
			_subj = subj[0:len(subj)-2]

		info.append(dict({'subj': str(_subj), 'data': []}))

		for i in data[2].findAll("span"):
			mark = i.text
			what = i.attrs['title']

			info[len(info)-1]['data'].append({'for_what': what, 'mark': mark})

			# print("For what: " + what + "  Mark: " + mark) #- DEBUG

		if sub != ("" or " "):
			if sub.lower() in info[len(info)-1]['subj'].lower():
				print("[INF] FOUND! Subject: " + sub.lower())
				return info[len(info)-1]

	if sub != ("" or " "):
		print("[ERR] Failed to find this subj > " + sub)
	
	return info



# Try this:
# print(get_all_marks_list(""))
# print()
# print(get_recent_marks_list())