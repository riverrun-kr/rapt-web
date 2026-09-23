#!/usr/bin/env python3
"""섹션 라벨용 명조 볼드 서브셋을 만든다.

라벨(문서의 `## ` 제목과 랜딩의 기능 이름)만 볼드로 찍는데, 그것 하나 때문에
Google Fonts에서 Nanum Myeongjo 700을 통째로 받으면 **179KB**가 더 나간다
(실측 2026-09-23 — 92개 조각 중 라벨 글자가 걸치는 12개). 라벨이 쓰는 글자는
200자도 안 되므로, 그 글자만 남긴 woff2를 직접 서빙하는 게 훨씬 싸다.
워드마크(Bodoni)에 이미 쓰는 방식과 같다.

    python3 scripts/subset_label_font.py           # content/*.md 에서 글자를 모은다

**라벨 문구를 고치거나 문서를 추가하면 이 스크립트를 다시 돌려야 한다.**
서브셋에 없는 글자는 이 폰트가 못 그려서 다음 폰트로 떨어지고, 거기서
브라우저가 가짜 굵기를 만들어낸다 — 그 글자만 굵기와 모양이 튄다.
빠진 글자가 있으면 아래 검사가 잡아준다.

원본: https://raw.githubusercontent.com/google/fonts/main/ofl/nanummyeongjo/NanumMyeongjo-Bold.ttf
(SIL OFL 1.1 — /licenses/ 에 이미 고지돼 있다. 라이선스 원문은 assets/fonts/OFL.txt)
"""
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE_URL = ("https://raw.githubusercontent.com/google/fonts/main/ofl/"
              "nanummyeongjo/NanumMyeongjo-Bold.ttf")
OUT = ROOT / "assets" / "fonts" / "NanumMyeongjo-Bold-labels.woff2"

# 라벨에 안 쓰이더라도 늘 넣어두는 글자 — 조항 번호와 문장부호는 문서가
# 늘어나면 거의 확실히 쓰인다. 몇 글자 더 넣는 비용이 빠뜨리는 비용보다 싸다.
ALWAYS = set("0123456789. ·—–()[]&/:,'’“”")
ALWAYS |= set("abcdefghijklmnopqrstuvwxyz")
ALWAYS |= set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")


def label_chars() -> set:
    """content/*.md 의 '## ' 제목 + index.html 의 <dt> 에서 글자를 모은다."""
    chars = set(ALWAYS)
    for md in sorted((ROOT / "content").rglob("*.md")):
        for line in md.read_text(encoding="utf-8").splitlines():
            if line.startswith("## "):
                chars |= set(line[3:].strip())
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    for m in re.findall(r"<dt[^>]*>(.*?)</dt>", html, re.S):
        chars |= set(re.sub(r"<[^>]+>", "", m).strip())
    return {c for c in chars if c.strip()}


def main() -> None:
    try:
        from fontTools import subset
        from fontTools.ttLib import TTFont
    except ImportError:
        sys.exit("fontTools가 필요하다:  pip install 'fonttools[woff]' brotli")

    chars = label_chars()
    print(f"라벨이 쓰는 고유 글자 {len(chars)}자")

    cache = ROOT / ".cache-NanumMyeongjo-Bold.ttf"
    if not cache.exists():
        print("원본 내려받는 중…")
        urllib.request.urlretrieve(SOURCE_URL, cache)

    font = TTFont(cache)
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
    missing = {c for c in chars if ord(c) not in covered}
    print(f"→ {OUT.relative_to(ROOT)}  {OUT.stat().st_size / 1024:.1f} KB")
    print("빠진 글자: " + ("없음" if not missing else " ".join(sorted(missing))))
    if missing:
        sys.exit(1)


if __name__ == "__main__":
    sys.exit(main())
