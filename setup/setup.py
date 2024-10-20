import requests
import json
from datetime import datetime
from threading import Thread

'''
This file is for generating the JSON files used by the program. Run to actualize data
'''

TOP_API_URL = "https://api.collegefootballdata.com/"  
URLS = {"team_stats.json" : "stats/season?year=", 
        "team_records.json" : "records?year=", 
        "talent.json" : "talent?year=", 
        "adv_stats.json" : "stats/season/advanced?year=", 
        "games.json" : "games?year="}
API_KEY = "Bearer Z6JXW74B3aWzTa+oz9V+Q6aBUlZ6ddi4VuL3MgrZkwByMONTQM4hIB5X/Vm4KiQU"
current_year = datetime.now().year
current_month = datetime.now().month
if current_month < 8:
    current_year -= 1

threads = []
headers = {'Authorization': API_KEY, 'accept': 'application/json'}

def get_jsons(name, url):
    response = requests.get(f"{TOP_API_URL}{url}{current_year}", headers=headers)
    with open(name, "w") as f:
        json.dump(response.json(), f, indent=4)

for name, url in URLS.items():
    threads.append(Thread(target=get_jsons, args=(name, url)))

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

print("Data updated")