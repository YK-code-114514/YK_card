# -*- coding: utf-8 -*-
"""修复 bundle 中 refreshIcons 的图标名大小写问题：
data-lucide 用小写 kebab 名（info/rotate-3d），ICON_TREES 键为 PascalCase（Info/Rotate3d）。
在查找失败时做 kebab->Pascal 归一化再查，动态切换（play/pause）也会随之生效。"""
p = r'C:\Users\林绎客\AppData\Local\Doubao\User Data\Default\.doubao\agent_mode\workspace\holo-card-project\web\app.bundle.js'
with open(p, encoding='utf-8') as f:
    s = f.read()

old = 'const tree = icons[name];'
new = ('const tree = icons[name] || icons[' +
       'name.charAt(0).toUpperCase() + name.slice(1).replace(/-([a-z])/g, (m, c) => c.toUpperCase())' +
       '];')
assert s.count(old) == 1, s.count(old)
s = s.replace(old, new)
with open(p, 'w', encoding='utf-8') as f:
    f.write(s)
print('patched refreshIcons')
