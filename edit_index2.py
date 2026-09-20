# -*- coding: utf-8 -*-
"""在 index.html 编辑弹窗中插入：主体图背景处理区块 + 分层与阴影区块。保持 CRLF。"""
p = r'C:\Users\林绎客\AppData\Local\Doubao\User Data\Default\.doubao\agent_mode\workspace\holo-card-project\web\index.html'
with open(p, encoding='utf-8') as f:
    s = f.read()

anchor = '      </section>\n      <section class="edit-block">\n        <h3>文字内容</h3>'
assert s.count(anchor) == 1, s.count(anchor)

addition = '''      <section class="edit-block" id="key-block" hidden>
        <h3>主体图背景处理</h3>
        <canvas
          id="subject-preview"
          width="256"
          height="384"
          title="点击预览图取背景色"
        ></canvas>
        <div class="edit-row">
          <button id="pick-bg" type="button" class="edit-ghost">吸管取背景色</button>
          <button id="key-reset" type="button" class="edit-ghost">恢复原图</button>
        </div>
        <label class="edit-row" for="key-tol"
          >容差<input id="key-tol" type="range" min="10" max="180" step="1" value="80"
        /></label>
        <p class="edit-hint">上传后自动以边缘主色抠除背景；点「吸管」后点击预览图上的背景色可重新取色，拖动容差微调抠除范围。透明 PNG 自动保留，无需抠图。</p>
      </section>
      <section class="edit-block">
        <h3>分层与阴影</h3>
        <label class="edit-row" for="layer-depth"
          >主体距离<input id="layer-depth" type="range" min="0" max="80" step="1" value="28"
        /></label>
        <label class="edit-row" for="layer-bgdepth"
          >背景距离<input id="layer-bgdepth" type="range" min="-60" max="20" step="1" value="-20"
        /></label>
        <label class="edit-row" for="layer-textdepth"
          >文字距离<input id="layer-textdepth" type="range" min="-50" max="50" step="1" value="0"
        /></label>
        <label class="edit-row" for="layer-scale"
          >主体大小<input id="layer-scale" type="range" min="50" max="200" step="1" value="100"
        /></label>
        <label class="edit-row" for="layer-shadowop"
          >阴影浓度<input id="layer-shadowop" type="range" min="0" max="100" step="1" value="45"
        /></label>
        <label class="edit-row" for="layer-shadowdepth"
          >阴影偏移<input id="layer-shadowdepth" type="range" min="0" max="15" step="1" value="2"
        /></label>
        <label class="edit-row" for="layer-shadowangle"
          >阴影角度<input id="layer-shadowangle" type="range" min="0" max="360" step="1" value="45"
        /></label>
        <p class="edit-hint">分层与阴影参数实时生效；「保存」可导出当前画面。</p>
      </section>
      <section class="edit-block">
        <h3>文字内容</h3>'''

s = s.replace(anchor, addition)

# 补充内联样式：预览图样式
style_old = '      .edit-hint {'
style_add = '''      #subject-preview {
        width: 150px;
        height: 225px;
        display: block;
        margin: 4px 0 10px;
        border: 1px dashed rgba(0, 0, 0, .25);
        border-radius: 8px;
        cursor: crosshair;
        background:
          repeating-conic-gradient(rgba(0,0,0,.06) 0% 25%, transparent 0% 50%) 50% / 14px 14px;
      }
      #subject-preview.picking {
        outline: 2px solid var(--accent, #b8860b);
        outline-offset: 2px;
      }
      .edit-hint {'''
if style_old in s and '#subject-preview {' not in s:
    s = s.replace(style_old, style_add, 1)

with open(p, 'w', encoding='utf-8', newline='') as f:
    f.write(s)
print('index.html updated')
