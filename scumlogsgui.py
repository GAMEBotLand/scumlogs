# -*- coding: utf-8 -*-
# GUI g-portal logs downloader for scum servers
# by GAMEBotLand.com

import subprocess
import sys
import PySimpleGUI as sg
from configparser import ConfigParser


def load_configini(configini):
    try:
        config = ConfigParser()
        with open('scumlogs.ini', 'r') as f:
            config.read_file(f)
        configini = dict(config['GPORTAL'])
    except:
        configini = {}
    values = (
        'user', 'password', 'serverid', 'loc', 'folder', 'admin_file', 'admin_line', 'chat_file', 'chat_line',
        'kill_file',
        'kill_line', 'login_file', 'login_line', 'violations_file', 'violations_line')
    for value in values:
        if value not in configini:
            configini[value] = ''
    return configini


def save_configini(configini):
    parser = ConfigParser()
    parser.add_section('GPORTAL')
    for key in configini.keys():
        parser.set('GPORTAL', key, configini[key])
    with open('scumlogs.ini', 'w') as f:
        parser.write(f)

def main_gui():
    configini = {}
    configini = load_configini(configini)
    sg.ChangeLookAndFeel('Dark')
    sg.SetOptions(element_padding=(0, 0))
    layout = [[sg.Text("GAMEBotLand scumlogs v1.0")],
              [sg.Image(filename='scum.png', size=(455, 100), pad=((0, 0), (0, 0)))],
              [sg.Text("scum server logs downloader from G-Portal")],
              [sg.Frame(layout=[
                  [sg.Text('Username', size=(8, 1), justification='left'), sg.InputText(configini['user'], size=(30, 1), key='user')],
                  [sg.Text('Password', size=(8, 1), justification='left'),
                   sg.InputText(configini['password'], size=(30, 1), password_char='*', key='password')],
                  [sg.Text('Server id', size=(8, 1), justification='left'),
                   sg.InputText(configini['serverid'], size=(8, 1), key='serverid')],
                  [sg.Text('Folder', size=(8, 1), justification='left'), sg.InputText(configini['folder'], size=(40, 1), key='folder'),
                   sg.FolderBrowse()],

                  [sg.Radio('G-Portal international', "RADIO1", default=configini['loc'] == 'com', key='com', size=(18, 1)),
                   sg.Radio('G-Portal us', "RADIO1", default=configini['loc'] == 'us', key='us')]
              ], title='G-Portal server info', size=(200, 100))],
              [sg.Output(size=(62, 12), pad=((0, 0), (2, 0)), font='Sans 10')],
              [sg.Button('Start', size=(15, 1), bind_return_key=True, focus=True),
               sg.SimpleButton('Exit', size=(15, 1), button_color=('white', 'firebrick3')),
               sg.Text("GAMEBotLand.com", justification='right')]]

    window = sg.Window('GAMEBotLand scumlogs v1.0',
                       auto_size_text=False,
                       auto_size_buttons=False,
                       no_titlebar=True,
                       grab_anywhere=True,
                       size=(500, 800))
    window.Layout(layout)

    while True:
        event, values = window.Read(timeout=100)
        if event in (None, 'Exit'):
            break
        elif event == 'Start':
            print('started...')
            runCommand(configini, cmd='python scumlogs.py', timeout=100, window=window)
            #runCommand(configini, cmd='scumlogs.exe', timeout=100, window=window)
            print('finished...')
    window.Close()

def runCommand(configini, cmd, timeout=100, window=None):
    save_configini(configini)

    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = ''
    for line in p.stdout:
        line = line.decode(errors='replace' if (sys.version_info) < (3, 5) else 'backslashreplace').rstrip()
        output += line
        print(line)
        window.Refresh() if window else None
    retval = p.wait(timeout)
    return (retval, output)

if __name__ == '__main__':
    main_gui()
