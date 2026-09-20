# -*- coding: utf-8 -*-
"""在 bundle 的 window.__holo 上暴露 THREE，供 editor.js 使用。"""
p = r'C:\Users\林绎客\AppData\Local\Doubao\User Data\Default\.doubao\agent_mode\workspace\holo-card-project\web\app.bundle.js'
with open(p, encoding='utf-8') as f:
    s = f.read()

old = 'modelSource: config.assets.model,'
new = 'modelSource: config.assets.model,\n    THREE,'
assert s.count(old) == 1, s.count(old)
s = s.replace(old, new)
with open(p, 'w', encoding='utf-8') as f:
    f.write(s)
print('THREE exposed on window.__holo')
