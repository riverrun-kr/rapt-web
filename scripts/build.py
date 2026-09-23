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
LANDING_TEMPLATE = (ROOT / "scripts" / "landing.html").read_text(encoding="utf-8")

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

# 랜딩과 404. 랜딩은 2026-09-23까지 손수 쓴 index.html이었는데, 영문 홈이
# 생기면서 **손으로 관리하는 페이지가 4개**가 될 참이었다. 푸터가 이미 세 곳에서
# 따로 놀고 있었고(404의 푸터엔 사업자 정보가 빠져 있었다) 한 곳 더 늘리는 건
# 시간 문제라, 헤더·푸터·언어 전환을 **코드 한 곳에서 생성**하는 쪽으로 옮겼다.
LANDINGS = [
    {"slug": "", "lang": "ko", "source": "home.md", "alt": "en",
     "title": "Rapt",
     "description": "떠오른 순간은 글감으로 적어두고, 때가 된 것만 글로 옮겨 씁니다. "
                    "Threads에 최적화된 미니멀 글쓰기 앱, Rapt."},
    {"slug": "en", "lang": "en", "source": "en/home.md", "alt": "",
     "title": "Rapt",
     "description": "A minimal writing app built for Threads."},
]

NOT_FOUND = {"lang": "ko", "title": "찾을 수 없는 페이지",
             "heading": "여기엔 아무것도 없어요",
             "body": ["주소를 다시 확인해 주세요.",
                      '<a href="/">Rapt로 돌아가기 →</a>']}

# 사업자 정보 — 전자상거래법 표시이면서, Meta 비즈니스 인증이 "법적 상호가
# 웹사이트에 없어 이 사이트가 그 사업자의 것인지 확인할 수 없다"로 거절한
# 자리이기도 하다(2026-09-23). **상호는 사업자등록증 표기 그대로 둘 것** —
# Meta가 문서와 글자로 대조한다.
BUSINESS = ("카인드닷츠 (KIND_DOTS goods) · 대표 김재민<br>\n"
            "    사업자등록번호 637-23-01474<br>\n"
            "    경기도 수원시 영통구 웰빙타운로 50, 8504동 1101호")


def home(lang: str) -> str:
    return "/en/" if lang == "en" else "/"


def header_html(lang: str, alt: str, wordmark: bool) -> str:
    """상단 바 — 워드마크(왼쪽)와 언어 전환(오른쪽).

    전환 링크가 푸터 맨 아래, 이메일과 사업자 정보 **뒤**에 있어서 페이지에서
    가장 마지막에 보이는 자리였다(오너 지적, 2026-09-23). 위로 올리면서 형식도
    바꿨다: 가려는 쪽 하나만 걸어두면 지금 무슨 언어를 보고 있는지가 안 보이므로
    **둘 다 적고 현재 언어를 잉크로** 둔다 — 앱이 상태를 색이 아니라 형태·농도로
    말하는 것과 같다. 랜딩에는 큰 워드마크가 히어로 안에 있으므로 여기선 뺀다.
    """
    alt_lang = "en" if lang == "ko" else "ko"
    parts = []
    if wordmark:
        parts.append(f'  <a class="wordmark" href="{home(lang)}">Rapt</a>')
    here = SWITCH_LABEL[lang]
    there = SWITCH_LABEL[alt_lang]
    parts.append(
        f'  <p class="lang"><span class="lang-on">{here}</span>'
        f'<a href="/{alt}/" hreflang="{alt_lang}" lang="{alt_lang}">{there}</a></p>'
        .replace("//", "/")
    )
    return '<header class="site-header">\n' + "\n".join(parts) + "\n</header>"


def footer_html(lang: str) -> str:
    nav = "\n".join(f'    <a href="{href}">{label}</a>' for href, label in FOOTER[lang])
    return (
        '<footer class="site-footer">\n'
        f'  <a class="wordmark" href="{home(lang)}">Rapt</a>\n'
        f'  <nav class="footer-nav">\n{nav}\n  </nav>\n'
        '  <a class="footer-mail" href="mailto:support@rapt.kr">support@rapt.kr</a>\n'
        f'  <p class="footer-business">{BUSINESS}</p>\n'
        '</footer>'
    )


def alternates_html(ko_path: str) -> str:
    """ko_path는 한국어판 경로(빈 문자열이면 루트)."""
    ko = f"{SITE}/{ko_path}/".replace("//", "/").replace("https:/", "https://")
    en = f"{SITE}/en/{ko_path}/".replace("//", "/").replace("https:/", "https://")
    return "\n".join([
        f'<link rel="alternate" hreflang="ko" href="{ko}" />',
        f'<link rel="alternate" hreflang="en" href="{en}" />',
        f'<link rel="alternate" hreflang="x-default" href="{ko}" />',
    ])


def inline(text: str) -> str:
    # 링크를 굵게보다 먼저 — 링크 라벨 안에 **굵게**가 들어와도 순서가 꼬이지 않는다.
    # (이 지원이 없어서 terms.md 3조의 [개인정보처리방침](/privacy/)이 실제 사이트에
    # 마크다운 원문 그대로 노출되고 있었다. 2026-09-11 발견.)
    text = re.sub(r"\[([^\]]+?)\]\(([^)]+?)\)", r'<a href="\2">\1</a>', text)
    # ==강조== → 500자 초과 밑칠. 오너가 원고에서 쓰는 표기 그대로 받는다.
    text = re.sub(r"==(.+?)==", r'<mark class="overflow">\1</mark>', text)
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
    ko_path = doc["slug"] if lang == "ko" else doc["alt"]

    out_dir = ROOT / doc["slug"]
    out_dir.mkdir(parents=True, exist_ok=True)
    page = (
        TEMPLATE
        .replace("{{TITLE}}", f'{doc["title"]} · Rapt')
        .replace("{{DESCRIPTION}}", f'Rapt {doc["title"]}')
        .replace("{{PATH}}", doc["slug"] + "/")
        .replace("{{LANG}}", lang)
        .replace("{{ALTERNATES}}", alternates_html(ko_path))
        .replace("{{HEADER}}", header_html(lang, doc["alt"], wordmark=True))
        .replace("{{FOOTER}}", footer_html(lang))
        .replace("{{BODY}}", body_html)
    )
    (out_dir / "index.html").write_text(page, encoding="utf-8")
    print(f"wrote {out_dir / 'index.html'}")


def parse_landing(md_text: str):
    """랜딩 원고 → (머리 값들, 기능 목록 HTML).

    형식은 두 부분이다. 머리는 `KEY: 값` 줄(LEDE는 여러 줄 = 여러 행),
    그 아래는 문서와 같은 `## 라벨` + 문단. 앞의 일반 마크다운으로는 히어로
    리드·배지·플랫폼 표기를 표현할 방법이 없어서 머리만 따로 뒀다.
    """
    def paragraphs(lines):
        """빈 줄로 갈린 덩어리를 문단 목록으로. 설명이 길어지면 한 덩어리로
        쏟아내는 대신 문단을 나눌 수 있어야 한다(오너 요청, 2026-09-23)."""
        out, cur = [], []
        for line in lines:
            if line.strip():
                cur.append(line.strip())
            elif cur:
                out.append(" ".join(cur))
                cur = []
        if cur:
            out.append(" ".join(cur))
        return out

    meta, items, label, buf = {"LEDE": []}, [], None, []
    for line in md_text.splitlines():
        if line.startswith("## "):
            if label is not None:
                items.append((label, paragraphs(buf)))
            label, buf = line[3:].strip(), []
        elif label is not None:
            buf.append(line)
        elif ":" in line and line.split(":", 1)[0].isupper():
            key, value = line.split(":", 1)
            (meta["LEDE"].append(value.strip()) if key == "LEDE"
             else meta.update({key: value.strip()}))
    if label is not None:
        items.append((label, paragraphs(buf)))

    features = "\n\n".join(
        f"    <dt>{inline(name)}</dt>\n    <dd>"
        + "".join(f"<p>{inline(para)}</p>" for para in paras)
        + "</dd>"
        for name, paras in items
    )
    return meta, features


def build_landing(page: dict) -> None:
    md_text = (ROOT / "content" / page["source"]).read_text(encoding="utf-8")
    meta, features = parse_landing(md_text)

    out = ROOT / page["slug"] / "index.html" if page["slug"] else ROOT / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    html = (
        LANDING_TEMPLATE
        .replace("{{TITLE}}", page["title"])
        .replace("{{DESCRIPTION}}", page["description"])
        .replace("{{PATH}}", page["slug"] + "/" if page["slug"] else "")
        .replace("{{LANG}}", page["lang"])
        .replace("{{ALTERNATES}}", alternates_html(""))
        .replace("{{HEADER}}", header_html(page["lang"], page["alt"], wordmark=False))
        .replace("{{FOOTER}}", footer_html(page["lang"]))
        .replace("{{LEDE}}", "<br />".join(meta["LEDE"]))
        .replace("{{BADGE}}", meta.get("BADGE", ""))
        .replace("{{PLATFORMS}}", meta.get("PLATFORMS", ""))
        .replace("{{FEATURES}}", features)
    )
    out.write_text(html, encoding="utf-8")
    print(f"wrote {out}")


def build_404() -> None:
    """404도 같은 템플릿으로 찍는다 — 손으로 쓰던 동안 푸터가 실제로 드리프트했다
    (사업자 정보가 빠져 있었다). 색인 대상이 아니라 sitemap에는 넣지 않는다."""
    body = f'<h1>{NOT_FOUND["heading"]}</h1>\n' + "\n".join(
        f"<p>{line}</p>" for line in NOT_FOUND["body"])
    page = (
        TEMPLATE
        .replace("{{TITLE}}", f'{NOT_FOUND["title"]} · Rapt')
        .replace("{{DESCRIPTION}}", NOT_FOUND["title"])
        .replace("{{PATH}}", "404.html")
        .replace("{{LANG}}", NOT_FOUND["lang"])
        .replace("{{ALTERNATES}}", "")
        .replace("{{HEADER}}", header_html(NOT_FOUND["lang"], "en", wordmark=True))
        .replace("{{FOOTER}}", footer_html(NOT_FOUND["lang"]))
        .replace("{{BODY}}", body)
    )
    (ROOT / "404.html").write_text(page, encoding="utf-8")
    print(f"wrote {ROOT / '404.html'}")


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
    entries = [(ROOT / "content" / p["source"],
                p["slug"] + "/" if p["slug"] else "") for p in LANDINGS]
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
    for page in LANDINGS:
        build_landing(page)
    for doc in DOCS:
        build_doc(doc)
    build_404()
    build_sitemap()


if __name__ == "__main__":
    sys.exit(main())
