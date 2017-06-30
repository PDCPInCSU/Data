# -*- coding: utf-8 -*-

import urllib2
import re

request = urllib2.Request("http://tieba.baidu.com/f?kw=中南大学")

response = urllib2.urlopen(request)

# print response.read()

patternString = r'tieba\.baidu\.com/p/\d+"'

pattern = re.compile(patternString)

result = re.findall(pattern, response.read())

print result
