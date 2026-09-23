#!/usr/bin/env python3
"""Rapt 법적 문서 빌더: content/*.md -> {slug}/index.html

content/terms.md, content/privacy.md 을 수정한 뒤 이 스크립트를 실행하면
terms/index.html, privacy/index.html 이 다시 생성된다. 마크다운은 이 두
문서에서 실제로 쓰는 부분집합만 지원한다: '# ', '## ', '> ' (블록인용),
빈 줄로 구분된 문단, '- ' 목록, 인라인 **굵게**, 인라인 [링크](주소).
"""
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://rapt.kr"
TEMPLATE = (ROOT / "scripts" / "template.html").read_text(encoding="utf-8")

# slug가 곧 배포 경로다 — {slug}/index.html 로 나간다.
#
# 영문판을 붙일 때는 slug에 "en/" 을 앞세운다(`en/terms` → /en/terms/).
# 언어를 하위 경로로 가르는 이유: GitHub Pages는 정적이라 Accept-Language
# 협상도 서버 리디렉션도 못 한다. 서브도메인은 DNS·인증서가 따로 붙고,
# 쿼리스트링은 검색엔진이 같은 페이지로 본다 — 하위 경로만 남는다.
# 한국어가 루트(/terms/)를 계속 차지하고 영문이 /en/ 아래로 들어간다.
DOCS = [
    {"slug": "terms", "lang": "ko", "title": "이용약관",
     "source": "terms.md", "alt": "en/terms"},
    {"slug": "privacy", "lang": "ko", "title": "개인정보처리방침",
     "source": "privacy.md", "alt": "en/privacy"},
    {"slug": "support", "lang": "ko", "title": "지원",
     "source": "support.md", "alt": "en/support"},
    {"slug": "data-deletion", "lang": "ko", "title": "데이터 삭제",
     "source": "data-deletion.md", "alt": "en/data-deletion"},
    {"slug": "licenses", "lang": "ko", "title": "오픈소스 라이선스",
     "source": "licenses.md", "alt": "en/licenses"},

    {"slug": "en/terms", "lang": "en", "title": "Terms of Service",
     "source": "en/terms.md", "alt": "terms"},
    {"slug": "en/privacy", "lang": "en", "title": "Privacy Policy",
     "source": "en/privacy.md", "alt": "privacy"},
    {"slug": "en/support", "lang": "en", "title": "Support",
     "source": "en/support.md", "alt": "support"},
    {"slug": "en/data-deletion", "lang": "en", "title": "Data Deletion",
     "source": "en/data-deletion.md", "alt": "data-deletion"},
    {"slug": "en/licenses", "lang": "en", "title": "Open-Source Licenses",
     "source": "en/licenses.md", "alt": "licenses"},
]

# 푸터 문서 목록. 같은 언어 안에서만 이동한다 — 영문 페이지에서 한국어 문서로
# 빠지면 되돌아올 길이 없다. 언어를 건너는 이동은 {{LANG_SWITCH}} 하나가 맡는다.
FOOTER = {
    "ko": [("/support/", "지원"), ("/terms/", "이용약관"),
           ("/privacy/", "개인정보처리방침"), ("/data-deletion/", "데이터 삭제"),
           ("/licenses/", "오픈소스 라이선스")],
    "en": [("/en/support/", "Support"), ("/en/terms/", "Terms of Service"),
           ("/en/privacy/", "Privacy Policy"),
           ("/en/data-deletion/", "Data Deletion"),
           ("/en/licenses/", "Open-Source Licenses")],
}

# 언어 전환 링크에 붙는 라벨 — 항상 **가려는 쪽 언어로** 적는다. 읽지 못하는
# 언어로 쓰인 "English"는 출구가 되지 못한다.
SWITCH_LABEL = {"ko": "한국어", "en": "English"}


def inline(text: str) -> str:
    # 링크를 굵게보다 먼저 — 링크 라벨 안에 **굵게**가 들어와도 순서가 꼬이지 않는다.
    # (이 지원이 없어서 terms.md 3조의 [개인정보처리방침](/privacy/)이 실제 사이트에
    # 마크다운 원문 그대로 노출되고 있었다. 2026-09-11 발견.)
    text = re.sub(r"\[([^\]]+?)\]\(([^)]+?)\)", r'<a href="\2">\1</a>', text)
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)


def render_body(md_text: str) -> str:
    lines = md_text.splitlines()
    html = []
    i = 0
    para_buf = []

    def flush_para():
        if para_buf:
            html.append("<p>" + inline(" ".join(para_buf)) + "</p>")
            para_buf.clear()

    while i < len(lines):
        line = lines[i]
        if line.startswith("# "):
            flush_para()
            html.append(f"<h1>{inline(line[2:].strip())}</h1>")
        elif line.startswith("## "):
            flush_para()
            html.append(f"<h2>{inline(line[3:].strip())}</h2>")
        elif line.startswith(">"):
            flush_para()
            quote_paras, cur = [], []
            while i < len(lines) and lines[i].startswith(">"):
                content = lines[i][1:].strip()
                if content:
                    cur.append(content)
                else:
                    if cur:
                        quote_paras.append(" ".join(cur))
                    cur = []
                i += 1
            if cur:
                quote_paras.append(" ".join(cur))
            inner = "".join(f"<p>{inline(p)}</p>" for p in quote_paras)
            html.append(f'<blockquote class="note">{inner}</blockquote>')
            continue
        elif line.startswith("- "):
            # 목록. 이 지원이 없어서 support.md의 항목들이 '-'를 글자로 달고
            # 한 문단으로 뭉쳐 나왔다(2026-09-18 발견, 인라인 링크와 같은 누락).
            flush_para()
            items = []
            while i < len(lines) and lines[i].startswith("- "):
                items.append(inline(lines[i][2:].strip()))
                i += 1
            html.append("<ul>" + "".join(f"<li>{it}</li>" for it in items) + "</ul>")
            continue
        elif line.strip() == "":
            flush_para()
        else:
            para_buf.append(line.strip())
        i += 1
    flush_para()
    return "\n".join(html)


def build_doc(doc: dict) -> None:
    src = ROOT / "content" / doc["source"]
    md_text = src.read_text(encoding="utf-8")
    body_html = render_body(md_text)

    lang = doc["lang"]
    alt = doc["alt"]
    alt_lang = "en" if lang == "ko" else "ko"
    ko_path = doc["slug"] if lang == "ko" else alt

    # hreflang은 양쪽을 다 적고 x-default는 한국어(루트)로 보낸다 — 언어를
    # 모르는 크롤러·공유 링크가 닿을 기본값이 원본이어야 한다.
    alternates = "\n".join([
        f'<link rel="alternate" hreflang="ko" href="{SITE}/{ko_path}/" />',
        f'<link rel="alternate" hreflang="en" href="{SITE}/en/{ko_path}/" />',
        f'<link rel="alternate" hreflang="x-default" href="{SITE}/{ko_path}/" />',
    ])
    nav = "\n".join(f'    <a href="{href}">{label}</a>' for href, label in FOOTER[lang])
    switch = (f'  <a class="footer-lang" href="/{alt}/" hreflang="{alt_lang}" '
              f'lang="{alt_lang}">{SWITCH_LABEL[alt_lang]}</a>')

    out_dir = ROOT / doc["slug"]
    out_dir.mkdir(parents=True, exist_ok=True)
    page = (
        TEMPLATE
        .replace("{{TITLE}}", f'{doc["title"]} · Rapt')
        .replace("{{DESCRIPTION}}", f'Rapt {doc["title"]}')
        .replace("{{PATH}}", doc["slug"] + "/")
        .replace("{{LANG}}", lang)
        .replace("{{ALTERNATES}}", alternates)
        .replace("{{FOOTER_NAV}}", nav)
        .replace("{{LANG_SWITCH}}", switch)
        .replace("{{BODY}}", body_html)
    )
    (out_dir / "index.html").write_text(page, encoding="utf-8")
    print(f"wrote {out_dir / 'index.html'}")


def last_modified(path: Path) -> str:
    """sitemap의 lastmod — 파일의 마지막 커밋 날짜, 아직 안 올렸으면 오늘.

    손으로 관리하던 값이라 매번 빠졌다(9/22 변경이 9/18 날짜를 달고 있었다).
    파일 mtime은 clone하면 체크아웃 시각으로 뭉개지니 git을 근거로 삼고,
    아직 커밋 안 된 수정이 있으면 오늘 — 어차피 오늘 커밋해서 배포한다.
    git이 없는 환경(내려받은 zip 등)에서도 죽지 않게 오늘로 떨어뜨린다.
    """
    rel = str(path.relative_to(ROOT))
    try:
        dirty = subprocess.run(
            ["git", "diff", "--quiet", "HEAD", "--", rel], cwd=ROOT
        ).returncode != 0
        if dirty:
            return date.today().isoformat()
        out = subprocess.run(
            ["git", "log", "-1", "--format=%cs", "--", rel],
            cwd=ROOT, capture_output=True, text=True, check=True,
        ).stdout.strip()
        return out or date.today().isoformat()
    except (OSError, subprocess.SubprocessError):
        return date.today().isoformat()


def build_sitemap() -> None:
    """sitemap.xml — DOCS에서 그대로 뽑는다.

    페이지를 더하면 DOCS 한 줄로 끝나고 sitemap은 따라온다. /threads-callback/
    은 OAuth 중계라 noindex이므로 여기 없다(일부러).
    """
    entries = [(ROOT / "index.html", "")]
    entries += [(ROOT / "content" / doc["source"], doc["slug"] + "/") for doc in DOCS]

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        "<!-- scripts/build.py가 생성한다 — 직접 고치지 말 것.",
        "     /threads-callback/ 은 noindex(OAuth 중계)라 일부러 뺀다. -->",
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for source, path in entries:
        lines += [
            "  <url>",
            f"    <loc>{SITE}/{path}</loc>",
            f"    <lastmod>{last_modified(source)}</lastmod>",
            "  </url>",
        ]
    lines.append("</urlset>")

    out = ROOT / "sitemap.xml"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {out}")


def main() -> None:
    for doc in DOCS:
        build_doc(doc)
    build_sitemap()


if __name__ == "__main__":
    sys.exit(main())
