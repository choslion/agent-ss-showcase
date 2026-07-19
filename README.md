# SS - 개인 AI 비서 (Chief of Staff)

대화 세션이 바뀌어도 지난 맥락을 이어받고, 목표·할 일·결정을 함께 관리하도록 구성한 **Claude Code 기반 개인 AI 비서**입니다.

- 파일 기반 기억으로 세션 연속성 유지
- 시작·중간 저장·종료 흐름을 슬래시 커맨드로 표준화
- [Stock Pro](https://github.com/choslion/stock-pro) 관심종목 브리핑 선택 연동
- [포트폴리오](https://choslion.github.io/portfolio/)

> 이 저장소는 실제 운영 인스턴스에서 개인정보와 자격증명을 제거한 쇼케이스입니다. 구조와 커맨드는 예시 데이터로 확인할 수 있으며, 새로 시작하려면 [agent-ss-template](https://github.com/choslion/agent-ss-template)을 사용할 수 있습니다.

## 데모

`/start` 한 번으로 이전 세션의 상태를 읽고 오늘의 우선순위와 관심종목 움직임을 브리핑합니다.

https://github.com/user-attachments/assets/b4be8232-35e0-4bcb-ab85-c7fcf385ba6c

재생되지 않으면 [데모 영상](docs/demo.mp4)을 직접 확인할 수 있습니다.

## 해결하려던 문제

일반적인 AI 대화는 세션이 끝나면 이전 결정과 진행 상황을 다시 설명해야 합니다. SS는 대화 내용을 별도 데이터베이스에 숨겨 저장하는 대신, 사용자가 직접 읽고 수정할 수 있는 Markdown 파일에 현재 상태와 세션 기록을 남깁니다.

다음 세션에서는 이 파일들을 먼저 읽어 진행 중이던 작업과 남은 할 일을 이어받습니다. 반복되는 사용 흐름은 `.claude/commands/`의 커맨드로 고정해 매번 같은 방식으로 기록하고 갱신합니다.

## 핵심 기능

- **세션 연속성** — `state/current.md`와 최근 세션 로그를 인수인계 문서로 사용해 지난 작업을 이어갑니다.
- **목표·할 일·결정 관리** — 목표 진행률, 열린 할 일, 결정과 이유를 각각의 파일로 나누어 관리합니다.
- **세션 수명주기 자동화** — `/start`, `/update`, `/end`가 불러오기·중간 저장·종료 기록 절차를 일관되게 수행합니다.
- **선택형 시황 브리핑** — 별도 Stock Pro 저장소의 스크립트를 실행해 국내·미국 관심종목의 주요 움직임을 브리핑에 포함합니다.
- **사용 기록 집계** — 날짜별 로그를 기준으로 총 세션일, 현재·최장 연속 사용일과 이번 달 사용일을 계산합니다.

## 세션 흐름

```text
/start
  ├─ git pull
  ├─ state/ + 최근 sessions/ 읽기
  └─ 현재 상황과 우선순위 브리핑
        ↓
대화 중
  ├─ 새로운 할 일 → state/todos.md
  ├─ 중요한 결정 → state/decisions.md
  └─ /update → 중간 상태 저장
        ↓
/end
  ├─ sessions/YYYY-MM-DD.md 기록
  ├─ state/current.md 갱신
  └─ commit + push로 기억 동기화
```

기억이 일반 파일로 남기 때문에 사용자가 내용을 직접 확인하고 수정·삭제·백업할 수 있습니다. Git을 함께 사용하면 여러 기기에서도 같은 상태를 이어갈 수 있습니다.

## 커맨드

| 커맨드 | 역할 |
|---|---|
| `/start` | 원격 기억을 동기화하고 이전 상태·최근 로그를 읽어 오늘의 우선순위를 브리핑 |
| `/status` | 목표, 열린 할 일, 최근 결정을 10줄 이내로 요약 |
| `/update` | 현재 세션의 진행 상황과 새 할 일을 중간 저장 |
| `/end` | 세션 로그와 상태 파일을 갱신하고 Git으로 백업 |
| `/stocks` | Stock Pro 관심종목의 현재 시황 조회 |
| `/usage` | 총 세션일과 현재·최장 연속 사용일 집계 |
| `/help` | 사용 가능한 커맨드 안내 |

## 구조

```text
agent-ss-showcase/
├─ CLAUDE.md              # 비서의 역할·원칙·세션 규칙
├─ .claude/commands/      # start·status·update·end 등 커맨드 정의
├─ profile/me.md          # 사용자 정보와 선호 대화 방식
├─ state/
│  ├─ current.md         # 다음 세션이 읽는 현재 상태
│  ├─ goals.md           # 장기 목표와 진행률
│  ├─ todos.md           # 할 일 목록
│  └─ decisions.md       # 결정과 이유
├─ sessions/              # 날짜별 세션 로그
├─ scripts/
│  └─ usage_stats.py     # 표준 라이브러리 기반 사용 통계
└─ docs/demo.mp4          # 동작 데모
```

## 시작하기

### 쇼케이스 확인

```bash
git clone https://github.com/choslion/agent-ss-showcase.git
cd agent-ss-showcase
```

이 디렉터리를 Claude Code에서 열고 `/start`를 실행하면 예시 상태를 기준으로 흐름을 확인할 수 있습니다.

### 개인 비서로 사용

```bash
git clone https://github.com/choslion/agent-ss-template.git my-agent-ss
cd my-agent-ss
```

1. `profile/me.md`에 역할과 선호 대화 방식을 작성합니다.
2. `state/goals.md`에 장기 목표를 정리합니다.
3. 개인정보가 기록되므로 원격 저장소는 비공개로 설정하는 것을 권장합니다.
4. Claude Code에서 `/start`를 실행합니다.

별도 패키지 설치는 필요하지 않습니다. `/usage`는 Python 3 표준 라이브러리만 사용합니다.

## 선택 연동

### Stock Pro

`.claude/commands/start.md`와 `stocks.md`의 `<path-to>`를 로컬 Stock Pro 경로로 바꾸면 다음 스크립트를 호출할 수 있습니다.

```bash
python <path-to>/stock-pro/scripts/brief_quotes.py --min 1.0
```

Stock Pro가 없거나 외부 시세 요청이 실패하면 브리핑의 해당 단계만 건너뛰도록 구성했습니다.

### 개인 운영 환경

실제 운영 인스턴스에서는 Google Calendar·Notion MCP와 정기 리마인드를 함께 사용합니다. 이 쇼케이스에는 개인정보 보호를 위해 MCP 설정, 자격증명과 스케줄 설정을 포함하지 않았습니다.

## 기술 구성

| 구분 | 구성 |
|---|---|
| 실행 환경 | Claude Code |
| 기억 | Markdown 기반 `profile/`, `state/`, `sessions/` |
| 자동화 | Claude Code 슬래시 커맨드 |
| 보조 스크립트 | Python 3 표준 라이브러리 |
| 동기화 | Git, GitHub |
| 선택 연동 | Stock Pro, Google Calendar·Notion MCP |

## 검증

사용 통계 스크립트는 별도 의존성 없이 실행할 수 있습니다.

```bash
python -m py_compile scripts/usage_stats.py
python scripts/usage_stats.py
```

## 개인정보 및 사용 전 확인

- `profile/`, `state/`, `sessions/`에는 개인 일정과 의사결정이 쌓이므로 공개 저장소 사용을 피하는 편이 안전합니다.
- `/start`는 `git pull`, `/end`는 commit과 push를 수행하도록 정의되어 있습니다. 실제 사용 전 원격 저장소와 변경 범위를 확인하세요.
- 이 저장소의 프로필·상태·세션은 구조 설명을 위한 예시이며 실제 개인 데이터가 아닙니다.
