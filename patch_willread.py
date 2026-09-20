# -*- coding: utf-8 -*-
"""editor.js 所有 2d 上下文加 willReadFrequently（频繁 getImageData 读回）。"""
p = r'C:\Users\林绎客\AppData\Local\Doubao\User Data\Default\.doubao\agent_mode\workspace\holo-card-project\web\editor.js'
s = open(p, encoding='utf-8').read()
n = s.count('getContext("2d")')
s = s.replace('getContext("2d")', 'getContext("2d", { willReadFrequently: true })')
open(p, 'w', encoding='utf-8', newline='').write(s)
print('patched contexts:', n)
