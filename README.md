# SS - 개인 AI 비서 (Chief of Staff)

[Claude Code](https://claude.com/claude-code)(Claude Agent SDK) 위에 만든 개인 "Chief of Staff" 에이전트입니다.
세션을 넘어 맥락을 기억하고, 목표·할 일을 추적하고, 내가 실제로 쓰는 도구(주식·일정)에 통합해 매일 브리핑합니다.

🔗 포트폴리오: **[choslion.github.io/portfolio](https://choslion.github.io/portfolio/)**

> **이 저장소는 쇼케이스입니다.** 실제 운영 중인 개인 인스턴스에서 개인정보(실제 일정·메모)를 제거하고,
> 구조·커맨드·통합을 보여주기 위해 예시 데이터로 채웠습니다.
> 바로 시작할 수 있는 빈 템플릿은 [agent-ss-template](https://github.com/choslion/agent-ss-template)을 보세요.

## 데모

`/start` 한 번으로 지난 맥락을 이어받아 인사 + 오늘 브리핑(일정·관심종목)을 띄우는 모습입니다.

https://github.com/user-attachments/assets/b4be8232-35e0-4bcb-ab85-c7fcf385ba6c

> 재생이 안 되면 [데모 영상 직접 보기](docs/demo.mp4)

## 한눈에

- **문제** — AI 어시스턴트는 매 세션 맥락을 잃는다.
- **해결** — 파일 기반 기억(`state/` · `sessions/`)으로 세션 연속성을 만들고, 직접 만든 주식 대시보드·구글 캘린더에 통합해 "매일 여는" 비서로 만들었다.
- **차별점** — 튜토리얼 복붙이 아니라 내 실제 워크플로에 통합했고, **매일 실제로 쓴다**(`/usage`로 연속 사용일 집계).

## 주요 기능

- **세션 연속성** — `state/`와 최근 세션 로그를 읽어 매번 이어서 시작. 기억은 전부 일반 파일이라 직접 읽고 고칠 수 있습니다.
- **관심종목 시황 브리핑** — 내 [stock-pro](https://github.com/choslion/stock-pro) 백엔드를 직접 호출해 `/start` 브리핑과 `/stocks`에서 국내·미국 관심종목 시세를 보여줍니다 (서버 안 띄워도 됨).
- **정기 리마인드** — 클라우드 스케줄 루틴이 평일 17:40(KST)에 할 일·일정을 점검하고 알림.
- **사용 통계** — `/usage`가 세션 로그에서 연속 사용일·총 세션일을 계산. "매일 쓴다"는 증거를 정직하게 집계합니다.

## 커맨드

| 커맨드 | 설명 |
|--------|------|
| `/start` | 지난 세션 이어받기 + 오늘 브리핑 (관심종목 무버 포함) |
| `/stocks` | stock-pro 관심종목 현재 시황 (큰 무버 순) |
| `/usage` | 사용 통계 — 총 세션일·연속 사용일 |
| `/update` | 세션 중간 저장 |
| `/status` | 목표·할일·결정 현황 요약 |
| `/end` | 세션 로그 저장 + 상태 갱신 + `git push`로 기억 백업 |
| `/help` | 사용법 안내 |

## 작동 원리

```
agent-ss/
├── CLAUDE.md              # SS의 정체성·원칙·세션 규칙 (매 세션 자동 로드)
├── .claude/commands/      # 슬래시 커맨드 정의 (마크다운)
├── profile/me.md          # 내가 누구인지, 어떤 대화 스타일을 원하는지
├── state/
│   ├── current.md         # 세션 간 인수인계 문서
│   ├── goals.md           # 장기 목표 + 진행률
│   ├── todos.md           # 할 일 목록
│   └── decisions.md       # 결정 기록 (이유 포함)
├── scripts/               # 보조 스크립트 (usage_stats.py 등, 의존성 없음)
└── sessions/              # 날짜별 세션 로그 (YYYY-MM-DD.md)
```

Claude Code는 매 세션 시작 시 `CLAUDE.md`를 자동으로 읽습니다. 거기에 "state/와 최근 세션 로그를
읽고 이어가라"는 지시가 있어 대화가 끊기지 않아요. `/end`가 세션을 디스크에 기록하고 GitHub에 백업합니다.
기억은 전부 그냥 파일이라 직접 읽고, 고치고, 지우고, 백업할 수 있습니다.

## 통합 (차별 포인트)

- **Stock Pro 연동** — [stock-pro](https://github.com/choslion/stock-pro)의 `get_watchlist()`를 파이썬에서 직접
  import해 호출합니다(uvicorn 서버 불필요). 관심종목은 stock-pro의 `watchlist.json` 한 곳에서 관리하고,
  프론트엔드와 SS 브리핑이 같은 소스를 공유합니다.
- **정기 리마인드** — Claude Code 클라우드 스케줄 루틴(cron)이 평일 17:40 KST에 할 일·일정을 점검하고
  앱 푸시로 알립니다.
- **사용 통계** — `scripts/usage_stats.py`가 `sessions/`의 날짜 파일을 파싱해 총 세션일·현재/최장 연속일을
  계산합니다. 의존성 없이 표준 라이브러리만 사용.

## 기술 스택

Claude Agent SDK (Claude Code), Python, MCP (Google Calendar · Notion), GitHub Actions / Routines,
Markdown 기반 파일 메모리.
