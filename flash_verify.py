# -*- coding: utf-8 -*-
"""验证闪光：帧间差异（动态闪烁）与开关差异。"""
from PIL import Image
import numpy as np, os

d = r"C:\Users\林绎客\AppData\Local\Doubao\User Data\Default\.doubao\agent_mode\workspace\holo-card-project\shots"

def load(name):
    return np.asarray(Image.open(os.path.join(d, name)).convert("RGB"), dtype=np.float32)

a = load("flash-on-2.png")   # t2
b = load("flash-on-3.png")   # t3
c = load("flash-off.png")    # flash off

def stats(x, y):
    diff = np.abs(x - y)
    return {
        "mean_abs": round(float(diff.mean()), 2),
        "p99": round(float(np.percentile(diff, 99)), 1),
        "max": round(float(diff.max()), 1),
        "changed_pct": round(float((diff.mean(2) > 12).mean()) * 100, 2),
    }

print("on2 vs on3 (动态闪烁):", stats(a, b))
print("on2 vs off (闪光开关):", stats(a, c))
print("on3 vs off:", stats(b, c))

# 差异位置分布（on2 vs off）——闪光应集中在主体区域（画面中部偏上）
diff = np.abs(a - c).mean(2)  # (H, W)
H, W = diff.shape
cy, cx = H // 2, W // 2
halves = {
    "subject-upper": diff[:cy].mean(),
    "subject-lower": diff[cy:].mean(),
    "bg-top": diff[:cy // 2].mean(),
}
for k, v in halves.items():
    print(k, round(float(v), 2))
