# 实验室论文看板

成员论文档案 + 引用自动追踪。在线地址：**https://zhuoxi2000.github.io/lab-papers/**

- 首页是成员卡片墙（论文数 / 一作 / 参与 / 被引），点进去是个人主页：被引增长曲线、一作 vs 参与构成、每年产出、论文明细。
- 引用口径统一为 [Semantic Scholar](https://www.semanticscholar.org/)；已录用未见刊的论文引用记 0，**挂了 arXiv 才能开始自动追踪**。

## 文件结构

| 文件 | 作用 |
|---|---|
| `papers.json` | 唯一权威数据源（成员 + 论文 + 引用历史） |
| `index.html` | 看板页面，加载时读取 `papers.json` |
| `update_citations.py` | 引用更新脚本（按 arXiv ID / DOI 查 Semantic Scholar） |
| `.github/workflows/update-citations.yml` | 每周一 09:30（北京时间）自动跑脚本并提交 |

## 日常操作

**加人 / 删人 / 增改论文**（二选一）：

1. 网页方式：打开看板 → 右上角「编辑模式」→ 改完点「导出 JSON」→ 用导出的文件覆盖仓库里的 `papers.json`（GitHub 网页端直接上传即可）→ 强刷页面，最后点「丢弃草稿」。
2. 直接改文件：编辑 `papers.json` 后 push。

**论文录用后**：先把状态改成"已录用"；一旦挂了 arXiv，把 `arxiv` 字段填上（如 `2510.08841`），下次自动更新就会开始累积引用曲线；正式见刊后补 `doi`、状态改"已发表"。

**手动刷新引用**：仓库 Actions 页 → 「更新引用数据」→ Run workflow；或本地 `python3 update_citations.py`。

**限流**：Semantic Scholar 匿名访问偶尔 429，脚本自带重试；论文多了可免费申请 API key，存到仓库 Secrets 的 `S2_API_KEY`。

## 本地预览

```bash
python3 -m http.server 8000
# 打开 http://localhost:8000
```
