# YK_card · 闪卡工坊（3D 全息闪卡编辑器）

上传图片 → 自动抠背景 → 调整分层/阴影/闪光 → 生成可拖拽旋转的 **3D 全息闪卡**。

基于 [RuiC-card-skill](https://github.com/) 的 Blender + Three.js 流水线制作。

## 功能

- **上传与编辑**：上传主体图/背景图，自动抠除背景（可吸管微调容差）
- **文字编辑**：标题、副标题、系列、招式、寄语、编号，实时更新
- **分层视差**：主体 / 背景 / 文字三层独立深度
- **阴影控制**：主体阴影的浓度、偏移、角度
- **主体溢出**：主体可放大冲出卡面边界
- **拖拽交互**：移动主体 / 旋转卡片 双模式
- **动态闪光**：星芒闪烁 + 柔和扫光（强度/密度/速度可调）
- **导出**：一键保存当前卡面为图片

## 快速开始

```powershell
cd web
npm install --ignore-scripts   # 首次运行
node server.mjs
```

打开浏览器访问 **http://127.0.0.1:4173/**

## 目录结构

```
YK_card/
├─ card.blend            # Blender 3D 卡面工程（可编辑）
├─ card-config.json      # 闪卡配置（标题/系列/默认参数）
├─ assets/               # 主体/背景/文字/线稿分层素材
├─ renders/              # Blender 离线渲染成品
├─ shots/                # 迭代过程演示截图
├─ web/                  # 网页应用
│  ├─ index.html         # 页面 + 右侧编辑面板
│  ├─ app.js             # Three.js 渲染 + GLSL 着色器
│  ├─ editor.js          # 上传/抠图/分层/阴影/闪光/拖拽
│  ├─ app.bundle.js      # bun 打包产物（单文件）
│  ├─ server.mjs         # 本地服务
│  └─ assets/card.glb    # 导出 3D 模型
└─ tools/                # Blender 便携版（.gitignore 排除，按需下载）
```

## 技术栈

Blender 4.5（Cycles 渲染 + 节点着色器）、Three.js（GLSL 实时材质）、Node.js、Bun

> Blender 自研着色器节点图在网页端以 GLSL 等价重建，实时渲染与离线渲染存在细微差异属预期。
