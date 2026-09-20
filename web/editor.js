/* 闪卡工坊 · 上传图片与编辑文字
   1. 上传主体/背景图替换卡面纹理；
   2. 主体图自动抠除背景（边缘主色色键 + 吸管取色 + 容差微调 + 恢复原图）；
   3. 由主体轮廓生成软阴影贴图，与主体分层叠加；
   4. 分层与阴影参数（距离/大小/阴影浓度/偏移/角度）实时生效；
   5. 编辑标题/副标题/系列/招式/寄语/编号并实时重建文字层。 */
(function () {
  "use strict";
  var $ = function (id) { return document.getElementById(id); };
  var S = 1024, T = 1536; // 与素材画布一致
  var pending = { subject: null, background: null };
  var states = { subjectOriginal: null, subject: null, keyColor: null };
  var picking = false;

  function toast(msg) {
    var el = $("notice");
    if (!el) return;
    el.textContent = msg;
    el.hidden = false;
    clearTimeout(toast._t);
    toast._t = setTimeout(function () { el.hidden = true; }, 2600);
  }

  function waitHolo(cb, tries) {
    tries = tries || 0;
    if (window.__holo && window.__holo.ready) { cb(window.__holo); return; }
    if (tries > 200) return; // 约 20s 上限
    setTimeout(function () { waitHolo(cb, tries + 1); }, 100);
  }

  function readFile(file) {
    return new Promise(function (resolve, reject) {
      var fr = new FileReader();
      fr.onload = function () {
        var img = new Image();
        img.onload = function () { resolve(img); };
        img.onerror = reject;
        img.src = fr.result;
      };
      fr.onerror = reject;
      fr.readAsDataURL(file);
    });
  }

  // cover-fit 铺满 1024x1536 画布，保留透明通道
  function coverCanvas(img) {
    var c = document.createElement("canvas");
    c.width = S; c.height = T;
    var ctx = c.getContext("2d", { willReadFrequently: true });
    var s = Math.max(S / img.width, T / img.height);
    var dw = img.width * s, dh = img.height * s;
    ctx.drawImage(img, (S - dw) / 2, (T - dh) / 2, dw, dh);
    return c;
  }

  function cloneTexSettings(oldTex, newTex) {
    newTex.colorSpace = oldTex.colorSpace;
    newTex.wrapS = oldTex.wrapS;
    newTex.wrapT = oldTex.wrapT;
    newTex.magFilter = oldTex.magFilter;
    newTex.minFilter = oldTex.minFilter;
    newTex.anisotropy = oldTex.anisotropy;
    return newTex;
  }

  function applyImageLayer(uniform, canvas, label) {
    var makeTex = window.__holo.makeCanvasTexture;
    var old = uniform.value;
    var tex = cloneTexSettings(old, makeTex(canvas));
    tex.needsUpdate = true;
    uniform.value = tex;
    if (old && old.dispose) old.dispose();
    if (label) toast(label + "已更新");
  }

  // ---------- 主体图背景处理（色键抠图） ----------
  function hasAlpha(canvas) {
    var ctx = canvas.getContext("2d", { willReadFrequently: true });
    var d = ctx.getImageData(0, 0, canvas.width, canvas.height).data;
    var n = d.length / 4, low = 0;
    for (var i = 0; i < n; i++) if (d[i * 4 + 3] < 8) low++;
    return low / n > 0.02;
  }

  // 取边缘环（4px）的众数色作为背景键色：主体贴边时也不会被平均色带偏
  function edgeKeyColor(canvas) {
    var ctx = canvas.getContext("2d", { willReadFrequently: true });
    var w = canvas.width, h = canvas.height;
    var pts = [];
    function push(imgData, ww, hh) {
      var d = imgData.data;
      for (var y = 0; y < hh; y++) {
        for (var x = 0; x < ww; x++) {
          var i = (y * ww + x) * 4;
          if (d[i + 3] < 8) continue;
          var qr = d[i] >> 4, qg = d[i + 1] >> 4, qb = d[i + 2] >> 4;
          pts.push(qr * 4096 + qg * 64 + qb);
        }
      }
    }
    push(ctx.getImageData(0, 0, w, 4), w, 4);
    push(ctx.getImageData(0, h - 4, w, 4), w, 4);
    push(ctx.getImageData(0, 0, 4, h), 4, h);
    push(ctx.getImageData(w - 4, 0, 4, h), 4, h);
    var counts = {};
    for (var i = 0; i < pts.length; i++) counts[pts[i]] = (counts[pts[i]] || 0) + 1;
    var best = null, bestC = -1;
    for (var k in counts) if (counts[k] > bestC) { bestC = counts[k]; best = +k; }
    var br = ((best >> 12) & 15) << 4;
    var bg = ((best >> 6) & 63) << 4;
    var bb = (best & 63) << 4;
    return [br + 8, bg + 8, bb + 8];
  }

  function keyOut(canvas, keyColor, tol, feather) {
    var out = document.createElement("canvas");
    out.width = canvas.width; out.height = canvas.height;
    var octx = out.getContext("2d", { willReadFrequently: true });
    octx.drawImage(canvas, 0, 0);
    var img = octx.getImageData(0, 0, out.width, out.height);
    var d = img.data;
    var kr = keyColor[0], kg = keyColor[1], kb = keyColor[2];
    var t = tol, f = tol + feather;
    var n = d.length / 4;
    for (var i = 0; i < n; i++) {
      var dr = d[i * 4] - kr, dg = d[i * 4 + 1] - kg, db = d[i * 4 + 2] - kb;
      var dist = Math.sqrt(dr * dr + dg * dg + db * db);
      var a = 255;
      if (dist < t) a = 0;
      else if (dist < f) a = Math.round(255 * (f - dist) / (f - t));
      if (a < d[i * 4 + 3]) d[i * 4 + 3] = a;
    }
    octx.putImageData(img, 0, 0);
    return out;
  }

  // ---------- 阴影贴图（主体轮廓 → 黑色模糊 alpha） ----------
  function blurAlpha(src, radius, passes) {
    var w = src.width, h = src.height;
    var img = src.getContext("2d", { willReadFrequently: true }).getImageData(0, 0, w, h);
    var d = img.data;
    var a = new Float32Array(w * h);
    var b = new Float32Array(w * h);
    var i, x, y;
    for (i = 0; i < w * h; i++) a[i] = d[i * 4 + 3];
    var win = 2 * radius + 1;
    var clampX = function (x) { return x < 0 ? 0 : (x >= w ? w - 1 : x); };
    var clampY = function (y) { return y < 0 ? 0 : (y >= h ? h - 1 : y); };
    for (var p = 0; p < passes; p++) {
      for (y = 0; y < h; y++) {
        var row = y * w;
        var sum = 0;
        for (x = -radius; x <= radius; x++) sum += a[row + clampX(x)];
        for (x = 0; x < w; x++) {
          b[row + x] = sum / win;
          sum += a[row + clampX(x + radius + 1)] - a[row + clampX(x - radius)];
        }
      }
      for (x = 0; x < w; x++) {
        sum = 0;
        for (y = -radius; y <= radius; y++) sum += b[clampY(y) * w + x];
        for (y = 0; y < h; y++) {
          a[y * w + x] = sum / win;
          sum += b[clampY(y + radius + 1) * w + x] - b[clampY(y - radius) * w + x];
        }
      }
    }
    var out = document.createElement("canvas");
    out.width = w; out.height = h;
    var octx = out.getContext("2d", { willReadFrequently: true });
    var img2 = octx.createImageData(w, h);
    var od = img2.data;
    for (i = 0; i < w * h; i++) {
      od[i * 4] = 0; od[i * 4 + 1] = 0; od[i * 4 + 2] = 0;
      od[i * 4 + 3] = Math.round(a[i]);
    }
    octx.putImageData(img2, 0, 0);
    return out;
  }

  function makeShadowCanvas(subjectCanvas) {
    var sil = document.createElement("canvas");
    sil.width = S; sil.height = T;
    sil.getContext("2d", { willReadFrequently: true }).drawImage(subjectCanvas, 0, 0);
    return blurAlpha(sil, 22, 2);
  }

  function renderPreview(canvas) {
    var pv = $("subject-preview");
    if (!pv) return;
    var ctx = pv.getContext("2d", { willReadFrequently: true });
    ctx.clearRect(0, 0, pv.width, pv.height);
    ctx.drawImage(canvas, 0, 0, pv.width, pv.height);
  }

  function applySubjectAndShadow(canvas, label) {
    var u = window.__holo.uniforms;
    applyImageLayer(u.tSubject, canvas, label);
    applyImageLayer(u.tShadow, makeShadowCanvas(canvas), null);
  }

  function rekey() {
    if (!states.subjectOriginal) return;
    var tol = parseInt($("key-tol").value, 10) || 55;
    var keyColor = states.keyColor || edgeKeyColor(states.subjectOriginal);
    states.keyColor = keyColor;
    states.subject = keyOut(states.subjectOriginal, keyColor, tol, 35);
    applySubjectAndShadow(states.subject, null);
    renderPreview(states.subject);
  }

  function onSubjectImage(img) {
    var canvas = coverCanvas(img);
    states.subjectOriginal = canvas;
    states.subject = canvas;
    states.keyColor = null;
    picking = false;
    var pb = $("pick-bg");
    if (pb) pb.classList.remove("picking");
    var pv = $("subject-preview");
    if (pv) pv.classList.remove("picking");
    if (hasAlpha(canvas)) {
      // 本身带透明：直接使用，无需抠图
      $("key-block").hidden = true;
      applySubjectAndShadow(canvas, "主体图");
      renderPreview(canvas);
      toast("主体图已更新（已保留透明区域）");
    } else {
      // 无透明：自动以边缘主色抠除背景
      $("key-block").hidden = false;
      var tol = parseInt($("key-tol").value, 10) || 55;
      states.keyColor = edgeKeyColor(canvas);
      states.subject = keyOut(canvas, states.keyColor, tol, 35);
      applySubjectAndShadow(states.subject, "主体图");
      renderPreview(states.subject);
      toast("已自动抠除背景，可点「吸管」微调");
    }
  }

  // ---------- 文字层重建（复刻 generate_typography.py 版式） ----------
  var GOLD = "rgb(244,208,135)";
  var CREAM = "rgb(255,241,206)";
  var STROKE = "rgba(16,21,27,0.86)";
  var FONT = '"KaiTi","STKaiti",serif';

  function drawTxt(ctx, x, y, value, size, fill, anchor, maxWidth) {
    var font = size + 'px ' + FONT;
    ctx.font = font;
    if (maxWidth) {
      while (ctx.measureText(value).width > maxWidth && size > 10) {
        size -= 1;
        ctx.font = size + 'px ' + FONT;
      }
    }
    if (anchor === "ma") { ctx.textBaseline = "middle"; y = y + size * 0.42; }
    else { ctx.textBaseline = "top"; }
    ctx.lineWidth = 2;
    ctx.strokeStyle = STROKE;
    ctx.strokeText(value, x, y);
    ctx.fillStyle = fill;
    ctx.fillText(value, x, y);
  }

  function buildTextLayer(cfg) {
    var W = 1024, H = 1536;
    var c = document.createElement("canvas");
    c.width = W; c.height = H;
    var ctx = c.getContext("2d", { willReadFrequently: true });
    ctx.textAlign = "left";
    ctx.strokeStyle = GOLD;
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(70, 245); ctx.lineTo(954, 245);
    ctx.moveTo(70, 1280); ctx.lineTo(954, 1280);
    ctx.stroke();

    drawTxt(ctx, 72, 49, cfg.subtitle || "", 25, GOLD, "la", 850);
    drawTxt(ctx, 72, 87, cfg.title || "", 88, CREAM, "la", 875);
    drawTxt(ctx, 76, 195, cfg.collection || "", 22, GOLD, "la", 850);
    ctx.textAlign = "center";
    drawTxt(ctx, 512, 1300, cfg.tagline || "", 31, GOLD, "ma", 900);
    drawTxt(ctx, 512, 1346, cfg.technique || "", 69, CREAM, "ma", 900);
    ctx.textAlign = "left";
    drawTxt(ctx, 72, 1467, cfg.edition || "", 20, GOLD, "la", 850);
    ctx.textAlign = "right";
    drawTxt(ctx, 950, 1467, "HOLOGRAPHIC", 18, GOLD, "la", 380);
    return c;
  }

  function applyText(holo, cfg) {
    var canvas = buildTextLayer(cfg);
    applyImageLayer(holo.uniforms.tText, canvas, "文字");
    // 同步配置，使保存文件名等跟随新标题
    Object.keys(cfg).forEach(function (k) { holo.config[k] = cfg[k]; });
    // 同步页面标签
    var setText = function (id, v) { var el = $(id); if (el) el.textContent = v || ""; };
    setText("card-title", cfg.title);
    setText("subtitle", cfg.subtitle);
    setText("description", cfg.description);
    setText("edition", cfg.edition);
    setText("about-title", [cfg.subtitle, cfg.title].filter(Boolean).join(" / "));
    setText("about-edition", cfg.edition);
    setText("about-description", cfg.description);
    document.title = (cfg.title || "闪卡") + " · 闪卡工坊";
  }

  // ---------- 分层与阴影滑杆 ----------
  function wireLayerSliders(holo) {
    var u = holo.uniforms;
    var set = function (id, v) { var el = $(id); if (el) el.value = v; };
    set("layer-depth", Math.round((u.uDepth.value || 0.28) * 100));
    set("layer-bgdepth", Math.round((u.uBgDepth.value || -0.2) * 100));
    set("layer-textdepth", Math.round((u.uTextDepth.value || 0) * 100));
    set("layer-scale", Math.round((u.uScale.value || 1) * 100));
    set("layer-shadowop", Math.round((u.uShadowOpacity.value || 0.45) * 100));
    set("layer-shadowdepth", Math.round((u.uShadowDepth.value || 0.02) * 100));
    set("layer-shadowangle", 45);
    set("layer-flash", Math.round((u.uFlashIntensity.value || 0.8) * 100));
    set("layer-flashsize", Math.round((u.uFlashScale.value || 1) * 100));
    set("layer-flashspeed", Math.round((u.uFlashSpeed.value || 1) * 100));

    function bind(id, fn) {
      var el = $(id);
      if (!el) return;
      var apply = function () { fn(parseInt(el.value, 10) || 0); };
      el.addEventListener("input", apply);
    }
    bind("layer-depth", function (v) { u.uDepth.value = v / 100; });
    bind("layer-bgdepth", function (v) { u.uBgDepth.value = v / 100; });
    bind("layer-textdepth", function (v) { u.uTextDepth.value = v / 100; });
    bind("layer-scale", function (v) { u.uScale.value = v / 100; });
    bind("layer-shadowop", function (v) { u.uShadowOpacity.value = v / 100; });
    bind("layer-shadowdepth", function (v) { u.uShadowDepth.value = v / 100; });
    bind("layer-flash", function (v) { u.uFlashIntensity.value = v / 100; });
    bind("layer-flashsize", function (v) { u.uFlashScale.value = v / 100; });
    bind("layer-flashspeed", function (v) { u.uFlashSpeed.value = v / 100; });
    bind("layer-shadowangle", function (v) {
      var a = v * Math.PI / 180;
      var vec = holo.makeVector2(Math.cos(a), Math.sin(a));
      u.uShadowDir.value.copy(vec);
    });
  }

  // ---------- 主体溢出开关 + 拖拽移动主体 ----------
  var dragMode = "rotate"; // rotate | move

  function wireLayerExtras(holo) {
    var u = holo.uniforms;

    var clipBtn = $("layer-clip");
    if (clipBtn) {
      var syncClip = function () {
        var overflow = u.uClip.value < 0.5;
        clipBtn.textContent = overflow ? "主体溢出：开" : "主体溢出：关";
        clipBtn.classList.toggle("picking", overflow);
      };
      syncClip();
      clipBtn.addEventListener("click", function () {
        u.uClip.value = u.uClip.value < 0.5 ? 1 : 0;
        syncClip();
        toast(u.uClip.value < 0.5 ? "主体溢出已开启，可放大冲出卡面" : "主体已裁剪在卡面内");
      });
    }

    var modeBtn = $("drag-mode");
    if (modeBtn) {
      var syncMode = function () {
        modeBtn.textContent = dragMode === "move" ? "拖拽：移动主体" : "拖拽：旋转卡片";
        modeBtn.classList.toggle("picking", dragMode === "move");
      };
      syncMode();
      modeBtn.addEventListener("click", function () {
        dragMode = dragMode === "move" ? "rotate" : "move";
        syncMode();
        toast(dragMode === "move" ? "拖拽模式：移动主体；再次点击切回旋转" : "拖拽模式：旋转卡片");
      });
    }

    var flashBtn = $("flash-toggle");
    if (flashBtn) {
      var syncFlash = function () {
        var on = u.uFlash.value > 0.5;
        flashBtn.textContent = on ? "闪光：开" : "闪光：关";
        flashBtn.classList.toggle("picking", on);
      };
      syncFlash();
      flashBtn.addEventListener("click", function () {
        u.uFlash.value = u.uFlash.value > 0.5 ? 0 : 1;
        syncFlash();
        toast(u.uFlash.value > 0.5 ? "动态闪光已开启" : "动态闪光已关闭");
      });
    }

    // 移动主体：捕获阶段监听，阻止旋转拖拽
    var stage = document.getElementById("stage");
    if (!stage) return;
    var moveDrag = null;
    stage.addEventListener("pointerdown", function (e) {
      if (dragMode !== "move") return;
      if (e.button !== 0) return;
      e.stopImmediatePropagation();
      e.preventDefault();
      moveDrag = { x: e.clientX, y: e.clientY, id: e.pointerId };
      try { stage.setPointerCapture(e.pointerId); } catch (err) { /* 忽略 */ }
    }, true);
    stage.addEventListener("pointermove", function (e) {
      if (!moveDrag || moveDrag.id !== e.pointerId) return;
      e.stopImmediatePropagation();
      var rect = stage.getBoundingClientRect();
      if (rect.width > 0 && rect.height > 0) {
        u.uOffset.value.x += (e.clientX - moveDrag.x) / rect.width;
        u.uOffset.value.y += (e.clientY - moveDrag.y) / rect.height;
      }
      moveDrag.x = e.clientX;
      moveDrag.y = e.clientY;
    }, true);
    var endMove = function (e) {
      if (moveDrag && moveDrag.id === e.pointerId) moveDrag = null;
    };
    stage.addEventListener("pointerup", endMove, true);
    stage.addEventListener("pointercancel", endMove, true);
  }

  function wire(holo) {
    var cfg = holo.config || {};
    var uniforms = holo.uniforms;

    // 预填输入框
    var fields = {
      "text-title": cfg.title || "",
      "text-subtitle": cfg.subtitle || "",
      "text-collection": cfg.collection || "",
      "text-technique": cfg.technique || "",
      "text-tagline": cfg.tagline || "",
      "text-edition": cfg.edition || ""
    };
    Object.keys(fields).forEach(function (id) {
      var el = $(id);
      if (el) el.value = fields[id];
    });

    var editBtn = $("edit");
    var dialog = $("editor");
    function openPanel() {
      dialog.classList.add("open");
      dialog.style.transition = "none";
      dialog.style.transform = "none";
      dialog.removeAttribute("inert");
      document.body.classList.add("panel-open");
    }
    function closePanel() {
      dialog.classList.remove("open");
      dialog.style.transition = "none";
      dialog.style.transform = "";
      var active = document.activeElement;
      if (active && dialog.contains(active)) active.blur();
      dialog.setAttribute("inert", "");
      document.body.classList.remove("panel-open");
    }
    if (editBtn) {
      editBtn.disabled = false;
      editBtn.addEventListener("click", openPanel);
    }
    var closeBtn = $("close-editor");
    if (closeBtn) {
      closeBtn.addEventListener("click", closePanel);
    }

    function currentCfg() {
      return {
        title: $("text-title").value.trim() || cfg.title,
        subtitle: $("text-subtitle").value.trim() || cfg.subtitle,
        collection: $("text-collection").value.trim() || cfg.collection,
        technique: $("text-technique").value.trim() || cfg.technique,
        tagline: $("text-tagline").value.trim() || cfg.tagline,
        edition: $("text-edition").value.trim() || cfg.edition,
        description: cfg.description || ""
      };
    }

    // 文件选择后立即应用
    $("file-subject").addEventListener("change", function () {
      if (!this.files || !this.files[0]) return;
      var f = this.files[0];
      pending.subject = f;
      readFile(f).then(function (img) {
        try { onSubjectImage(img); }
        catch (e) { toast("应用图片失败：" + e.message); }
      }).catch(function () { toast("图片读取失败，请换一张试试"); });
    });
    $("file-background").addEventListener("change", function () {
      if (!this.files || !this.files[0]) return;
      var f = this.files[0];
      pending.background = f;
      readFile(f).then(function (img) {
        try {
          applyImageLayer(uniforms.tBackground, coverCanvas(img), "背景图");
        } catch (e) {
          toast("应用图片失败：" + e.message);
        }
      }).catch(function () { toast("图片读取失败，请换一张试试"); });
    });

    // 吸管取背景色
    var pickBtn = $("pick-bg");
    var preview = $("subject-preview");
    if (pickBtn && preview) {
      pickBtn.addEventListener("click", function () {
        picking = !picking;
        pickBtn.classList.toggle("picking", picking);
        preview.classList.toggle("picking", picking);
        toast(picking ? "点击预览图上的背景色完成取色" : "已退出取色");
      });
      preview.addEventListener("click", function (e) {
        if (!picking) return;
        var rect = preview.getBoundingClientRect();
        var x = Math.floor((e.clientX - rect.left) / rect.width * states.subjectOriginal.width);
        var y = Math.floor((e.clientY - rect.top) / rect.height * states.subjectOriginal.height);
        x = Math.max(0, Math.min(states.subjectOriginal.width - 1, x));
        y = Math.max(0, Math.min(states.subjectOriginal.height - 1, y));
        var d = states.subjectOriginal.getContext("2d", { willReadFrequently: true }).getImageData(x, y, 1, 1).data;
        states.keyColor = [d[0], d[1], d[2]];
        picking = false;
        pickBtn.classList.remove("picking");
        preview.classList.remove("picking");
        rekey();
        toast("已按所选背景色重新抠图");
      });
    }
    var tolEl = $("key-tol");
    if (tolEl) {
      tolEl.addEventListener("input", function () {
        if (states.subjectOriginal && !states.keyColor) states.keyColor = edgeKeyColor(states.subjectOriginal);
        rekey();
      });
    }
    var keyReset = $("key-reset");
    if (keyReset) {
      keyReset.addEventListener("click", function () {
        if (!states.subjectOriginal) return;
        states.subject = states.subjectOriginal;
        states.keyColor = null;
        picking = false;
        if (pickBtn) pickBtn.classList.remove("picking");
        if (preview) preview.classList.remove("picking");
        applySubjectAndShadow(states.subject, null);
        renderPreview(states.subject);
        toast("已恢复原图（不含抠图）");
      });
    }

    wireLayerSliders(holo);
    wireLayerExtras(holo);

    $("apply-edit").addEventListener("click", function () {
      applyText(holo, currentCfg());
      closePanel();
      toast("卡面已更新，可保存图片");
    });
    $("reset-edit").addEventListener("click", function () {
      location.reload();
    });
  }

  waitHolo(wire);
})();
