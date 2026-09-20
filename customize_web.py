# -*- coding: utf-8 -*-
"""定制 web 品牌文案：白相 → 闪卡工坊"""
base = r'C:\Users\林绎客\AppData\Local\Doubao\User Data\Default\.doubao\agent_mode\workspace\holo-card-project\web'

p1 = base + r'\index.html'
with open(p1, encoding='utf-8') as f:
    s = f.read()
for a, b in [
    ('白相 · White Atelier', '闪卡工坊 · Flash Card Atelier'),
    ('白相首页', '闪卡工坊首页'),
    ('白相', '闪卡工坊'),
    ('WHITE ATELIER', 'FLASH CARD ATELIER'),
    ('光影之间，自有回响。', '云海之上，自有回响。'),
    ('PERSONAL ART COLLECTION', 'PERSONAL HOLO CARD'),
]:
    s = s.replace(a, b)
with open(p1, 'w', encoding='utf-8') as f:
    f.write(s)

p2 = base + r'\app.bundle.js'
with open(p2, encoding='utf-8') as f:
    s = f.read()
s = s.replace(' · 白相', ' · 闪卡工坊')
with open(p2, 'w', encoding='utf-8') as f:
    f.write(s)
print('done; bundle 白相 remaining:', s.count('白相'))
