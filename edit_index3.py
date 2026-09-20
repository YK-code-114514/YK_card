# -*- coding: utf-8 -*-
"""index.html：主体大小范围扩到 40–400；新增「主体溢出」「拖拽模式」按钮。保持 CRLF。"""
p = r'C:\Users\林绎客\AppData\Local\Doubao\User Data\Default\.doubao\agent_mode\workspace\holo-card-project\web\index.html'
s = open(p, encoding='utf-8').read()

old_scale = '>主体大小<input id="layer-scale" type="range" min="50" max="200" step="1" value="100"'
new_scale = '>主体大小<input id="layer-scale" type="range" min="40" max="400" step="1" value="100"'
assert s.count(old_scale) == 1
s = s.replace(old_scale, new_scale)

# 在「主体大小」滑杆后插入两个按钮行
anchor = '        <label class="edit-row" for="layer-scale"\n          >主体大小<input id="layer-scale" type="range" min="40" max="400" step="1" value="100"\n        /></label>'
assert s.count(anchor) == 1, s.count(anchor)
buttons = '''        <div class="edit-row">
          <button id="layer-clip" type="button" class="edit-ghost">主体溢出：开</button>
          <button id="drag-mode" type="button" class="edit-ghost">拖拽：移动主体</button>
        </div>'''
s = s.replace(anchor, anchor + '\n' + buttons)

# 更新提示文案
old_hint = '分层与阴影参数实时生效；「保存」可导出当前画面。'
new_hint = '分层与阴影参数实时生效；「主体溢出」开启后可放大冲出卡面，「拖拽」切换为移动主体后可直接在卡面上拖动。'
assert s.count(old_hint) == 1
s = s.replace(old_hint, new_hint)

with open(p, 'w', encoding='utf-8', newline='') as f:
    f.write(s)
print('index.html updated')
