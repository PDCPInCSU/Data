# -*- coding: utf-8 -*-

import urllib2
import re

request = urllib2.Request("http://tieba.baidu.com/p/5181822218")

response = urllib2.urlopen(request)

print response.read()


test = ""

patternString = r'tieba\.baidu\.com/p/\d+"'

pattern = re.compile(patternString)

# result = re.findall(pattern, )

# print result
