# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import json
import requests


NER_URL = 'http://api.bosonnlp.com/ner/analysis'


s = ['北京']
data = json.dumps(s)
headers = {'X-Token': 'RT22z3DL.13450.vPiFD1J5MM6r'}
resp = requests.post(NER_URL, headers=headers, data=data.encode('utf-8'))


for item in resp.json():
    for entity in item['entity']:
        print(''.join(item['word'][entity[0]:entity[1]]), entity[2])