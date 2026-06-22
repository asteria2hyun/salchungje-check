"""chempold 네트워크 수집 (표준 라이브러리 urllib만 사용)."""
import urllib.request
import urllib.parse

BASE = "https://chempold.keiti.re.kr/cpms/bcp/disc/"
_HEADERS = {"User-Agent": "Mozilla/5.0"}


def list_request(count=1000):
    url = BASE + "bcp000List.do"
    data = urllib.parse.urlencode({
        "pageIndex": "1",
        "searchKey1": "SC001",
        "searchKey2": "",
        "countPerPage": str(count),
    }).encode("utf-8")
    return url, data, dict(_HEADERS)


def detail_url(sn):
    return BASE + "BcpDisclosureView.do?" + urllib.parse.urlencode({"bcpDiscSn": sn})


def _get(url, data=None, headers=None):
    req = urllib.request.Request(url, data=data, headers=headers or dict(_HEADERS))
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read().decode("utf-8")


def fetch_list_html(count=1000):
    url, data, headers = list_request(count)
    return _get(url, data=data, headers=headers)


def fetch_detail_html(sn):
    return _get(detail_url(sn))
