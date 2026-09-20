# -*- coding: utf-8 -*-
"""index.html 容差默认值 80 -> 55"""
p = r'C:\Users\林绎客\AppData\Local\Doubao\User Data\Default\.doubao\agent_mode\workspace\holo-card-project\web\index.html'
s = open(p, encoding='utf-8').read()
s = s.replace('id="key-tol" type="range" min="10" max="180" step="1" value="80"',
              'id="key-tol" type="range" min="10" max="180" step="1" value="55"')
open(p, 'w', encoding='utf-8', newline='').write(s)
print('tol default:', 'value="55"' in s)
