"""빌드 오케스트레이션: 수집 → 조립 → products.json + index.html 생성."""
import os
import re
import sys
import json
import time
import datetime

sys.path.insert(0, os.path.dirname(__file__))
import fetch
from parse import parse_list, parse_detail, extra_names, normalize

_EXPORT_LINE = re.compile(r"(?m)^\s*export\s*\{[^}]*\};?\s*$")
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def build_search_text(product, detail_pairs):
    parts = [product.get("제품명", ""), product.get("물질명", ""), extra_names(detail_pairs)]
    return normalize(" ".join(p for p in parts if p))


def assemble(list_records, details_by_sn):
    out = []
    for r in list_records:
        item = dict(r)
        detail = details_by_sn.get(r.get("sn")) or []
        item["상세"] = detail
        item["검색텍스트"] = build_search_text(r, detail)
        out.append(item)
    return out


def render_html(template, search_js, db):
    js = _EXPORT_LINE.sub("", search_js)          # 브라우저용: export 줄 제거
    out = template.replace("/*__SEARCH_JS__*/", js)
    out = out.replace("__DB_JSON__", json.dumps(db, ensure_ascii=False))
    return out


def write_index(out_root, db):
    with open(os.path.join(out_root, "app", "template.html"), encoding="utf-8") as f:
        template = f.read()
    with open(os.path.join(out_root, "app", "search.js"), encoding="utf-8") as f:
        search_js = f.read()
    with open(os.path.join(out_root, "index.html"), "w", encoding="utf-8") as f:
        f.write(render_html(template, search_js, db))


def render_only(out_root=None):
    """네트워크 없이 기존 data/products.json으로 index.html만 재생성 (UI 수정용)."""
    out_root = out_root or _ROOT
    with open(os.path.join(out_root, "data", "products.json"), encoding="utf-8") as f:
        db = json.load(f)
    write_index(out_root, db)
    print(f"재생성: index.html ({db.get('총건수')}건, 기준일 {db.get('기준일')})")


def main(out_root=None, 기준일=None):
    out_root = out_root or _ROOT
    기준일 = 기준일 or datetime.date.today().isoformat()
    print("목록 수집 중...")
    records = parse_list(fetch.fetch_list_html(1000))
    print(f"  목록 {len(records)}건")
    details = {}
    targets = [r for r in records if r.get("sn")]
    for i, r in enumerate(targets, 1):
        details[r["sn"]] = parse_detail(fetch.fetch_detail_html(r["sn"]))
        if i % 20 == 0:
            print(f"  상세 {i}/{len(targets)}")
        time.sleep(0.3)
    products = assemble(records, details)
    db = {
        "기준일": 기준일,
        "총건수": len(products),
        "출처": fetch.BASE + "bcp000List.do",
        "제품": products,
    }
    os.makedirs(os.path.join(out_root, "data"), exist_ok=True)
    with open(os.path.join(out_root, "data", "products.json"), "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=1)
    write_index(out_root, db)
    print(f"완료: index.html ({len(products)}건, 기준일 {기준일})")


if __name__ == "__main__":
    if "--render-only" in sys.argv:
        render_only()
    else:
        main()
