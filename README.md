# rapt.kr

Rapt(Threads 특화 미니멀 글쓰기 앱)의 공개 웹사이트. 현재는 이용약관·개인정보처리방침 게시가 목적인 최소 사이트다. GitHub Pages로 배포하며 커스텀 도메인은 `rapt.kr`.

## 구조

- `index.html` — 랜딩 페이지 (직접 수정)
- `404.html` — GitHub Pages가 자동으로 서빙하는 404 페이지 (직접 수정)
- `content/terms.md`, `content/privacy.md` — 이용약관·개인정보처리방침 **원본**. 내용을 바꿀 땐 이 파일만 수정한다.
- `scripts/build.py`, `scripts/template.html` — `content/*.md` → `terms/index.html`, `privacy/index.html` 변환기. 페이지 공통 `<head>`(메타·파비콘 등)를 바꾸려면 `template.html`을 고치고 `python3 scripts/build.py`를 다시 실행한다 — `index.html`, `404.html`은 별도 문서라 템플릿을 안 쓰므로 같은 변경을 직접 반영해야 한다.
- `assets/` — 파비콘(`favicon-32`, `apple-touch-icon-180`, `site-icon-192/512`), OG 이미지, 공용 CSS(`site.css`)
- `manifest.json` — 웹 앱 매니페스트. `assets/site-icon-192.png`, `site-icon-512.png`를 참조해 Android/PWA 홈 화면 추가를 지원한다.
- `robots.txt`, `sitemap.xml` — 크롤러용. 페이지를 추가/제거하면 `sitemap.xml`의 `<url>` 목록도 같이 갱신한다.
- `CNAME` — GitHub Pages 커스텀 도메인 설정 파일 (내용: `rapt.kr`, 건드리지 말 것)

## 약관/방침 내용을 업데이트하는 방법

1. `content/terms.md` 또는 `content/privacy.md`를 수정한다.
2. `python3 scripts/build.py` 실행 → `terms/index.html`, `privacy/index.html`이 재생성된다.
3. 변경 사항을 커밋하고 `main`에 푸시하면 GitHub Pages가 자동 재배포한다.

`terms/index.html`, `privacy/index.html`은 빌드 산출물이므로 직접 편집하지 않는다.

## 배포 (최초 1회 설정)

1. GitHub에 이 저장소를 **public**으로 새로 만들고 푸시한다. (Pages 무료 요금제는 public 저장소만 지원)
2. 저장소 Settings → Pages → Build and deployment → Source: `Deploy from a branch`, Branch: `main` / `root`.
3. 같은 화면의 Custom domain에 `rapt.kr` 입력 후 저장 (이미 저장소에 있는 `CNAME` 파일과 일치해야 함).
4. 도메인 등록기관(도메인을 구매한 곳)의 DNS 설정에서 아래 레코드를 추가:
   - `A` 레코드 4개, 호스트 `@` (또는 루트), 값:
     - 185.199.108.153
     - 185.199.109.153
     - 185.199.110.153
     - 185.199.111.153
   - (선택) `www` 서브도메인을 쓰려면 `CNAME` 레코드, 호스트 `www`, 값 `<github-username>.github.io`
5. DNS 전파 후 GitHub Pages 설정 화면에서 "Enforce HTTPS"를 켠다.
