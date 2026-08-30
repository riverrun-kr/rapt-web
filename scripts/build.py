#!/usr/bin/env python3
"""Rapt 법적 문서 빌더: content/*.md -> {slug}/index.html

content/terms.md, content/privacy.md 을 수정한 뒤 이 스크립트를 실행하면
terms/index.html, privacy/index.html 이 다시 생성된다. 마크다운은 이 두
문서에서 실제로 쓰는 부분집합만 지원한다: '# ', '## ', '> ' (블록인용),
빈 줄로 구분된 문단, 인라인 **굵게**.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = (ROOT / "scripts" / "template.html").read_text(encoding="utf-8")

DOCS = [
    {"slug": "terms", "title": "이용약관", "source": "terms.md"},
    {"slug": "privacy", "title": "개인정보처리방침", "source": "privacy.md"},
]


def inline(text: str) -> str:
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
