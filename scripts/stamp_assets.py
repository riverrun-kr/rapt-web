#!/usr/bin/env python3
"""정적 에셋 URL에 내용 해시를 붙인다 (캐시 무효화).

GitHub Pages는 모든 파일에 `Cache-Control: max-age=600`을 붙인다. 그래서 CSS나
파비콘을 고쳐 배포해도, 직전 10분 안에 그 파일을 받아간 브라우저는 재검증 없이
옛 파일을 계속 쓴다 — 새 HTML + 옛 CSS 조합이라 레이아웃이 통째로 깨져 보인다
(2026-09-11 실제로 겪음: 히어로 아래 빈 구멍, 테두리 없는 배지, 형광 노란색 강조).

URL에 내용 해시를 붙이면 파일이 바뀔 때마다 주소가 달라져 캐시가 자동으로
비껴간다. HTML 자체는 해시를 못 붙이지만(주소가 곧 URL이라), HTML은 매번
새로 받아오므로 문제가 되지 않는다.

    python3 scripts/stamp_assets.py   # 에셋을 고친 뒤 → 그다음 build.py

build.py보다 **먼저** 돌려야 한다. 이 스크립트가 template.html을 고치고,
build.py가 그 template으로 terms/privacy를 다시 찍기 때문이다.
"""
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 폰트는 **CSS 안에서** 참조된다(@font-face). 그래서 두 단계로 나눠 찍는다 —
# 아래 main() 주석 참고.
FONT_ASSETS = [
    "/assets/fonts/BodoniModa11pt-Medium-latin.woff2",
    "/assets/fonts/NanumMyeongjo-Bold-labels.woff2",
]
FONT_HOSTS = ["assets/site.css"]

# HTML 안에서 참조되는 것들.
ASSETS = [
    "/assets/site.css",
    "/assets/favicon-16.png",
    "/assets/favicon-32.png",
    "/assets/apple-touch-icon-180.png",
]

# 손으로 쓰는 페이지 + 빌드 템플릿. (terms/privacy는 산출물이라 여기 없다.)
PAGES = [
    "index.html",
    "404.html",
    "threads-callback/index.html",
    "scripts/template.html",
]


def digest(asset_path: str) -> str:
    data = (ROOT / asset_path.lstrip("/")).read_bytes()
    return hashlib.sha256(data).hexdigest()[:10]


def stamp_into(files, assets) -> None:
    stamps = {a: digest(a) for a in assets}
    for f in files:
        path = ROOT / f
        text = original = path.read_text(encoding="utf-8")
        for asset, stamp in stamps.items():
            text = re.sub(
                re.escape(asset) + r"(\?v=[0-9a-f]+)?",
                asset + "?v=" + stamp,
                text,
            )
        if text != original:
            path.write_text(text, encoding="utf-8")
            print(f"stamped {f}")
    for asset, stamp in stamps.items():
        print(f"  {asset} -> ?v={stamp}")


def main() -> None:
    # 1단계: 폰트 해시를 site.css 안에 먼저 찍는다.
    #
    # 순서가 중요하다. 폰트 URL은 CSS 안에 있으므로 CSS를 고쳐야 하는데, 그러면
    # CSS 자체의 내용이 바뀌어 해시도 달라진다. 폰트를 먼저 찍고 **그 다음에**
    # CSS 해시를 계산해야 HTML이 가리키는 값이 실제 파일과 맞는다. 반대로 하면
    # HTML은 옛 CSS 해시를 가리키고, 그게 바로 이 스크립트가 막으려던 상황이다.
    stamp_into(FONT_HOSTS, FONT_ASSETS)

    # 2단계: (이제 확정된) CSS와 파비콘 해시를 HTML에 찍는다.
    stamps = {a: digest(a) for a in ASSETS}
    for page in PAGES:
        path = ROOT / page
        text = original = path.read_text(encoding="utf-8")
        for asset, stamp in stamps.items():
            # 이미 붙어 있는 ?v=... 는 새 값으로 갈아끼운다.
            text = re.sub(
                re.escape(asset) + r"(\?v=[0-9a-f]+)?",
                asset + "?v=" + stamp,
                text,
            )
        if text != original:
            path.write_text(text, encoding="utf-8")
            print(f"stamped {page}")
    for asset, stamp in stamps.items():
        print(f"  {asset} -> ?v={stamp}")


if __name__ == "__main__":
    sys.exit(main())
