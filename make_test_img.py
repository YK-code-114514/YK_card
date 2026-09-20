# -*- coding: utf-8 -*-
"""生成一张特征明显的测试上传图（红橙渐变 + 深色星形），用于浏览器实测上传功能。"""
from PIL import Image, ImageDraw

W, H = 1200, 1600
img = Image.new("RGB", (W, H))
px = img.load()
for y in range(H):
    t = y / H
    r = int(210 + 45 * t)
    g = int(90 - 30 * t)
    b = int(40 + 60 * t)
    for x in range(0, W, 1):
        px[x, y] = (r, g, b)
d = ImageDraw.Draw(img)
# 大五角星（中心偏左）
cx, cy, R = W * 0.42, H * 0.48, H * 0.30
import math
pts = []
for i in range(10):
    ang = -math.pi / 2 + i * math.pi / 5
    r = R if i % 2 == 0 else R * 0.42
    pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
d.polygon(pts, fill=(24, 24, 34))
# 底部文字条
d.rectangle([0, H - 150, W, H], fill=(255, 255, 255))
d.text((W / 2 - 220, H - 120), "TEST UPLOAD 2026", fill=(24, 24, 34))
out = r'C:\Users\林绎客\AppData\Local\Doubao\User Data\Default\.doubao\agent_mode\workspace\holo-card-project\assets\test-upload.jpg'
img.save(out, quality=92)
print('saved', out)
