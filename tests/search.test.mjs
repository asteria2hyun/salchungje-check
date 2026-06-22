import { test } from "node:test";
import assert from "node:assert/strict";
import { normalize, matchProducts } from "../app/search.js";

const DB = [
  { 제품명: "홈매트 리퀴드 에스", 검색텍스트: "홈매트리퀴드에스홈키파홈매트prallethrin" },
  { 제품명: "베스핀쓰리", 검색텍스트: "베스핀쓰리clorofene" },
];

test("normalize removes spaces and lowercases", () => {
  assert.equal(normalize("홈매트 리퀴드 ES"), "홈매트리퀴드es");
});

test("matchProducts finds by partial keyword (홈키파 via 추가제품명)", () => {
  const r = matchProducts(DB, "홈키파");
  assert.equal(r.length, 1);
  assert.equal(r[0].제품명, "홈매트 리퀴드 에스");
});

test("matchProducts ignores spacing", () => {
  assert.equal(matchProducts(DB, "홈 매 트").length, 1);
});

test("empty query returns nothing", () => {
  assert.equal(matchProducts(DB, "   ").length, 0);
});

test("no match returns empty", () => {
  assert.equal(matchProducts(DB, "타이레놀").length, 0);
});
