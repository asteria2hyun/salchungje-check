import os, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "build"))
from parse import parse_detail, extra_names

FIX = os.path.join(os.path.dirname(__file__), "fixtures", "detail_sample.html")


class TestParseDetail(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(FIX, encoding="utf-8") as f:
            cls.pairs = parse_detail(f.read())

    def test_has_many_pairs(self):
        self.assertGreater(len(self.pairs), 50)

    def test_pairs_are_label_value(self):
        d = dict(self.pairs)
        self.assertEqual(d.get("정보공개번호"), "2025-182")
        self.assertEqual(d.get("제품명"), "홈매트 리퀴드 에스")
        self.assertEqual(d.get("살생물제품유형"), "살충제")

    def test_extra_names_contains_homekipa(self):
        self.assertIn("홈키파", extra_names(self.pairs))


if __name__ == "__main__":
    unittest.main()
