# -*- coding: utf-8 -*-
"""修正弹窗来源/呈现文案以匹配本项目实际素材来源"""
p = r'C:\Users\林绎客\AppData\Local\Doubao\User Data\Default\.doubao\agent_mode\workspace\holo-card-project\web\index.html'
with open(p, encoding='utf-8') as f:
    s = f.read()
for a, b in [
    ('<dd>用户提供的参考作品</dd>', '<dd>AI 生成素材 · 分层绘制</dd>'),
    ('<dd>个人艺术卡片习作</dd>', '<dd>3D 全息闪卡 · 山野典藏</dd>'),
]:
    assert a in s, a
    s = s.replace(a, b)
with open(p, 'w', encoding='utf-8') as f:
    f.write(s)
print('fixed')
