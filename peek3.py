# -*- coding: utf-8 -*-
import re
s = open(r'C:\Users\林绎客\AppData\Local\Doubao\User Data\Default\.doubao\agent_mode\workspace\holo-card-project\web\app.bundle.js', encoding='utf-8').read()
i = s.find('var ICON_TREES')
if i < 0:
    i = s.find('ICON_TREES = {')
start = s.find('{', i)
# 括号配平
depth = 0
j = start
while j < len(s):
    if s[j] == '{':
        depth += 1
    elif s[j] == '}':
        depth -= 1
        if depth == 0:
            break
    j += 1
obj = s[start:j + 1]
keys = re.findall(r'^\s{0,4}"?([A-Za-z0-9]+)"?\s*:', obj, re.M)
print('full keys:', sorted(set(keys)))
print('len', len(obj))
