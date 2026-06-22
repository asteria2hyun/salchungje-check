"""chempold HTML 파싱 및 정규화 (순수 함수, 네트워크 없음)."""
import re
import html as _html

_TAG = re.compile(r"<[^>]+>")
_WS = re.compile(r"\s+")
_ROW = re.compile(r"<tr>(.*?)</tr>", re.S)
_CELL = re.compile(r"<td[^>]*>(.*?)</td>", re.S)
_VIEW = re.compile(r"view\('([^']+)'\)")
_PAIR = re.compile(r"<th[^>]*>(.*?)</th>\s*<td[^>]*>(.*?)</td>", re.S)


def normalize(s):
    """공백 전부 제거 + 소문자화. JS normalize와 동일 규칙."""
    return _WS.sub("", s or "").lower()


def _cell_text(fragment):
    # 태그만 제거(공백 삽입 안 함) → 물질명의 줄바꿈/CAS 구분 유지
    return _html.unescape(_TAG.sub("", fragment)).replace("\xa0", " ").strip()


def parse_list(html):
    """목록 HTML → 제품 레코드 리스트."""
    products = []
    for row in _ROW.findall(html):
        cells = [_cell_text(c) for c in _CELL.findall(row)]
        if len(cells) < 8:
            continue
        m = _VIEW.search(row)
        products.append({
            "순번": cells[0],
            "공개번호": cells[1],
            "제품명": cells[2],
            "물질명": cells[3],
            "유형": cells[4],
            "사용자": cells[5],
            "유효기간": cells[6],
            "상태": cells[7],
            "sn": m.group(1) if m else None,
        })
    return products


def _detail_text(fragment):
    return _WS.sub(" ", _html.unescape(_TAG.sub(" ", fragment))).strip()


def parse_detail(html):
    """상세 HTML → [[label, value], ...] (순서 보존)."""
    pairs = []
    for th, td in _PAIR.findall(html):
        label = _detail_text(th)
        value = _detail_text(td)
        if label:
            pairs.append([label, value])
    return pairs


def extra_names(pairs):
    """'추가제품명' 값 반환(없으면 빈 문자열)."""
    for label, value in pairs:
        if "추가제품명" in label:
            return value
    return ""
