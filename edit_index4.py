# -*- coding: utf-8 -*-
"""index.html：闪光开关按钮 + 闪光强度/密度/速度三滑杆；edit-btns 改为自适应列。保持 CRLF。"""
p = r'C:\Users\林绎客\AppData\Local\Doubao\User Data\Default\.doubao\agent_mode\workspace\holo-card-project\web\index.html'
s = open(p, encoding='utf-8').read()

# 1) edit-btns 自适应换行
old_css = '''      .edit-btns {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 10px;
        margin: 8px 0;
      }'''
new_css = '''      .edit-btns {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(118px, 1fr));
        gap: 10px;
        margin: 8px 0;
      }'''
assert s.count(old_css) == 1
s = s.replace(old_css, new_css)

# 2) 按钮行加闪光开关
old_btns = '''        <div class="edit-btns">
          <button id="layer-clip" type="button" class="edit-ghost">主体溢出：关</button>
          <button id="drag-mode" type="button" class="edit-ghost">拖拽：旋转卡片</button>
        </div>'''
new_btns = '''        <div class="edit-btns">
          <button id="layer-clip" type="button" class="edit-ghost">主体溢出：关</button>
          <button id="drag-mode" type="button" class="edit-ghost">拖拽：旋转卡片</button>
          <button id="flash-toggle" type="button" class="edit-ghost">闪光：开</button>
        </div>'''
assert s.count(old_btns) == 1
s = s.replace(old_btns, new_btns)

# 3) 阴影角度行后插入三个闪光滑杆（放在阴影浓度之前，作为一组）
anchor = '''          >阴影浓度<input id="layer-shadowop" type="range" min="0" max="100" step="1" value="45"
        /></label>'''
assert s.count(anchor) == 1
sliders = '''        <label class="edit-row" for="layer-flash"
          >闪光强度<input id="layer-flash" type="range" min="0" max="100" step="1" value="70"
        /></label>
        <label class="edit-row" for="layer-flashsize"
          >闪光密度<input id="layer-flashsize" type="range" min="30" max="250" step="1" value="100"
        /></label>
        <label class="edit-row" for="layer-flashspeed"
          >闪光速度<input id="layer-flashspeed" type="range" min="0" max="200" step="1" value="100"
        /></label>
        <label class="edit-row" for="layer-shadowop"
          >阴影浓度<input id="layer-shadowop" type="range" min="0" max="100" step="1" value="45"
        /></label>'''
s = s.replace(anchor, sliders)

# 4) 提示文案更新
old_hint = '分层与阴影参数实时生效；「主体溢出」开启后可放大冲出卡面，「拖拽」切换为移动主体后可直接在卡面上拖动。'
new_hint = '分层与阴影参数实时生效；「主体溢出」开启后可放大冲出卡面，「拖拽」切换为移动主体后可直接在卡面上拖动，「闪光」为卡面叠加动态星芒与扫光。'
assert s.count(old_hint) == 1
s = s.replace(old_hint, new_hint)

with open(p, 'w', encoding='utf-8', newline='') as f:
    f.write(s)
print('index.html updated')
