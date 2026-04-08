# Model Routing

이 문서는 역할, refinement module, execution lane별로 어떤 AI model tier를 권장하는지 정리한다.
canonical 기준은 실제 모델명이 아니라 `economy`, `standard`, `high-reasoning` 세 단계만 쓴다.

## 왜 필요한가

- 간단한 문서 정리나 inventory 수집까지 늘 비싼 모델로 돌릴 필요는 없다.
- 반대로 data, security, release, migration 같은 판단은 낮은 tier에서 놓치는 비용이 더 클 수 있다.
- 그래서 `무조건 최고급 모델`이나 `무조건 저렴한 모델` 대신, 현재 단계에 맞는 tier를 정하고 경고를 주는 편이 낫다.

이 정책은 generated repo의 `.agent-base/model-routing.json`으로 내려간다.
starter helper는 `python3 scripts/show_start_path.py --current-model-tier <tier>`로 현재 tier를 비교해 경고를 보여줄 수 있다.

## Tier 정의

- `economy`
  - 반복형 문서 정리, inventory 추출, 고정 포맷 전환, 낮은 리스크의 보정 작업
- `standard`
  - 일반 구현, bootstrap/spec 정리, command alignment, test plan, 보통 수준의 리팩터링
- `high-reasoning`
  - production 설계, data/security/release 판단, migration, compatibility, cutover

## 기본 원칙

- 역할 문서와 프롬프트 문서에는 실제 모델명 대신 tier만 적는다.
- 실제 모델명 매핑은 `CLAUDE.md`, `GEMINI.md`, Copilot/Cursor 규칙 같은 tool adapter에서만 한다.
- generated repo는 역할별 policy 외에도 refinement module과 execution lane 기준 policy를 같이 저장한다.
- minimum 아래로 내려가면 즉시 경고하고, recommended보다 높으면 비용/토큰 note를 준다.
- 도구가 현재 tier를 모르면 hard enforcement 없이 soft recommendation만 적용한다.

## 권장 적용 범위

- `economy`로 충분한 경우
  - `docs-operator`
  - 단순 inventory, boilerplate alignment, 고정 형식 문서 갱신
- `standard`가 기본인 경우
  - `runtime-engineer`
  - `bootstrap-planner`
  - `orchestrator`
  - `qa-validator`
- `high-reasoning`을 강하게 권장하는 경우
  - `data-steward`
  - `security-reviewer`
  - `solution-architect`
  - `release-manager`
  - `migration-planner`
  - `compatibility-reviewer`
  - `refactor-guardian`
  - `cutover-manager`

production 프로젝트에서는 위 고위험 역할의 minimum도 `high-reasoning`으로 올리는 편을 기본값으로 본다.

## 경고 규칙

- `below-minimum`
  - 현재 tier가 최소 요구보다 낮다.
  - 산출물 품질 하한이 흔들릴 수 있으므로 상위 tier로 올리거나, 상위 tier reviewer와 추가 검증을 붙인다.
- `below-recommended`
  - 최소 기준은 충족하지만 권장보다 낮다.
  - 진행은 가능하되 재작업 가능성을 염두에 두고 verification을 강화한다.
- `above-recommended`
  - 품질은 충분하지만 비용/토큰이 과할 수 있다.
  - 정말 high tier reasoning이 필요한 단계인지 다시 확인한다.

## 즉시 경고를 띄우는 방법

- AI IDE가 현재 tier를 알고 있으면 첫 질의 전에 `.agent-base/model-routing.json`과 비교한다.
- shell helper를 쓸 때는 아래처럼 넘긴다.

```bash
python3 scripts/show_start_path.py --current-model-tier standard
```

- 자동으로 넘기고 싶으면 `HARNESS_MODEL_TIER` 환경변수를 쓸 수 있다.

```bash
HARNESS_MODEL_TIER=high-reasoning python3 scripts/show_start_path.py
```

## 복잡도에 대한 판단

이 정책은 새로운 heavy workflow를 추가하는 것이 아니다.
기본적으로는:

- 문서 한 장
- generated metadata 파일 한 장
- 기존 starter helper의 경고 한 줄

정도만 늘어난다.
즉, coordination artifact를 새로 하나 더 강제하는 구조가 아니라 이미 있는 역할/단계 정보에 tier 힌트를 덧붙이는 수준으로 보는 편이 맞다.
