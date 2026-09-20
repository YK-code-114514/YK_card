# -*- coding: utf-8 -*-
from PIL import Image
import os

base = r'C:\Users\林绎客\AppData\Local\Doubao\User Data\Default\.doubao\agent_mode\workspace\holo-card-project\shots'
a = Image.open(os.path.join(base, 'shadow-off.png')).convert('RGB')
b = Image.open(os.path.join(base, 'shadow-on45.png')).convert('RGB')
c = Image.open(os.path.join(base, 'shadow-on135.png')).convert('RGB')
print('sizes', a.size, b.size, c.size)

def diff(x, y):
    x = x.resize((400, 200))
    y = y.resize((400, 200))
    px = x.load(); py = y.load()
    s = 0; n = 0
    for i in range(400):
        for j in range(200):
            dx = px[i, j]; dy = py[i, j]
            s += abs(dx[0]-dy[0]) + abs(dx[1]-dy[1]) + abs(dx[2]-dy[2])
            n += 1
    return s / n

print('off vs on45 mean_abs_diff:', round(diff(a, b), 2))
print('on45 vs on135 mean_abs_diff:', round(diff(b, c), 2))
print('off vs on135 mean_abs_diff:', round(diff(a, c), 2))
