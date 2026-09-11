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

# 해시를 붙일 대상. HTML 안에서 쓰이는 경로 그대로.
ASSETS = [
    "/assets/site.css",
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


def main() -> None:
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
