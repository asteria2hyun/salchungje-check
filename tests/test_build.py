import os, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "build"))
import fetch
import build as builder


class TestFetchRequest(unittest.TestCase):
    def test_list_request_params(self):
        url, data, headers = fetch.list_request(1000)
        self.assertIn("bcp000List.do", url)
        body = data.decode()
        self.assertIn("searchKey1=SC001", body)
        self.assertIn("countPerPage=1000", body)
        self.assertIn("Mozilla", headers.get("User-Agent", ""))

    def test_detail_url(self):
        self.assertEqual(
            fetch.detail_url("2025-182"),
            "https://chempold.keiti.re.kr/cpms/bcp/disc/BcpDisclosureView.do?bcpDiscSn=2025-182",
        )


class TestAssembleRender(unittest.TestCase):
    def test_search_text_includes_extra_names(self):
        product = {"제품명": "홈매트 리퀴드 에스", "물질명": "Prallethrin (CAS No. 23031-36-9)"}
        pairs = [["추가제품명", "홈키파 홈매트, 홈키파 리퀴드"]]
        st = builder.build_search_text(product, pairs)
        self.assertIn("홈키파", st)
        self.assertIn("홈매트리퀴드에스", st)
        self.assertEqual(st, st.lower())
        self.assertNotIn(" ", st)

    def test_assemble_attaches_detail_and_searchtext(self):
        records = [{"제품명": "홈매트 리퀴드 에스", "물질명": "P", "sn": "2025-182"},
                   {"제품명": "작업중품", "물질명": "Q", "sn": None}]
        details = {"2025-182": [["추가제품명", "홈키파"]]}
        out = builder.assemble(records, details)
        self.assertEqual(out[0]["상세"], [["추가제품명", "홈키파"]])
        self.assertIn("홈키파", out[0]["검색텍스트"])
        self.assertEqual(out[1]["상세"], [])

    def test_render_injects_data_and_js(self):
        template = 'A /*__SEARCH_JS__*/ B var DB = __DB_JSON__; C'
        search_js = "function normalize(s){return s;}\nexport { normalize };\n"
        db = {"기준일": "2026-06-23", "제품": [{"제품명": "홈매트"}]}
        html = builder.render_html(template, search_js, db)
        self.assertIn("function normalize", html)
        self.assertNotIn("export {", html)
        self.assertIn('"2026-06-23"', html)
        self.assertIn("홈매트", html)
        self.assertNotIn("__DB_JSON__", html)


if __name__ == "__main__":
    unittest.main()
