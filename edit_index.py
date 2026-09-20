# -*- coding: utf-8 -*-
"""向 web/index.html 添加上传/编辑按钮、编辑弹窗、样式与脚本引用"""
p = r'C:\Users\林绎客\AppData\Local\Doubao\User Data\Default\.doubao\agent_mode\workspace\holo-card-project\web\index.html'
raw = open(p, 'rb').read()
crlf = b'\r\n' in raw
s = raw.decode('utf-8')
if crlf:
    s = s.replace('\r\n', '\n')

# 1) 头部 actions 追加"上传与编辑"按钮
old_actions = '''        <button
          class="icon-button save-button"
          id="save"
          aria-label="保存卡片图片"
          title="保存卡片图片"
          disabled
        >
          <i data-lucide="download"></i>
        </button>
      </div>'''
new_actions = '''        <button
          class="icon-button save-button"
          id="save"
          aria-label="保存卡片图片"
          title="保存卡片图片"
          disabled
        >
          <i data-lucide="download"></i>
        </button>
        <button
          class="icon-button"
          id="edit"
          aria-label="上传图片与编辑文字"
          title="上传图片与编辑文字"
          disabled
        >
          <svg
            viewBox="0 0 24 24"
            width="20"
            height="20"
            fill="none"
            stroke="currentColor"
            stroke-width="1.5"
            stroke-linecap="round"
            stroke-linejoin="round"
            aria-hidden="true"
          >
            <path d="M12 20h9" />
            <path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4Z" />
          </svg>
        </button>
      </div>'''
assert s.count(old_actions) == 1, 'actions anchor'
s = s.replace(old_actions, new_actions)

# 2) 编辑弹窗（插在 about 弹窗前）
editor_dialog = '''    <dialog id="editor" aria-labelledby="editor-title">
      <button
        id="close-editor"
        class="icon-button modal-close"
        aria-label="关闭上传与编辑"
        title="关闭上传与编辑"
      >
        <i data-lucide="x"></i>
      </button>
      <p class="dialog-mark">上传与编辑</p>
      <h2 id="editor-title">定制你的闪卡</h2>
      <section class="edit-block">
        <h3>卡面图片</h3>
        <label class="edit-row" for="file-subject"
          >主体图<input id="file-subject" type="file" accept="image/*"
        /></label>
        <label class="edit-row" for="file-background"
          >背景图（可选）<input id="file-background" type="file" accept="image/*"
        /></label>
        <p class="edit-hint">图片自动铺满卡面，保留原始宽高比；透明 PNG 会保留透明区域。</p>
      </section>
      <section class="edit-block">
        <h3>文字内容</h3>
        <label class="edit-row" for="text-title"
          >标题<input id="text-title" maxlength="14" autocomplete="off"
        /></label>
        <label class="edit-row" for="text-subtitle"
          >副标题<input id="text-subtitle" maxlength="20" autocomplete="off"
        /></label>
        <label class="edit-row" for="text-collection"
          >系列<input id="text-collection" maxlength="16" autocomplete="off"
        /></label>
        <label class="edit-row" for="text-technique"
          >招式<input id="text-technique" maxlength="12" autocomplete="off"
        /></label>
        <label class="edit-row" for="text-tagline"
          >寄语<input id="text-tagline" maxlength="28" autocomplete="off"
        /></label>
        <label class="edit-row" for="text-edition"
          >编号<input id="text-edition" maxlength="12" autocomplete="off"
        /></label>
      </section>
      <div class="edit-actions">
        <button id="apply-edit" class="edit-primary">应用更改</button>
        <button id="reset-edit" class="edit-ghost">恢复默认</button>
      </div>
    </dialog>
    <dialog id="about"'''
assert s.count('<dialog id="about"') == 1, 'about anchor'
s = s.replace('<dialog id="about"', editor_dialog, 1)

# 3) 脚本引用（在 app.bundle.js 之后）
old_script = '    <script type="module" src="./app.bundle.js"></script>\n  </body>'
new_script = '    <script type="module" src="./app.bundle.js"></script>\n    <script src="./editor.js"></script>\n  </body>'
assert s.count(old_script) == 1, 'script anchor'
s = s.replace(old_script, new_script)

# 4) 样式（head 中 stylesheet 之后）
style_block = '''    <style>
      .edit-block { margin: 26px 0 0; }
      .edit-block h3 {
        font: 600 13px/1.4 var(--font-ui, sans-serif);
        letter-spacing: 0.08em;
        margin: 0 0 12px;
        color: #6b6f63;
      }
      .edit-row {
        display: grid;
        grid-template-columns: 62px 1fr;
        align-items: center;
        gap: 10px;
        margin: 8px 0;
        font: 13px/1.4 var(--font-ui, sans-serif);
        color: var(--ink, #26261f);
      }
      .edit-row input[type="text"],
      .edit-row input:not([type]) {
        font: 14px/1.3 "KaiTi", "STKaiti", serif;
        padding: 7px 10px;
        border: 1px solid #dcded6;
        border-radius: 6px;
        background: #fafaf7;
        color: var(--ink, #26261f);
        min-width: 0;
      }
      .edit-row input:focus {
        outline: 2px solid var(--focus, #8a6d4f);
        outline-offset: 1px;
        border-color: transparent;
      }
      .edit-row input[type="file"] {
        font: 12px/1.3 var(--font-ui, sans-serif);
        color: #55584c;
        min-width: 0;
      }
      .edit-hint {
        font: 12px/1.6 var(--font-ui, sans-serif);
        color: #8b8e80;
        margin: 10px 0 0;
      }
      .edit-actions {
        display: flex;
        gap: 10px;
        margin-top: 30px;
      }
      .edit-actions button {
        flex: 1;
        padding: 10px 0;
        border-radius: 6px;
        font: 600 14px/1.3 var(--font-ui, sans-serif);
        cursor: pointer;
      }
      .edit-primary {
        background: #26261f;
        color: #fff;
        border: 1px solid #26261f;
      }
      .edit-primary:hover { background: #3c3c32; }
      .edit-ghost {
        background: transparent;
        color: #55584c;
        border: 1px solid #dcded6;
      }
      .edit-ghost:hover { background: #f1f2ee; }
      dialog { max-height: 86vh; overflow: auto; }
    </style>'''
old_style = '    <link rel="stylesheet" href="./style.css" />'
assert s.count(old_style) == 1, 'style anchor'
s = s.replace(old_style, old_style + '\n' + style_block)

out = s.replace('\n', '\r\n') if crlf else s
open(p, 'wb').write(out.encode('utf-8'))
print('index.html updated (crlf=%s)' % crlf)
