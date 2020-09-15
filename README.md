# scumlogs (for python v3.7)
scumlogs v1.0, gets logs from gportal scum servers, by https://gamebotland.com

is incremental, adds new lines to last updated files and create new ones from last execution

created to keep a backup of the server logs in local

run once to generate a new ini file, edit ini file and complete gportal data

when you access your gportal server you can see serverid value in url: https://www.g-portal.com/en/scum/status/XXXXXX

- for gportal international set: gportal_loc = com
- for gportal us set: gportal_loc = us

include in crontab or in windows task manager to run periodicaly

Now is included scumlogs GUI

Instructions

	Install python 3.7.4 on your system
	Download all files and decompress in a folder
		
	pip install -r requirements.txt
	
	Run scumlogs:
		python scumlogs.py
		
	Run gui with embeded scumlogs:
		python scumlogsgui.py
	


