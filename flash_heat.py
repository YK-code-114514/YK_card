# -*- coding: utf-8 -*-
from PIL import Image
import numpy as np, glob, os

d = r"C:\Users\林绎客\AppData\Local\Doubao\User Data\Default\.doubao\agent_mode\workspace\holo-card-project\shots\flash-frames\full"
out = r"C:\Users\林绎客\AppData\Local\Doubao\User Data\Default\.doubao\agent_mode\workspace\holo-card-project\shots"
files = sorted(glob.glob(os.path.join(d, "*.jpg")))
H, W = 296, 480
arrs = [np.asarray(Image.open(f).convert("RGB").resize((W, H)), dtype=np.float32) for f in files]
stack = np.stack(arrs, axis=0)          # (F, H, W, 3)
lum = stack.mean(axis=-1)               # (F, H, W)
diff = lum.max(axis=0) - lum.min(axis=0)  # (H, W)
print("shapes", lum.shape, diff.shape, "mean", round(float(diff.mean()), 1), "max", round(float(diff.max()), 1))

hot = np.clip((diff - diff.mean()) / (diff.std() * 2 + 1e-6), 0, 2.2)
hot = np.clip(hot, 0.0, 1.0)
hmap = np.zeros((H, W, 3), dtype=np.uint8)
hmap[..., 0] = (255 * hot).astype(np.uint8)
hmap[..., 1] = (60 * hot).astype(np.uint8)
hmap[..., 2] = (20 * hot).astype(np.uint8)
Image.fromarray(hmap).save(os.path.join(out, "flash-heatmap.png"))
print("heat saved")

print("frame-to-frame:")
for i in range(len(files) - 1):
    dd = np.abs(lum[i + 1] - lum[i]).mean()
    print(" ", os.path.basename(files[i])[:4], "->", os.path.basename(files[i + 1])[:4], round(float(dd), 1))

print("vs frame0:")
base = lum[0]
for i, f in enumerate(files):
    dd = np.abs(lum[i] - base).mean()
    print(" ", os.path.basename(f)[:8], round(float(dd), 1))

# 分区差异：把画面切 4x4 块，输出每块 diff 均值，定位动画区域
import itertools
blocks = np.zeros((4, 4))
bh, bw = H // 4, W // 4
for r in range(4):
    for c in range(4):
        blocks[r, c] = diff[r * bh:(r + 1) * bh, c * bw:(c + 1) * bw].mean()
print("4x4 block diff map:")
for row in blocks:
    print(" ", [round(float(v), 1) for v in row])
