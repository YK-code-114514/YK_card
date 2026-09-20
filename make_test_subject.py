# -*- coding: utf-8 -*-
"""白底测试主体图：深蓝山影 + 浅蓝灰雪顶 + 金色细节 + 红色圆点，全部远离白色背景。"""
from PIL import Image, ImageDraw, ImageFilter

W, H = 1200, 1600
im = Image.new("RGB", (W, H), (246, 248, 250))
d = ImageDraw.Draw(im)

# 深蓝山形剪影（主体），底部左右留白角
mountain = [(W * 0.06, H * 0.97), (W * 0.10, H * 0.60), (W * 0.22, H * 0.48),
            (W * 0.34, H * 0.66), (W * 0.50, H * 0.40), (W * 0.66, H * 0.70),
            (W * 0.82, H * 0.46), (W * 0.94, H * 0.58), (W * 0.94, H * 0.97)]
d.polygon(mountain, fill=(52, 68, 92))

# 浅蓝灰雪顶（远离背景色，不会被误抠）
d.polygon([(W * 0.42, H * 0.45), (W * 0.50, H * 0.40), (W * 0.57, H * 0.48),
           (W * 0.54, H * 0.54), (W * 0.46, H * 0.53)], fill=(160, 180, 210))

# 金色细节条
d.rectangle([W * 0.20, H * 0.68, W * 0.44, H * 0.695], fill=(232, 180, 96))
d.rectangle([W * 0.20, H * 0.70, W * 0.34, H * 0.715], fill=(232, 180, 96))

# 红色圆点
d.ellipse([W * 0.70, H * 0.62, W * 0.80, H * 0.72], fill=(214, 92, 80))

# 底部浅金色横条（主题装饰，非白背景）
d.rectangle([W * 0.30, H * 0.86, W * 0.70, H * 0.87], fill=(228, 214, 178))

im = im.filter(ImageFilter.GaussianBlur(0.5))
im.save(r"C:\Users\林绎客\AppData\Local\Doubao\User Data\Default\.doubao\agent_mode\workspace\holo-card-project\assets\test-subject-bg.jpg", quality=92)
im.save(r"C:\Temp\hcard\test-subject-bg.jpg", quality=92)
print("saved", im.size)
