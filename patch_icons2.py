# -*- coding: utf-8 -*-
"""修正归一化正则：-后跟数字也要去横线（rotate-3d -> Rotate3d）"""
p = r'C:\Users\林绎客\AppData\Local\Doubao\User Data\Default\.doubao\agent_mode\workspace\holo-card-project\web\app.bundle.js'
with open(p, encoding='utf-8') as f:
    s = f.read()

old = 'name.slice(1).replace(/-([a-z])/g, (m, c) => c.toUpperCase())'
new = 'name.slice(1).replace(/-([a-z0-9])/g, (m, c) => c.toUpperCase())'
assert s.count(old) == 1, s.count(old)
s = s.replace(old, new)
with open(p, 'w', encoding='utf-8') as f:
    f.write(s)
print('regex fixed')
