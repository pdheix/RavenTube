#!/usr/bin/env python3
import json, os, html, datetime, sys
query   = os.environ.get("QUERY", "")
sort_by = os.environ.get("SORT", "relevance")
now     = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
videos = []
if os.path.exists("raw.json"):
    with open("raw.json", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                videos.append(json.loads(line))
            except json.JSONDecodeError:
                continue
sort_keys = {
    "upload_date": lambda v: v.get("upload_date") or "",
    "view_count":  lambda v: int(v.get("view_count")  or 0),
    "like_count":  lambda v: int(v.get("like_count")  or 0),
    "duration":    lambda v: int(v.get("duration")    or 0),
}
if sort_by in sort_keys:
    videos.sort(key=sort_keys[sort_by], reverse=True)
rows, urls = [], []
for i, v in enumerate(videos, 1):
    title = html.escape(v.get("title") or "?")
    dur   = int(v.get("duration")   or 0)
    views = int(v.get("view_count") or 0)
    date  = (v.get("upload_date") or "")[:10]
    url   = v.get("webpage_url") or f"https://youtu.be/{v.get('id','')}"
    url_e = html.escape(url, quote=True)
    rows.append(
        f'<tr><td>{i}</td><td><a href="{url_e}">{title}</a></td>'
        f'<td>{date}</td><td>{views:,}</td>'
        f'<td>{dur//60}:{dur%60:02d}</td></tr>'
    )
    urls.append(url)
q_esc     = html.escape(query)
rows_html = "\n".join(rows) if rows else '<tr><td colspan="5">No results</td></tr>'
page = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><title>RavenTube: {q_esc}</title>
<style>
body{{font:14px/1.4 monospace;background:#111;color:#ccc;padding:20px}}
h1{{color:#4ecdc4}}
table{{border-collapse:collapse;width:100%}}
th,td{{border:1px solid #333;padding:6px 10px;text-align:left}}
th{{background:#222}}
a{{color:#ff6b6b;text-decoration:none}}
a:hover{{text-decoration:underline}}
</style></head><body>
<h1>RavenTube: {q_esc}</h1>
<p>{now} — {len(videos)} results — sorted by {html.escape(sort_by)}</p>
<table>
<tr><th>#</th><th>Title</th><th>Date</th><th>Views</th><th>Dur</th></tr>
{rows_html}
</table></body></html>"""
with open("index.html", "w", encoding="utf-8") as f:
    f.write(page)
with open("urls.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(urls))
print(f"Generated index.html with {len(videos)} entries", file=sys.stderr)
