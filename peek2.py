# -*- coding: utf-8 -*-
import re
s = open(r'C:\Users\林绎客\AppData\Local\Doubao\User Data\Default\.doubao\agent_mode\workspace\holo-card-project\web\editor.js', encoding='utf-8').read()
for m in re.finditer(r'.{60}(showModal|dialog\.close|\.close\(\)).{40}', s):
    print(repr(m.group(0)))
print('--- index.html ---')
h = open(r'C:\Users\林绎客\AppData\Local\Doubao\User Data\Default\.doubao\agent_mode\workspace\holo-card-project\web\index.html', encoding='utf-8').read()
print('dialog count:', h.count('<dialog'), '| aside editor:', 'aside id="editor"' in h, '| close aside:', h.count('</aside>'))
