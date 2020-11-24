#!/usr/bin/env python3

import requests
import json
import time

def send_slack_msg(account_id,apikey,url,acc_type,acc_js,swjs):
    webhook_url = 'https://hooks.slack.com/services/xxxxxxx'
    now = time.time()

    data = {'attachments': [
        {
            'color': 'danger',
            'fields': [
                {
                    'title': 'Account Alert :exclamation:',
                    'value': 'Account :       %s\nAPI-Key :       %s\nURL :              %s\nType :             %s\nJs :                  %s\nSw :                %s' % (account_id,apikey,url,acc_type,acc_js,swjs)
                }
            ],
                'footer': 'XXX API',
                'footer_icon': 'https://yyy.xxx.com/img/icon.png',
                'ts': '%s*' % now
            }
        ]
    }

    response = requests.post(webhook_url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
