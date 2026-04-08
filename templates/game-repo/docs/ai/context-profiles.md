# Context Profiles

이 문서는 작업 시작 시 어떤 문서를 얼마나 읽어야 하는지 정하는 `context loading guide`다.

## 목적

- 필요한 문맥만 먼저 읽게 한다.
- simple 작업에 brownfield, migration, extended role 문맥이 과하게 섞이지 않게 한다.
- `fast path`와 `deep path`를 분리해 entry layer를 가볍게 유지한다.

## Context Depth vs Coordination Depth

- `fast path` / `deep path`는 문서를 얼마나 읽을지 정하는 축이다.
- `Lite` / `Coordinated` / `Full`은 사람과 agent가 얼마나 강하게 coordination artifact를 쓸지 정하는 축이다.
- generated repo는 `.agent-base/context-manifest.json`에 추천 coordination mode를 남긴다.
- `Lite` 작업도 DB나 rollout 이슈가 생기면 deep path로 확장할 수 있고, `Full` 작업도 시작은 fast path로 가볍게 할 수 있다.

## 기본 원칙

- 항상 `AGENTS.md`부터 시작한다.
- 그 다음에는 현재 작업 모드 하나만 고른다.
  - `bootstrap`
  - `adoption`
  - `delivery`
  - `incident`
- 처음에는 `core roles`만 본다.
- 아래 조건이 생길 때만 `extended roles`와 심화 문서를 연다.

## Fast Path

다음 조건이면 fast path로 시작한다.

- 새 프로젝트 생성
- 단일 기능 추가
- 기존 구조 안에서의 작은 수정
- 배포, cutover, migration, schema ownership이 없는 작업

읽는 순서:

1. `AGENTS.md`
2. `docs/ai/start-bootstrap.md` 또는 `docs/ai/start-adoption.md`
3. `docs/ai/project-selection-mapping.md`
4. `docs/ai/roles/README.md`
5. `docs/ai/governance/quality-gates.md`

## Deep Path

다음 조건이면 deep path로 확장한다.

- framework/runtime migration
- brownfield onboarding
- schema, seed, risky SQL, data correction
- production rollout or rollback planning
- multi-agent handoff가 복잡한 작업
- 반복 실패가 발생한 작업

추가로 읽는 문서:

- `docs/ai/database-rules.md`
- `docs/ai/repository-inventory.md`
- `docs/ai/migration-strategy.md`
- `docs/ai/compatibility-matrix.md`
- `docs/ai/parity-validation.md`
- `docs/ai/governance/pre-commit-hooks.md`
- `docs/ai/governance/agent-failure-learning.md`
- `docs/ai/prompts/roles/README.md`

## Core Roles First

기본으로 먼저 보는 역할:

- `orchestrator`
- `bootstrap-planner`
- `runtime-engineer`
- `qa-validator`
- `docs-operator`

조건부로 바로 추가하는 역할:

- `data-steward`
  - schema, migration, seed, SQL, query ownership
- `security-reviewer`
  - 인증, 권한, 외부 공개, secret, production 보안 영향

## Extended Roles Only When Needed

아래 역할은 필요 조건이 생길 때만 읽는다.

- `product-analyst`
- `solution-architect`
- `release-manager`
- `failure-curator`
- `legacy-analyst`
- `migration-planner`
- `compatibility-reviewer`
- `refactor-guardian`
- `cutover-manager`

## Context Budget

작업 시작 시 한 번에 여는 문서 수를 제한한다.

- 기본 시작:
  - entry 문서 3개 이하
  - 역할 문서 3개 이하
  - 체크리스트 2개 이하
- 심화 작업:
  - 새 문서를 추가할 때는 기존 문서 중 현재 단계와 무관한 것은 닫는다.

## 권장 시작 조합

- 새 프로젝트 bootstrap:
  - `AGENTS.md`
  - `docs/ai/start-bootstrap.md`
  - `docs/ai/project-selection-mapping.md`
  - `docs/ai/roles/README.md`
- 기존 프로젝트 adoption:
  - `AGENTS.md`
  - `docs/ai/start-adoption.md`
  - `docs/ai/repository-inventory.md`
  - `docs/ai/project-selection-mapping.md`
- 구현/전달:
  - `AGENTS.md`
  - 관련 서비스 문서 1개
  - `docs/ai/governance/quality-gates.md`
  - 필요한 체크리스트 1~2개
