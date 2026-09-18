#!/usr/bin/env python3
"""Rapt 법적 문서 빌더: content/*.md -> {slug}/index.html

content/terms.md, content/privacy.md 을 수정한 뒤 이 스크립트를 실행하면
terms/index.html, privacy/index.html 이 다시 생성된다. 마크다운은 이 두
문서에서 실제로 쓰는 부분집합만 지원한다: '# ', '## ', '> ' (블록인용),
빈 줄로 구분된 문단, '- ' 목록, 인라인 **굵게**, 인라인 [링크](주소).
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = (ROOT / "scripts" / "template.html").read_text(encoding="utf-8")

# slug가 곧 배포 경로다 — {slug}/index.html 로 나간다.
#
# 영문판을 붙일 때는 slug에 "en/" 을 앞세운다(`en/terms` → /en/terms/).
# 언어를 하위 경로로 가르는 이유: GitHub Pages는 정적이라 Accept-Language
# 협상도 서버 리디렉션도 못 한다. 서브도메인은 DNS·인증서가 따로 붙고,
# 쿼리스트링은 검색엔진이 같은 페이지로 본다 — 하위 경로만 남는다.
# 한국어가 루트(/terms/)를 계속 차지하고 영문이 /en/ 아래로 들어간다.
DOCS = [
    {"slug": "terms", "title": "이용약관", "source": "terms.md"},
    {"slug": "privacy", "title": "개인정보처리방침", "source": "privacy.md"},
    {"slug": "support", "title": "지원", "source": "support.md"},
    {"slug": "data-deletion", "title": "데이터 삭제", "source": "data-deletion.md"},
    {"slug": "licenses", "title": "오픈소스 라이선스", "source": "licenses.md"},
]


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

    out_dir = ROOT / doc["slug"]
    out_dir.mkdir(parents=True, exist_ok=True)
    page = (
        TEMPLATE
        .replace("{{TITLE}}", f'{doc["title"]} · Rapt')
        .replace("{{DESCRIPTION}}", f'Rapt {doc["title"]}')
        .replace("{{PATH}}", doc["slug"] + "/")
        .replace("{{BODY}}", body_html)
    )
    (out_dir / "index.html").write_text(page, encoding="utf-8")
    print(f"wrote {out_dir / 'index.html'}")


def main() -> None:
    for doc in DOCS:
        build_doc(doc)


if __name__ == "__main__":
    sys.exit(main())
