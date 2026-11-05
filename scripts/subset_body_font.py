#!/usr/bin/env python3
"""본문 명조(Regular) 서브셋을 만든다.

본문 서체 Nanum Myeongjo 400을 Google Fonts에서 받으면 페이지마다 조각 16개쯤(약 270KB)이
오가고, 방문자의 IP 주소와 브라우저 정보가 Google(미국)로 간다 — Threads 연결 중계 화면도
마찬가지였다(2026-11-05 검토). 이 사이트가 쓰는 글자는 500자 안팎이라, 그 글자만 남긴
woff2 하나(약 80KB)를 직접 서빙한다. 라벨 볼드(subset_label_font.py)·워드마크와 같은 방식이다.

    python3 scripts/subset_body_font.py     # 원고와 빌드된 페이지에서 글자를 모은다

**원고를 고쳐 새 글자가 생기면 이 스크립트를 다시 돌린다.** 빠진 글자는 대체 서체
(AppleMyungjo·Batang)로 떨어져 그 글자만 모양이 튄다. build.py가 빌드 끝에 빠진 글자를
검사해 멈춰 주므로, 그때 이 스크립트 → stamp_assets.py → build.py 순서로 돌리면 된다.

글자는 두 곳에서 모은다.
- content/ 아래 원고 전부 — 출시 날에야 보이는 <!-- launch --> 구간도 포함된다.
- 빌드된 페이지(*.html)의 글 — build.py와 템플릿이 넣는 문구(푸터, 404 등)까지 잡힌다.

원본: https://raw.githubusercontent.com/google/fonts/main/ofl/nanummyeongjo/NanumMyeongjo-Regular.ttf
(SIL OFL 1.1 — /licenses/ 에 이미 고지돼 있다. 라이선스 원문은 assets/fonts/OFL-NanumMyeongjo.txt)
"""
import html
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE_URL = ("https://raw.githubusercontent.com/google/fonts/main/ofl/"
              "nanummyeongjo/NanumMyeongjo-Regular.ttf")
OUT = ROOT / "assets" / "fonts" / "NanumMyeongjo-Regular-site.woff2"
CACHE = ROOT / ".cache-NanumMyeongjo-Regular.ttf"

# 지금 원고에 없더라도 늘 넣어두는 글자 — 라틴 전부와 문서에 흔히 새로 들어오는 부호.
# 몇 글자 더 넣는 비용이 빠뜨리는 비용보다 싸다.
ALWAYS = {chr(c) for c in range(0x20, 0x7F)}
ALWAYS |= set("·—–…“”‘’«»→←↑↓›‹•°×±§¶©®™€₩\u00a0")

# 빌드 산출물이 아닌 곳은 건너뛴다.
SKIP_DIRS = {"scripts", ".git", "node_modules", "_site"}


def page_text(markup: str) -> str:
    """HTML에서 화면에 그려지는 글만 남긴다."""
    markup = re.sub(r"<(script|style)\b.*?</\1>", " ", markup, flags=re.S | re.I)
    markup = re.sub(r"<!--.*?-->", " ", markup, flags=re.S)
    return html.unescape(re.sub(r"<[^>]+>", " ", markup))


def site_chars() -> set:
    chars = set(ALWAYS)
    for md in sorted((ROOT / "content").rglob("*.md")):
        chars |= set(md.read_text(encoding="utf-8"))
    for page in sorted(ROOT.rglob("*.html")):
        if SKIP_DIRS & set(page.relative_to(ROOT).parts):
            continue
        chars |= set(page_text(page.read_text(encoding="utf-8")))
    # 공백 두 가지는 꼭 남긴다 — strip()으로 거르면 띄어쓰기까지 빠져, 띄어쓰기만 대체 서체
    # (AppleMyungjo, 0.4em)로 그려져 줄이 넓어졌다(2026-11-05 실측). 줄바꿈·탭만 버린다.
    return {c for c in chars if c in (" ", "\u00a0") or (c.strip() and ord(c) >= 0x20)}


def main() -> int:
    try:
        from fontTools import subset
        from fontTools.ttLib import TTFont
    except ImportError:
        sys.exit("fontTools가 필요하다:  pip install 'fonttools[woff]' brotli")

    chars = site_chars()
    print(f"사이트가 쓰는 고유 글자 {len(chars)}자")
    if not CACHE.exists():
        print("원본 내려받는 중…")
        urllib.request.urlretrieve(SOURCE_URL, CACHE)
    font = TTFont(CACHE)
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.desubroutinize = True
    opts.drop_tables += ["DSIG"]
    subsetter = subset.Subsetter(options=opts)
    subsetter.populate(text="".join(sorted(chars)))
    subsetter.subset(font)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    font.flavor = "woff2"
    font.save(OUT)

    covered = set(TTFont(OUT).getBestCmap())
    # 원본 서체에 아예 없는 글자(이모지 등)는 어차피 대체 서체가 그린다 — 따로 알린다.
    source = set(TTFont(CACHE).getBestCmap())
    absent = {c for c in chars if ord(c) not in source}
    missing = {c for c in chars if ord(c) in source and ord(c) not in covered}
    print(f"→ {OUT.relative_to(ROOT)}  {OUT.stat().st_size / 1024:.1f} KB")
    if absent:
        print("원본에도 없는 글자(대체 서체가 그림): " + " ".join(sorted(absent)))
    print("빠진 글자: " + ("없음" if not missing else " ".join(sorted(missing))))
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
