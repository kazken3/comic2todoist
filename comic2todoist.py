#!/usr/bin/python3

import json
import urllib.request
import todoist
import os.path
import sys
import re
import configparser

config_ini = configparser.ConfigParser()
config_ini.read('config.ini', encoding='utf-8')

api_token = config_ini['DEFAULT']['API_TOKEN']
pid = config_ini['DEFAULT']['PROJECT_ID']

url = "https://books.rakuten.co.jp/event/book/comic/calendar/js/booklist.json"

if not os.path.isfile("./booklists.json"):
    file = open('booklists.json', 'w')
    try:
        with urllib.request.urlopen(url) as resp:
            file.write(resp.read().decode('utf-8'))
            file.close()
    except urllib.error.URLError as e:
        print(e.reason)
        sys.exit()


jf = open('./booklists.json', 'rb')
body = json.loads(jf.read())
len = len(body['list'])
with open('pattern.txt') as p:
    for line in p:
#        print(line)
        for num in range(len):
            if re.search(line.rstrip(), body['list'][num][5]):
#                print(body['list'][num])
                title = body['list'][num][5]
                eisbn = body['list'][num][3]
                date = body['list'][num][20]
                url = body['list'][num][24]
#                print(url)
                api = todoist.TodoistAPI(api_token)
                api.sync()
                task = api.items.add(title + " " + url, project_id=pid, due={"string": date})
                api.commit()
