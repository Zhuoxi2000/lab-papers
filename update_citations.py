#!/usr/bin/env python3
"""每周自动刷新 papers.json 里的引用数（Semantic Scholar 口径）。

- 只处理填了 arxiv 或 doi 的论文；在投、未挂 arXiv 的跳过（引用维持 0，状态手动维护）。
- 引用数变化（或该论文还没有任何历史点）时，追加/更新当月的 history 数据点，供看板画趋势线。
- 可选环境变量 S2_API_KEY：论文多了可到 semanticscholar.org 免费申请 key，避开匿名公共限流池。

本地手动跑：python3 update_citations.py
"""
import json
import os
import sys
import time
import urllib.request

API = "https://api.semanticscholar.org/graph/v1/paper/{}?fields=citationCount"


def fetch(paper_id):
    headers = {"User-Agent": "lab-papers-bot/1.0 (github.com/Zhuoxi2000/lab-papers)"}
    key = os.environ.get("S2_API_KEY")
    if key:
        headers["x-api-key"] = key
    req = urllib.request.Request(API.format(paper_id), headers=headers)
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                return json.load(r)["citationCount"]
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 2:
                time.sleep(30)  # 匿名限流：歇 30 秒再试
                continue
            raise
    raise RuntimeError("unreachable")


def main():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "papers.json")
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    today = time.strftime("%Y-%m")
    changed = False
    for p in data["papers"]:
        pid = ("arXiv:" + p["arxiv"]) if p.get("arxiv") else \
              (("DOI:" + p["doi"]) if p.get("doi") else None)
        if not pid:
            print(f"  跳过（无 arXiv/DOI）  {p['title'][:60]}")
            continue
        try:
            c = fetch(pid)
        except Exception as e:
            print(f"  失败  {p['title'][:50]}: {e}", file=sys.stderr)
            continue
        hist = p.setdefault("history", [])
        if c != (p.get("citations") or 0) or not hist:
            p["citations"] = c
            if hist and hist[-1]["d"] == today:
                hist[-1]["c"] = c
            else:
                hist.append({"d": today, "c": c})
            changed = True
        print(f"{c:>6}  {p['title'][:60]}")
        time.sleep(2)  # 对公共池温柔一点

    if changed:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print("papers.json 已更新")
    else:
        print("引用无变化，papers.json 未改动")


if __name__ == "__main__":
    main()
