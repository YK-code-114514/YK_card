# -*- coding: utf-8 -*-
import re
s = open(r'C:\Users\林绎客\AppData\Local\Doubao\User Data\Default\.doubao\agent_mode\workspace\holo-card-project\web\index.html', encoding='utf-8').read()
for m in re.finditer(r'<(dialog|aside|section|main|div)[^>]*id="([^"]+)"[^>]*>', s):
    print(m.group(1), '->', m.group(2))
print('---- dialog head ----')
i = s.find('<dialog')
print(s[i:i + 400])
print('---- dialog close ----')
j = s.find('</dialog>')
print(s[j - 200:j + 20])
print('---- editor.js editor refs ----')
e = open(r'C:\Users\林绎客\AppData\Local\Doubao\User Data\Default\.doubao\agent_mode\workspace\holo-card-project\web\editor.js', encoding='utf-8').read()
for m in re.finditer(r'.{90}(editor|close-editor|showModal|\.open|\.close\(\)).{70}', e):
    print(repr(m.group(0)))
