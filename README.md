# scumlogs
g-portal logs downloader for scum servers

is incremental, adds new lines to last updated files and create new ones from last execution

created to keep a backup of the server logs in local

run once to generate a new ini file
edit ini file and complete gportal data

when you access your gportal server you can see serverid value in url:
  https://www.g-portal.com/en/scum/status/XXXXXX

for gportal international set:
  gportal_loc = eu
 
for gportal us set:
  gportal_loc = us

include in crontab or in windows task manager to run periodicaly


