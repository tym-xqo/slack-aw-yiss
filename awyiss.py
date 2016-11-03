#!/usr/bin/env/ python
# coding: utf-8

from flask import Flask
from flask_slack import Slack
import requests
import json
import threading


app = Flask(__name__)
slack = Slack(app)
app.add_url_rule('/', view_func=slack.dispatch)

# On GCE, we're using files mounted at /secret for
# incoming webhook URL and team token
# Or you can hard-code values in the except blocks below.
try:
    with open('/secret/hookurl', 'r') as hookf:
        url = hookf.read().strip()
except:
    url = ("https://hooks.slack.com/services/T02594HP0/B081REU01"
           "/PjOvu5UAGNgVKUTydc3GqS6L")  # <- fake ;)
try:
    with open('/secret/token', 'r') as tokenf:
        valid = tokenf.read().strip()
except:
    valid = "bZKQqL4qkCOORlwzJRAPAvNc"  # phony
try:
    with open('/secret/teamid', 'r') as teamf:
        team = teamf.read().strip()
except:
    team = "T02594HP0"  # phony


def get_awyiss(channel, resp_url, text):
    api_url = 'http://www.awyisser.com/api/generator'
    if text:
        inpt = text
    else:
        inpt = "bread crumbs"
    awyiss = requests.post(api_url, data={'phrase': inpt})
    awyiss = json.loads(awyiss.text)['link']

    username = 'AW YISS'

    payload = {'text': awyiss,
               'username': username,
               'icon_emoji': ':aw_yiss:',
               'channel': channel}
    requests.post(resp_url, data=json.dumps(payload))


@slack.command('awyiss', token=valid,
               team_id=team, methods=['POST'])
def awyiss(**kwargs):
    channel = kwargs.get('channel_id')
    inpt = kwargs.get('text')
    resp_url = kwargs.get('response_url')
    getter = threading.Thread(target=get_awyiss, args=(channel,
                                                       resp_url,
                                                       inpt))
    getter.start()
    return slack.response('one sec....')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
