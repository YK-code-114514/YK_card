# -*- coding: utf-8 -*-
"""蒙太奇 + 动态差异热区图，用于理解闪光海报的动画区域。"""
from PIL import Image, ImageOps
import numpy as np, glob, os

d = r"C:\Users\林绎客\AppData\Local\Doubao\User Data\Default\.doubao\agent_mode\workspace\holo-card-project\shots\flash-frames\full"
out = r"C:\Users\林绎客\AppData\Local\Doubao\User Data\Default\.doubao\agent_mode\workspace\holo-card-project\shots"
files = sorted(glob.glob(os.path.join(d, "*.jpg")))
print(len(files), "frames")

# 1) 蒙太奇 3x4
cell_w = 400
cols, rows = 3, 4
mont = Image.new("RGB", (cell_w * cols, int(cell_w * 2368 / 3840) * rows), (20, 20, 20))
small = []
for i, f in enumerate(files):
    im = Image.open(f).convert("RGB")
    im.thumbnail((cell_w, cell_w * 2368 // 3840))
    small.append((im, os.path.basename(f)[:4]))
for idx, (im, name) in enumerate(small):
    r, c = divmod(idx, cols)
    mont.paste(im, (c * cell_w, r * im.height))
mont.save(os.path.join(out, "flash-montage.jpg"), quality=88)
print("montage saved", mont.size)

# 2) 动态差异热区：每像素取 12 帧亮度 max-min
arrs = []
for f in files:
    im = np.asarray(Image.open(f).convert("L").resize((480, 296)), dtype=np.float32)
    arrs.append(im)
stack = np.stack(arrs, axis=0)
diff = stack.max(0) - stack.min(0)
diff_img = Image.fromarray(np.clip(diff * 4, 0, 255).astype(np.uint8)).convert("RGB")
# 叠加到首帧上
base = Image.open(files[0]).convert("RGB").resize((480, 296))
overlay = Image.blend(base, diff_img, 0.6)
overlay.save(os.path.join(out, "flash-diffmap.jpg"), quality=90)
print("diffmap saved")
