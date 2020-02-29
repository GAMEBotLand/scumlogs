# -*- coding: utf-8 -*-
# g-portal logs downloader for scum servers
# by GAMEBotLand.com

import json
import asyncio
from bs4 import BeautifulSoup
from aiocfscrape import CloudflareScraper
from configparser import RawConfigParser
from datetime import datetime

def log(text):
    print('[%s] %s' % (datetime.strftime(datetime.now(), '%H:%M:%S'), text))

def help():
    print('\nPlease edit scumlogs.ini and include your g-portal credentials, use:')
    print('  user = gportal email or username')
    print('  password = gportal password')
    print('  serverid = gportal server id')
    print('  loc = com (for gportal international) or us (for gportal us)')
    print('  folder = blank for local or path folder to store your log files')
    print('  leave the rest of the parameters as is\n')

def load_configini():
    config = RawConfigParser()
    with open('scumlogs.ini', 'r', encoding="utf-8") as f:
        config.read_file(f)
    global configini
    configini = dict(config['GPORTAL'])

def save_configini():
    parser = RawConfigParser()
    parser.add_section('GPORTAL')
    for key in configini.keys():
        parser.set('GPORTAL', key, configini[key])
    with open('scumlogs.ini', 'w', encoding="utf-8") as f:
        parser.write(f)


async def read_logs():
    values = ('user','password','serverid','loc','folder','admin_file','admin_line','chat_file','chat_line','kill_file','kill_line','login_file','login_line','violations_file','violations_line')
    print('scumlogs v1.0, scum server logs downloader from gportal\nby htttps://GAMEBotLand.com')
    try:
        load_configini()
    except:
        global configini
        configini = {}
    for value in values:
        if value not in configini:
            configini[value] = ''
    if configini['folder'] != '':
        if configini['folder'][-1:] != '/' and configini['folder'][-1:] != '\\':
            configini['folder'] = configini['folder'] + '/'
    save_configini()

    if configini['loc'] == 'com':
        loc = 'com'
    else:
        loc = 'us'
    URL_LOGIN = 'https://id2.g-portal.com/login?redirect=https://www.g-portal.{}/en/gportalid/login?'.format(configini['loc'])
    URL_LOGS = 'https://www.g-portal.{}/en/scum/logs/{}'.format(configini['loc'], configini['serverid'])
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'}
    
    async with CloudflareScraper() as session:
        try:
            log('connecting g-portal...')
            payload = {'_method': 'POST', 'login': configini['user'], 'password': configini['password'],
                       'rememberme': '1'}
            async with session.post(URL_LOGIN, headers=headers, data=payload) as raw_response:
                response = await raw_response.text()
            async with session.get(URL_LOGS, headers=headers) as raw_response:
                response = await raw_response.text()
            html = BeautifulSoup(response, 'html.parser')
            select = html.find('div', {'class': 'wrapper logs'})
            loglist = select['data-logs']
            logs = json.loads(loglist)

            for i in range(len(logs)):
                getid = logs["file_" + str(i + 1)]
                id = (getid[int(getid.find('Logs')) + 5:])
                type = id.split('_')[0]

                if configini[type + '_file'] != '':
                    if id < configini[type + '_file']:
                        continue
                payload = {'_method': 'POST', 'load': 'true', 'ExtConfig[config]': getid}
                async with session.post(URL_LOGS, headers=headers, data=payload) as raw_response:
                    response = await raw_response.text()
                content = json.loads(response)
                lines = content["ExtConfig"]["content"].splitlines()
                filename = configini['folder'] + id
                file = open(filename, "a+", encoding='utf-8')
                found = False
                writing = False
                for line in lines:
                    if id == configini[type + '_file'] and not found:
                        if line == configini[type + '_line']:
                            found = True
                            continue
                    else:
                        file.write(line + '\n')
                        writing = True
                if writing:
                    if found:
                        log('updating {}'.format(id))
                    else:
                        log('creating {}'.format(id))
                file.close()
                configini[type + '_file'] = id
                configini[type + '_line'] = lines[-1]

            save_configini()
        except:
            log('error connecting, check connectivity and scumlogs.ini')
            help()
        await session.close()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(read_logs())
    loop.close()
