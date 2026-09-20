# -*- coding: utf-8 -*-
"""闪光默认强度 0.7 -> 0.8（app.js / index.html / editor.js 三处）。"""
p1 = r'C:\Users\林绎客\AppData\Local\Doubao\User Data\Default\.doubao\agent_mode\workspace\holo-card-project\web\app.js'
s = open(p1, encoding='utf-8').read()
assert 'uFlashIntensity: { value: 0.7 }' in s
s = s.replace('uFlashIntensity: { value: 0.7 }', 'uFlashIntensity: { value: 0.8 }')
open(p1, 'w', encoding='utf-8', newline='').write(s)

p2 = r'C:\Users\林绎客\AppData\Local\Doubao\User Data\Default\.doubao\agent_mode\workspace\holo-card-project\web\index.html'
s = open(p2, encoding='utf-8').read()
assert 'id="layer-flash" type="range" min="0" max="100" step="1" value="70"' in s
s = s.replace('id="layer-flash" type="range" min="0" max="100" step="1" value="70"',
              'id="layer-flash" type="range" min="0" max="100" step="1" value="80"')
open(p2, 'w', encoding='utf-8', newline='').write(s)

p3 = r'C:\Users\林绎客\AppData\Local\Doubao\User Data\Default\.doubao\agent_mode\workspace\holo-card-project\web\editor.js'
s = open(p3, encoding='utf-8').read()
assert 'Math.round((u.uFlashIntensity.value || 0.7) * 100)' in s
s = s.replace('Math.round((u.uFlashIntensity.value || 0.7) * 100)',
              'Math.round((u.uFlashIntensity.value || 0.8) * 100)')
open(p3, 'w', encoding='utf-8', newline='').write(s)
print('defaults -> 0.8 ok')
