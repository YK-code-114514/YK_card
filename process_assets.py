# -*- coding: utf-8 -*-
"""把主体图抠成透明 PNG（去掉品红背景/白描边/水印），再由主体生成注册线稿。"""
from PIL import Image, ImageFilter
import numpy as np
import os

PROJ = r'C:\Users\林绎客\AppData\Local\Doubao\User Data\Default\.doubao\agent_mode\workspace\holo-card-project'
ASSETS = os.path.join(PROJ, 'assets')

def load_rgb(name):
    return np.array(Image.open(os.path.join(ASSETS, name)).convert('RGB')).astype(np.float32)

def save_rgba(name, rgb, alpha):
    out = np.dstack([rgb, alpha]).astype(np.uint8)
    Image.fromarray(out, 'RGBA').save(os.path.join(ASSETS, name))

# ---------- 1. 主体抠像 ----------
im = load_rgb('raw-subject.jpg')
H, W, _ = im.shape
# 品红参考色：取四边最外圈
border = np.concatenate([
    im[:10].reshape(-1, 3), im[-10:].reshape(-1, 3),
    im[:, :10].reshape(-1, 3), im[:, -10:].reshape(-1, 3)], axis=0)
mag = border.mean(axis=0)
print('magenta ref:', mag.round(1))
dist = np.sqrt(((im - mag) ** 2).sum(axis=2))

d0, d1 = 16.0, 55.0
alpha = np.clip((dist - d0) / (d1 - d0), 0.0, 1.0)
mask = (alpha * 255).astype(np.uint8)

# 白描边去除：从透明区洪泛连通近白像素 → 清除外部白色贴纸边（保留山体内部亮色）
from collections import deque
a8 = (alpha * 255).astype(np.uint8)
white = im.min(axis=2) > 215
transp = a8 < 60
reach = transp.copy()
q = deque()
for y in range(H):
    for x in range(W):
        if transp[y, x]:
            q.append((y, x))
while q:
    y, x = q.popleft()
    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        ny, nx = y + dy, x + dx
        if 0 <= ny < H and 0 <= nx < W and not reach[ny, nx] and white[ny, nx]:
            reach[ny, nx] = True
            q.append((ny, nx))
a = alpha.copy()
a[reach & white] = 0.0

# 形态学开运算去噪点（先腐蚀后膨胀）
am = (a * 255).astype(np.uint8)
am = np.array(Image.fromarray(am).filter(ImageFilter.MinFilter(5)).filter(ImageFilter.MaxFilter(5)))
a = am.astype(np.float32) / 255.0

# 边缘轻微羽化
a = np.array(Image.fromarray((a * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.0))).astype(np.float32) / 255.0
a = np.clip(a, 0, 1)

# 去掉最外圈 1px 残边（品红溢色）
a[0, :] = 0; a[-1, :] = 0; a[:, 0] = 0; a[:, -1] = 0

save_rgba('subject.png', im, a * 255)
sub = Image.open(os.path.join(ASSETS, 'subject.png'))
trans = (np.array(sub.getchannel('A')) < 16).mean()
solid = (np.array(sub.getchannel('A')) > 127).mean()
print('subject.png 透明占比 %.3f 实体占比 %.3f' % (trans, solid))

# 预览合成（白底 / 黑底）
white_bg = Image.new('RGBA', (W, H), (255, 255, 255, 255))
white_bg.alpha_composite(sub)
white_bg.convert('RGB').save(os.path.join(ASSETS, 'preview-subject-white.jpg'), quality=92)
black_bg = Image.new('RGBA', (W, H), (18, 18, 24, 255))
black_bg.alpha_composite(sub)
black_bg.convert('RGB').save(os.path.join(ASSETS, 'preview-subject-black.jpg'), quality=92)

# ---------- 2. 背景：原样转 PNG ----------
Image.open(os.path.join(ASSETS, 'raw-background.jpg')).convert('RGB').save(
    os.path.join(ASSETS, 'background.png'))

# ---------- 3. 线稿：主体轮廓 + 内部亮度边缘（与主体严格对齐） ----------
comp_bg = Image.new('RGBA', (W, H), (255, 255, 255, 255))
comp_bg.alpha_composite(sub)
comp = comp_bg.convert('L')
g = np.array(comp).astype(np.float32)
# 简单 Sobel 梯度幅值
gx = np.zeros_like(g); gy = np.zeros_like(g)
gx[:, 1:-1] = g[:, 2:] - g[:, :-2]
gy[1:-1, :] = g[2:, :] - g[:-2, :]
grad = np.sqrt(gx * gx + gy * gy)
# 阈值：边缘线（黑）
line = np.where(grad > 42, 0, 255).astype(np.uint8)
line = np.array(Image.fromarray(line).filter(ImageFilter.MinFilter(3)))  # 加粗暗线
# 只保留主体范围内（alpha 明显处），避免背景残影
amask = np.array(sub.getchannel('A')) > 30
line = np.where(amask, line, 255)
Image.fromarray(line).save(os.path.join(ASSETS, 'lineart.png'))
print('lineart.png 极值:', Image.open(os.path.join(ASSETS, 'lineart.png')).convert('L').getextrema())
print('done')
