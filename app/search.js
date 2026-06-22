// 순수 검색 함수 (브라우저·Node 공용). Python parse.normalize와 동일 규칙.
function normalize(s) {
  return (s || "").replace(/\s+/g, "").toLowerCase();
}

function matchProducts(products, query) {
  const q = normalize(query);
  if (!q) return [];
  return products.filter((p) => (p.검색텍스트 || "").includes(q));
}

export { normalize, matchProducts };
