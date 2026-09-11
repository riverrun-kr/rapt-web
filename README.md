# rapt.kr

Rapt(Threads 특화 미니멀 글쓰기 앱)의 공개 웹사이트. GitHub Pages로 배포하며 커스텀 도메인은 `rapt.kr`. 세 가지 일을 한다 — 제품 소개(랜딩), 이용약관·개인정보처리방침 게시, Threads OAuth 리디렉션 중계.

## 디자인 언어 — 앱을 따라간다

**색·서체·간격을 여기서 새로 정하지 않는다.** 값의 출처는 앱이고, 이 저장소는 그걸 베껴 쓰는 쪽이다.

- 색 — `Rapt/Rapt/Assets.xcassets/*.colorset`의 sRGB 값. `assets/site.css`의 CSS 변수 이름을 컬러셋 이름과 1:1로 맞춰뒀다(`--canvas` ↔ `RaptCanvas`). 2026-09-08에 앱이 브랜드 컬러(태운 오렌지)를 제거하고 종이+잉크 단색으로 갔으므로, 웹에도 강조색이 없다. 남은 색은 500자 초과 경고(`--overflow-*`) 하나뿐이다.
- 서체 — 워드마크는 **Bodoni Moda 500 · opsz 11 · 트래킹 −0.005em**(앱 아이콘 글리프와 같은 활자, 2026-09-09 교체). 명조(Nanum Myeongjo)는 "앱이 말하는 자리"에만. 그 밖의 UI·본문은 시스템 산세리프 — 앱이 사용자의 글에 목소리를 부여하지 않으려고 시스템 폰트를 쓰는 것과 같은 이유다.
- 앱의 네 번째 서체인 IBM Plex Mono는 **일부러 쓰지 않는다**. 모노엔 한글 글리프가 없어 한글을 넣으면 그 부분만 시스템 폰트로 대체되고 모노 metric만 남아 자간이 뜬다(앱이 2026-09-11에 고친 문제). 이 사이트의 메타 자리는 전부 한글이다.
- 아이콘·OG 이미지 — 원본은 `Rapt/Design_method/rapt-brand-assets/layers-bodoni/`. 재생성 방법은 아래 참고.

## 구조

- `index.html` — 랜딩 페이지 (직접 수정). 기능 설명 문구는 **최신 빌드에 실제로 있는 것만** 적는다 — 앱 쪽 `HANDOFF.md`는 일부 절이 낡아 있으므로, 애매하면 코드(`Rapt/Rapt/Item.swift`, `DesignTokens.swift`)를 근거로 삼는다.
- `404.html` — GitHub Pages가 자동으로 서빙하는 404 페이지 (직접 수정)
- `content/terms.md`, `content/privacy.md` — 이용약관·개인정보처리방침 **원본**. 내용을 바꿀 땐 이 파일만 수정한다.
- `scripts/build.py`, `scripts/template.html` — `content/*.md` → `terms/index.html`, `privacy/index.html` 변환기. 페이지 공통 `<head>`(메타·파비콘 등)를 바꾸려면 `template.html`을 고치고 `python3 scripts/build.py`를 다시 실행한다 — `index.html`, `404.html`은 별도 문서라 템플릿을 안 쓰므로 같은 변경을 직접 반영해야 한다.
- `assets/` — 파비콘(`favicon-32`, `apple-touch-icon-180`, `site-icon-192/512`), OG 이미지, 공용 CSS(`site.css`)
- `manifest.json` — 웹 앱 매니페스트. `assets/site-icon-192.png`, `site-icon-512.png`를 참조해 Android/PWA 홈 화면 추가를 지원한다.
- `threads-callback/index.html` — Meta OAuth 리디렉션 중계. Meta는 HTTPS `redirect_uri`만 허용해서 여기로 먼저 돌아온 뒤 쿼리스트링을 `rapt://threads-auth`로 넘긴다(앱 쪽 `Rapt/ThreadsAuth.swift`). `noindex`라 sitemap에 넣지 않는다.
- `robots.txt`, `sitemap.xml` — 크롤러용. 페이지를 추가/제거하면 `sitemap.xml`의 `<url>` 목록도 같이 갱신하고, 약관·방침을 고치면 해당 `lastmod`도 같이 올린다.
- `CNAME` — GitHub Pages 커스텀 도메인 설정 파일 (내용: `rapt.kr`, 건드리지 말 것)

## 약관/방침 내용을 업데이트하는 방법

1. `content/terms.md` 또는 `content/privacy.md`를 수정한다.
2. `python3 scripts/build.py` 실행 → `terms/index.html`, `privacy/index.html`이 재생성된다.
3. 변경 사항을 커밋하고 `main`에 푸시하면 GitHub Pages가 자동 재배포한다.

`terms/index.html`, `privacy/index.html`은 빌드 산출물이므로 직접 편집하지 않는다.

## 아이콘·OG 이미지를 다시 만드는 방법

앱 아이콘이 바뀌면 웹 에셋도 같이 갱신해야 한다(2026-09-11 이전엔 두 세대 뒤처져 있었다 — 어두운 사각형 + Newsreader "Rapt" 전체 워드마크였고, OG 이미지엔 이미 제거된 태운 오렌지 점이 남아 있었다).

- **파비콘 4종** — 원본은 `rapt-brand-assets/layers-bodoni/icon-light-1024.png`(opsz 11)와 `icon-light-small-1024.png`(opsz 6). 32px 이하 슬롯은 헤어라인이 사라지므로 반드시 opsz 6 판을 쓴다. `apple-touch-icon-180.png`는 iOS가 스스로 마스킹하므로 **미리 라운딩하지 않는다**(이중 라운딩 문제). 나머지는 22.37% 라운딩.
- **OG 이미지** — `assets/social-preview-1200x630.png`. 종이 배경(`#F6F3EE`) 위에 Bodoni 워드마크 + 명조 리드 문장. 폰트 실물은 `Rapt/Rapt/Fonts/`에 있다.

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
