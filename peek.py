# -*- coding: utf-8 -*-
s = open(r'C:\Users\林绎客\AppData\Local\Doubao\User Data\Default\.doubao\agent_mode\workspace\holo-card-project\web\index.html', encoding='utf-8').read()
i = s.find('id="save"')
print(repr(s[i - 120:i + 240]))
