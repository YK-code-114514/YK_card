# -*- coding: utf-8 -*-
"""将 __holo 里损坏的 THREE 引用替换为 makeCanvasTexture 工厂。"""
p = r'C:\Users\林绎客\AppData\Local\Doubao\User Data\Default\.doubao\agent_mode\workspace\holo-card-project\web\app.bundle.js'
with open(p, encoding='utf-8') as f:
    s = f.read()

old = '    THREE,'
new = '    makeCanvasTexture: (canvas) => new CanvasTexture(canvas),'
assert s.count(old) == 1, s.count(old)
s = s.replace(old, new)
with open(p, 'w', encoding='utf-8') as f:
    f.write(s)
print('makeCanvasTexture exposed')
