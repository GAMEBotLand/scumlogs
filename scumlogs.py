# -*- coding: utf-8 -*-
# g-portal logs downloader for scum servers
# by scr developments

import json
import asyncio
from bs4 import BeautifulSoup
from aiocfscrape import CloudflareScraper
from configparser import SafeConfigParser
from datetime import datetime


def log(text):
    print('[%s] %s' % (datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'), text))

def help():
    print('\nPlease edit scumlogs.ini and include your g-portal credentials, use:')
    print('  email = yourgportalemail')
    print('  password = yourgportalpassword')
    print('  serverid = gportalserverid')
    print('  gportal_loc = com (for gportal international) or us (for gportal us)')
    print('  download_path = path to store your log files\n')


def load_configini():
    config = SafeConfigParser()
    with open('scumlogs.ini', 'r') as f:
        config.readfp(f)
    global configini
    configini = dict(config['GPORTAL'])


def save_configini():
    parser = SafeConfigParser()
    parser.add_section('GPORTAL')
    for key in configini.keys():
        parser.set('GPORTAL', key, configini[key])
    with open('scumlogs.ini', 'w') as f:
        parser.write(f)


async def read_logs():
    async with CloudflareScraper(loop=loop) as session2:
        try:
            log('connecting g-portal...')
            raw_response = await session2.get(URL_LOGIN)
            response = await raw_response.text()
            payload = {'_method': 'POST', 'login': configini['email'], 'password': configini['password'],
                       'rememberme': '1'}
            raw_response = await session2.post(URL_LOGIN, data=payload)
            response = await raw_response.text()
            raw_response = await session2.get(URL_LOGS)

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
                raw_response = await session2.post(URL_LOGS, data=payload)
                response = await raw_response.text()
                content = json.loads(response)
                lines = content["ExtConfig"]["content"].splitlines()
                filename = configini['downloads_path'] + id
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
            await session2.close()
            save_configini()
        except:
            log('error connecting, check connectivity and scumlogs.ini')
            help()


if __name__ == '__main__':

    values = ('email','password','serverid','gportal_loc','downloads_path','admin_file','admin_line','chat_file','chat_line','kill_file','kill_line','login_file','login_line','violations_file','violations_line')

    print('scumlogs v1.0, gets logs from gportal scum servers, scr developments')
    try:
        load_configini()
    except:
        global configini
        configini = {}
        for value in values:
            if value not in configini:
                configini[value] = ''
        save_configini()

    if configini['gportal_loc'] == 'com':
        loc = 'com'
    else:
        loc = 'us'
    URL_LOGIN = 'https://id2.g-portal.com/login?redirect=https://www.g-portal.{}/en/gportalid/login?'.format(loc)
    URL_LOGS = 'https://www.g-portal.{}/en/scum/logs/{}'.format(loc, configini['serverid'])

    loop = asyncio.get_event_loop()
    loop.run_until_complete(read_logs())
    loop.close()





