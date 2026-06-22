# 살충제 판매가능 확인 (살생물제 승인)

2026년 7월 1일 살생물제 승인제 전면 시행 → **승인된 살생물제품만 판매 가능**.
약국 제품명을 폰에서 검색해 "판매 가능(승인됨) / 미승인(판매 불가 대상)"을 즉시 확인하는 오프라인 웹앱.

데이터 출처: 환경부 화학제품관리시스템(chempold) "승인 살생물제품 정보공개" (UTF-8, 전 건 일괄 수집).

## 빌드 (데이터 수집 → index.html 생성)

필요: Python 3 (추가 설치 불필요)

```
python build/build.py
```

생성물: `data/products.json`, `index.html` (자체 완결형, 데이터 내장)

## 테스트

```
python -m unittest discover -s tests -p "test_*.py" -v
node --test tests/search.test.mjs
```

## 배포 (GitHub Pages — 소스 private, 사이트 public)

1. GitHub에서 **private** 저장소 생성(예: `bio-check`).
2. push:
   ```
   git branch -M main
   git remote add origin https://github.com/<아이디>/bio-check.git
   git push -u origin main
   ```
3. 저장소 → Settings → Pages → Source: **Deploy from a branch**, Branch: **main / (root)** → Save
4. 1~2분 뒤 `https://<아이디>.github.io/bio-check/` 접속 → 폰에서 이 링크 사용.
   (저장소는 private, 배포된 페이지만 공개)

## 데이터 갱신

```
python build/build.py
git add index.html data/products.json
git commit -m "data: refresh"
git push
```

## 판정 의미 / 주의

- 목록에 **있음** → ✅ 승인됨 · 판매 가능 ("작업중"도 승인된 것이라 판매 가능, 상세만 준비중)
- 목록에 **없음** → ⚠️ 미승인 · 7/1부터 판매 불가 대상(살충제·살생물 용도 제품 한정)
- 같은 브랜드라도 제품(SKU)마다 승인 여부가 다름 → **정확한 제품명**으로 확인.
- 최종 판단은 공식 공지·제조사 확인 권장. 안전확인대상생활화학제품(초록누리, 별도 포털)은 이번 승인과 별개.

## 트러블슈팅

- 빌드 시 SSL/네트워크 오류: 방화벽 확인 후 재시도.
- "작업중" 제품(상세 페이지 미게시)은 리스트 정보로만 검색됨(정상).
