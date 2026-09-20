// 纯静态资产 Worker：所有请求由 [assets] 目录（./web）提供，无需自定义脚本。
export default {
  async fetch(request, env, ctx) {
    // 未匹配到静态文件时返回 404（前端为单页应用，资源均为静态文件）
    return new Response("Not Found", { status: 404 });
  },
};
