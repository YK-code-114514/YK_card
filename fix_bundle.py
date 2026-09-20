# -*- coding: utf-8 -*-
p = r'C:\Users\林绎客\AppData\Local\Doubao\User Data\Default\.doubao\agent_mode\workspace\holo-card-project\web\app.bundle.js'
with open(p, encoding='utf-8') as f:
    s = f.read()
old = 'backMark.textContent = "' + '\u767d\u76f8' + '";'
new = 'backMark.textContent = "' + '\u95ea\u5361\u5de5\u574a' + '";'
assert old in s
s = s.replace(old, new)
with open(p, 'w', encoding='utf-8') as f:
    f.write(s)
print('remaining 白相:', s.count('\u767d\u76f8'))
