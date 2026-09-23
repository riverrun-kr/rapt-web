# rapt.kr

Rapt(Threads 특화 미니멀 글쓰기 앱)의 공개 웹사이트. GitHub Pages로 배포하며 커스텀 도메인은 `rapt.kr`. 네 가지 일을 한다 — 제품 소개(랜딩), 출시에 필요한 공개 문서 게시, 앱 안에서 링크로 닿을 문서 제공, Threads OAuth 리디렉션 중계.

## 페이지와 그 페이지가 존재하는 이유

문서 페이지는 "있으면 좋은 것"이 아니라 대부분 **바깥에서 요구해서 생긴 것**이다. 지우거나 경로를 바꾸기 전에 아래를 확인할 것.

| 경로 | 왜 있나 |
| --- | --- |
| `/` | 제품 소개. 출시 전까지 "출시 준비 중" 배지 |
| `/support/` | **App Store Connect의 Support URL은 필수 입력**이고 실제로 연락이 닿아야 한다. "준비 중" 페이지나 깨진 링크는 리젝 사유 |
| `/terms/` | 이용약관 |
| `/privacy/` | 개인정보처리방침. Meta App Review 제출물이기도 하다 |
| `/data-deletion/` | **Meta 앱 Basic Settings가 "데이터 삭제 콜백 URL" 또는 "데이터 삭제 안내 URL" 중 하나를 요구**한다. Rapt는 운영자 서버에 아무것도 저장하지 않아 콜백을 만들 이유가 없어서 안내 URL로 간다 |
| `/licenses/` | 번들 서체 4종이 전부 SIL OFL이라 고지가 의무. 이 웹사이트도 Bodoni를 직접 서빙하므로 웹 자신에게도 필요하다 |
| `/threads-callback/` | Meta OAuth 중계. `noindex` |
| `/en/*` | 위 문서 5종의 영문판. **Meta App Review 제출용이 1차 목적** — 소명문은 영문인데 제출하는 URL이 한국어 전용이면, 심사관이 권한 요청의 근거를 읽지 못한다 |

### ⚠️ 이 경로들은 이제 앱이 하드코딩한 계약이다

**출시된 앱이 아래 네 경로를 문자열로 들고 있다. 옮기거나 지우기 전에 앱을 먼저 볼 것** — 웹에서 경로만 바꾸면 이미 사용자 기기에 설치된 앱의 링크가 조용히 깨지고, 그건 앱 업데이트로만 고쳐진다.

| 경로 | 앱에서 참조하는 곳 |
| --- | --- |
| `/terms/` | `Rapt/AboutView.swift` (설정 → 정보) |
| `/privacy/` | `Rapt/AboutView.swift` |
| `/support/` | `Rapt/AboutView.swift`, `Rapt/RaptApp.swift` (mac 도움말 메뉴) |
| `/threads-callback/` | `Rapt/ThreadsAuth.swift` (OAuth redirect URI, Meta 콘솔에도 등록돼 있다) |

방향이 2026-09-18 기록과 반대로 뒤집혔다. 그때는 "웹이 섰으니 앱이 링크를 걸면 된다"였고, 지금은 걸렸다 — 이제 **웹이 앱에 대해 하위 호환을 진다.**

## 언어 — 한국어가 루트, 영문은 `/en/`

**문서 5종은 2026-09-23에 영문판이 올라갔다**(`/en/terms/` 등). 한국어가 루트를 계속 차지하고 영문이 `/en/` 아래로 들어간다.

서브도메인·쿼리스트링이 아니라 하위 경로인 이유: GitHub Pages는 정적이라 `Accept-Language` 협상도 서버 리디렉션도 못 한다. 서브도메인은 DNS·인증서가 따로 붙고, 쿼리스트링은 검색엔진이 같은 페이지로 본다.

- **원문은 한국어다.** 영문 각 페이지 머리말에 "한국어판이 정본"을 명시해뒀다 — 약관 10조의 준거법이 대한민국 법령이라, 번역본이 정본 행세를 하면 안 된다. **한국어를 고치면 영문도 같이 고친다.**
- `build.py`의 `DOCS`가 `lang`·`alt`를 들고 있고, 템플릿은 그걸로 `<html lang>`·`hreflang`·푸터·언어 전환 링크를 찍는다. 템플릿은 **한 벌뿐이다** — 언어별로 복제하지 말 것(복제하면 반드시 한쪽만 고쳐진다).
- 푸터 문서 목록은 **같은 언어 안에서만** 이동한다. 언어를 건너는 이동은 푸터 맨 아래 전환 링크 하나가 맡는다.
- `hreflang`의 `x-default`는 한국어(루트)를 가리킨다.

**랜딩(`/`)과 `404.html`은 아직 한국어 전용이다** — `/en/` 랜딩은 만들지 않았다. 영문 페이지의 워드마크를 누르면 한국어 랜딩으로 간다. 영문 진입점은 제출된 URL 자체라 지금은 문제가 아니지만, 영문 마켓을 열면 그때 다시 볼 자리다.

## 출시 시점에 갈아끼울 것

`index.html`에 `출시 교체 지점` 주석으로 표시해뒀다.

- ① 랜딩의 "출시 준비 중" 배지 → App Store 링크
- ② 스크린샷 자리 — 지원 기기 범위 확정(앱 `HANDOFF.md` §7 2단계) 이후
- ③ `content/terms.md`·`content/privacy.md` 머리말의 "최종 개정 · 앱 출시 전" → 정식 시행일
- ④ `index.html`의 `description`·`og:description` 출시 후 문구
- ~~⑤ `/support/`에 노출할 연락 수단 범위~~ — **닫힘(2026-09-23).** `support@rapt.kr` 하나로 확정, 사이트 전체가 이 주소를 쓴다

## 디자인 언어 — 앱을 따라간다

**색·서체·간격을 여기서 새로 정하지 않는다.** 값의 출처는 앱이고, 이 저장소는 그걸 베껴 쓰는 쪽이다.

- 색 — `Rapt/Rapt/Assets.xcassets/*.colorset`의 sRGB 값. `assets/site.css`의 CSS 변수 이름을 컬러셋 이름과 1:1로 맞춰뒀다(`--canvas` ↔ `RaptCanvas`). 2026-09-08에 앱이 브랜드 컬러(태운 오렌지)를 제거하고 종이+잉크 단색으로 갔으므로, 웹에도 강조색이 없다. 남은 색은 500자 초과 경고(`--overflow-*`) 하나뿐이다.
- 서체 — **사이트 전체가 "앱이 말하는 목소리"다(2026-09-23 전환).** 라틴은 워드마크 폰트(Bodoni Moda 500 · opsz 11), 한글은 명조(Nanum Myeongjo). 폰트 스택 맨 앞에 Bodoni를 두면 한글엔 글리프가 없어 자동으로 명조로 떨어진다.

  앱 규칙은 "UI·본문은 시스템 산세리프"인데, **그 규칙의 이유는 사용자가 쓴 글에 목소리를 부여하지 않기 위해서**다 — 보호할 사용자 글이 화면에 있을 때 성립한다. rapt.kr에는 사용자 콘텐츠가 한 글자도 없다. 앱 안에서 같은 조건인 화면(`AboutView`)은 라벨도 본문도 링크도 전부 명조다. 그래서 명조 전환은 규칙 위반이 아니라 규칙을 제대로 적용한 것이다.

  **문서 문법도 `AboutView`에서 가져왔다**: 구분선(위 56 / 아래 36) → 라벨(12px) → 본문. 섹션 제목을 키우는 대신 **구분선이 구조를 진다.**

  웹이 정한 값 3개(앱에 대응이 없거나 매체가 달라 조정한 것) — 본문 17px(명조는 x-height가 작아 16px로는 작게 읽힌다), 라벨 잉크 ink-2(폰 3배 밀도와 달리 데스크톱에선 ink-3 디도네 헤어라인이 사라진다), 영문 페이지 측정 폭 560px(디도네는 줄이 길면 행을 놓친다).
- 강조(`<strong>`)는 **굵기가 아니라 잉크**다. 명조는 wght@400 하나만 받고 Bodoni는 Medium 단일이라 `font-weight`를 올리면 둘 다 브라우저 합성 굵기가 되고, 디도네 헤어라인은 거기서 특히 잘 뭉개진다. ink-2 → ink로 올리는 것이 앱의 "강조는 색이 아니라 잉크로 말한다"와도 같다.
- 앱의 네 번째 서체인 IBM Plex Mono는 **일부러 쓰지 않는다**. 모노엔 한글 글리프가 없어 한글을 넣으면 그 부분만 시스템 폰트로 대체되고 모노 metric만 남아 자간이 뜬다(앱이 2026-09-11에 고친 문제). 이 사이트의 메타 자리는 전부 한글이다.
- 아이콘·OG 이미지 — 원본은 `Rapt/Design_method/rapt-brand-assets/layers-bodoni/`. 재생성 방법은 아래 참고.

## 구조

- `index.html` — 랜딩 페이지 (직접 수정). 기능 설명 문구는 **최신 빌드에 실제로 있는 것만** 적는다 — 앱 쪽 `HANDOFF.md`는 일부 절이 낡아 있으므로, 애매하면 코드(`Rapt/Rapt/Item.swift`, `DesignTokens.swift`)를 근거로 삼는다.
- `404.html` — GitHub Pages가 자동으로 서빙하는 404 페이지 (직접 수정)
- `content/*.md` — 문서 페이지 **원본**(약관·방침·지원·데이터 삭제·라이선스), `content/en/*.md`가 그 영문판. 내용을 바꿀 땐 이 파일만 수정한다. 페이지를 추가하려면 `content/`에 md를 넣고 `build.py`의 `DOCS`에 한 줄 더하면 된다 — **`sitemap.xml`은 따라온다**(아래).
- `scripts/build.py`, `scripts/template.html` — `content/*.md` → `{slug}/index.html` 변환기 + `sitemap.xml` 생성기. 지원하는 마크다운은 `# `/`## `/`> `/`- `/문단/`**굵게**`/`[링크](주소)`뿐이다 — 문서가 쓰는 문법을 넘어서면 **원문이 그대로 화면에 나간다**(링크·목록 둘 다 실제로 그렇게 새어 나간 적이 있다). 페이지 공통 `<head>`(메타·파비콘 등)를 바꾸려면 `template.html`을 고치고 `python3 scripts/build.py`를 다시 실행한다 — `index.html`, `404.html`은 별도 문서라 템플릿을 안 쓰므로 같은 변경을 직접 반영해야 한다.
- `assets/` — 파비콘(`favicon-16/32`, `apple-touch-icon-180`, `site-icon-192/512`), OG 이미지(`og-1200x630.png`), 공용 CSS(`site.css`), 자체 호스팅 워드마크 폰트(`fonts/`)
- `manifest.json` — 웹 앱 매니페스트. `assets/site-icon-192.png`, `site-icon-512.png`를 참조해 Android/PWA 홈 화면 추가를 지원한다.
- `threads-callback/index.html` — Meta OAuth 리디렉션 중계. Meta는 HTTPS `redirect_uri`만 허용해서 여기로 먼저 돌아온 뒤 쿼리스트링을 `rapt://threads-auth`로 넘긴다(앱 쪽 `Rapt/ThreadsAuth.swift`). `noindex`라 sitemap에 넣지 않는다.
- `robots.txt` — 크롤러용. 손으로 관리한다.
- `sitemap.xml` — **`build.py`가 생성한다. 직접 고치지 말 것.** 목록은 `DOCS`에서 뽑고, `lastmod`는 원본 파일의 마지막 커밋 날짜(아직 안 올린 수정이 있으면 오늘)를 git에서 읽는다. 손으로 관리하던 2026-09-18~23 사이에 실제로 값이 틀어져 있었다(9/22 변경이 9/18 날짜를 달고 있었다) — 사람이 기억해야 하는 값이라 빠진 것이라, 기억을 없애는 쪽으로 고쳤다. 파일 mtime이 아니라 git을 근거로 삼는 이유는 clone하면 mtime이 체크아웃 시각으로 뭉개지기 때문이다.
- `CNAME` — GitHub Pages 커스텀 도메인 설정 파일 (내용: `rapt.kr`, 건드리지 말 것)

## 약관/방침 내용을 업데이트하는 방법

1. `content/terms.md` 또는 `content/privacy.md`를 수정한다.
2. `python3 scripts/build.py` 실행 → `terms/index.html`, `privacy/index.html`이 재생성된다.
3. 변경 사항을 커밋하고 `main`에 푸시하면 GitHub Pages가 자동 재배포한다.

`terms/index.html`, `privacy/index.html`은 빌드 산출물이므로 직접 편집하지 않는다.

## 아이콘·OG 이미지를 다시 만드는 방법

앱 아이콘이 바뀌면 웹 에셋도 같이 갱신해야 한다(2026-09-11 이전엔 두 세대 뒤처져 있었다 — 어두운 사각형 + Newsreader "Rapt" 전체 워드마크였고, OG 이미지엔 이미 제거된 태운 오렌지 점이 남아 있었다).

- **파비콘 5종** — 원본은 `rapt-brand-assets/layers-bodoni/icon-light-1024.png`(opsz 11)와 `icon-light-small-1024.png`(opsz 6). 32px 이하 슬롯은 헤어라인이 사라지므로 반드시 opsz 6 판을 쓴다. `apple-touch-icon-180.png`는 iOS가 스스로 마스킹하므로 **미리 라운딩하지 않는다**(이중 라운딩 문제). 나머지는 22.37% 라운딩.
- **OG 이미지** — `assets/og-1200x630.png`. 종이 배경(`#F6F3EE`) 위에 Bodoni 워드마크 + 명조 리드 문장. 폰트 실물은 `Rapt/Rapt/Fonts/`에 있다. **내용을 바꾸면 파일 이름도 바꾼다** — 스크래퍼(Threads·카카오톡 등)는 URL 기준으로 오래 캐시하고 쿼리스트링을 떼고 보는 곳도 있어서, 이름을 그대로 두면 옛 이미지가 계속 나간다.
- **워드마크 폰트** — `assets/fonts/BodoniModa11pt-Medium-latin.woff2`. 앱이 번들하는 `Rapt/Rapt/Fonts/BodoniModa11pt-Medium.ttf`를 라틴만 남겨 줄인 것(12KB)이라 글자꼴이 앱 아이콘 글리프와 정확히 같다. 이건 정적 인스턴스라 opsz·weight가 이미 구워져 있다 — CSS에서 `font-variation-settings`를 걸지 말 것. **OFL 폰트를 웹에서 직접 배포하는 것이므로 `assets/fonts/OFL.txt`(라이선스 원문)를 같이 올려둬야 한다** — 폰트 파일만 빼고 올리면 라이선스 위반이다.

## 캐시 무효화 — 에셋을 고쳤으면 반드시

GitHub Pages는 모든 파일에 `Cache-Control: max-age=600`을 붙인다. CSS를 고쳐 배포해도 직전 10분 안에 그 파일을 받아간 브라우저는 재검증 없이 옛 CSS를 쓰기 때문에, **새 HTML + 옛 CSS** 조합으로 레이아웃이 통째로 깨져 보인다(2026-09-11에 실제로 겪음).

`assets/` 안의 무언가를 고쳤으면 순서대로:

```
python3 scripts/stamp_assets.py   # 에셋 URL에 내용 해시를 붙인다
python3 scripts/build.py          # 그 template으로 terms/privacy 재생성
```

`stamp_assets.py`를 **먼저** 돌려야 한다 — 이 스크립트가 `template.html`을 고치고 `build.py`가 그 template을 쓴다.

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
