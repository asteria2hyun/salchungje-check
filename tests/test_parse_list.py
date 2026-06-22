import os, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "build"))
from parse import parse_list, normalize

FIX = os.path.join(os.path.dirname(__file__), "fixtures", "list_sample.html")


class TestParseList(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(FIX, encoding="utf-8") as f:
            cls.products = parse_list(f.read())

    def test_count_is_five(self):
        self.assertEqual(len(self.products), 5)

    def test_first_product_fields(self):
        p = self.products[0]
        self.assertEqual(p["제품명"], "홈매트 리퀴드 에스")
        self.assertEqual(p["공개번호"], "2025-182")
        self.assertEqual(p["상태"], "상세보기")
        self.assertEqual(p["sn"], "2025-182")
        self.assertIn("Prallethrin", p["물질명"])

    def test_jakeopjung_has_no_sn(self):
        jak = [p for p in self.products if p["상태"] == "작업중"]
        self.assertEqual(len(jak), 2)
        self.assertTrue(all(p["sn"] is None for p in jak))

    def test_normalize(self):
        self.assertEqual(normalize("홈매트 리퀴드 ES"), "홈매트리퀴드es")
        self.assertEqual(normalize("  A  B  "), "ab")


if __name__ == "__main__":
    unittest.main()
