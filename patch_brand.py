# -*- coding: utf-8 -*-
p = r'C:\Users\林绎客\AppData\Local\Doubao\User Data\Default\.doubao\agent_mode\workspace\holo-card-project\web\app.js'
s = open(p, encoding='utf-8').read()
a = 'config.title + " · 白相"'
b = 'backMark.textContent = "白相";'
assert s.count(a) == 1, s.count(a)
assert s.count(b) == 1, s.count(b)
s = s.replace(a, 'config.title + " · 闪卡工坊"')
s = s.replace(b, 'backMark.textContent = "闪卡工坊";')
open(p, 'w', encoding='utf-8', newline='').write(s)
print('app.js branding patched:', ' · 闪卡工坊' in s, '闪卡工坊";' in s)
