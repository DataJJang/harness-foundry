# Agent Roles

이 디렉토리는 agentic engineering을 위해 역할을 분리할 때 쓰는 기준 역할군, 책임, 입력/출력, handoff 규칙을 정의한다.

## 사용 원칙

- 역할은 사람 조직도보다 `agentic runtime responsibility` 기준으로 본다.
- 한 사람 또는 한 agent가 여러 역할을 겸할 수는 있지만, 책임과 산출물은 분리해 기록한다.
- 프로젝트 패밀리별 필수 역할은 [`project-selection-mapping.md`](../project-selection-mapping.md)를 따른다.
- 역할 배정은 [`agent-role-selection.md`](../../../checklists/agent-role-selection.md), 역할 간 인수인계는 [`agent-handoff.md`](../../../checklists/agent-handoff.md)를 함께 쓴다.
- 상위 설계 이후 실행 단계에서는 `.agent-base/agent-workboard.json`과 `docs/ai/agent-handoff-log.md`를 같이 쓴다.
- 모델 정책은 벤더 중립적인 `economy`, `standard`, `high-reasoning` tier로만 기록하고, 실제 모델명 매핑은 도구 adapter에서만 한다.
- 생성된 저장소의 `.agent-base/model-routing.json`은 역할, refinement module, execution lane별 권장/최소 tier를 담는다.

## Coordination Mode Baseline

- `Lite`
  - 한 사람 또는 작은 팀이 `runtime-engineer`, `qa-validator`, `docs-operator`를 겸해도 된다.
  - `orchestrator`와 `bootstrap-planner`는 문서 기준 역할로만 두고 실제 handoff artifact는 최소화한다.
- `Coordinated`
  - `orchestrator`, `runtime-engineer`, `qa-validator`, `docs-operator`를 기본으로 두고, `data-steward`와 `security-reviewer`는 조건부로 켠다.
  - execution lane, first handoff packet, high-priority refinement를 명시적으로 맞춘다.
- `Full`
  - core roles를 명시적으로 유지하고 `release-manager`, `solution-architect` 같은 extended role을 실제 흐름에 올린다.
  - shared delivery 전에는 owner, validator, docs owner, packet freshness를 모두 설명 가능해야 한다.

## Core Roles

기본적으로 먼저 확정하는 역할군이다.

| 역할 | 핵심 책임 | 주로 필요한 경우 | 권장/최소 tier |
| --- | --- | --- | --- |
| `orchestrator` | 전체 순서, 역할 배정, handoff 관리 | multi-agent 작업, 변경 영향이 큰 작업 | `standard / economy` |
| `bootstrap-planner` | bootstrap, spec, template, scaffold 확정 | 새 프로젝트, 새 저장소 도입 | `standard / economy` |
| `runtime-engineer` | 실제 코드/설정 구현 | 모든 구현 작업 | `standard / standard` |
| `data-steward` | DB naming, migration, verification, rollback | schema/data/query 변경 | `high-reasoning / standard` |
| `security-reviewer` | 인증, 권한, secret, 위험작업 검토 | 보안/운영 노출이 있는 작업 | `high-reasoning / standard` |
| `qa-validator` | build/test/smoke/stage validation | 모든 공유 전달 전 | `standard / economy` |
| `docs-operator` | README, runbook, manual, checklist 갱신 | 운영/배포/사용 흐름 영향이 있는 작업 | `economy / economy` |

## Extended Roles

조건이 생길 때만 추가하는 역할군이다.

| 역할 | 핵심 책임 | 주로 필요한 경우 | 권장/최소 tier |
| --- | --- | --- | --- |
| `product-analyst` | 목적, 범위, 사용자 가치 정리 | 신규 기능, 신규 프로젝트, 요구사항 불명확 | `standard / economy` |
| `solution-architect` | 경계, 아키텍처, 기술선정 | 구조 결정, 큰 리팩터링, 신규 서비스 | `high-reasoning / standard` |
| `release-manager` | rollout, rollback, 배포 점검 | 배포/운영 영향이 큰 작업 | `high-reasoning / standard` |
| `failure-curator` | 실패 수집과 harness 강화 | 반복 실패, 규약 갭 발견 | `standard / economy` |
| `legacy-analyst` | 기존 저장소 구조, 명령, 제약, docs gap 파악 | brownfield onboarding | `standard / economy` |
| `migration-planner` | 전환 단계, parity, cutover 순서 정의 | migration, replatform | `high-reasoning / standard` |
| `compatibility-reviewer` | 현재/목표 스택 호환성, breaking point 검토 | framework upgrade, stack migration | `high-reasoning / standard` |
| `refactor-guardian` | 구조 정리 중 behavior drift 통제 | large refactor, modularization | `high-reasoning / standard` |
| `cutover-manager` | cutover, rollback, 운영 점검 실행 기준 관리 | phased rollout, shadow, cutover | `high-reasoning / standard` |

## Model Tier Rule

- `economy`
  - 문서 정리, inventory 추출, 고정 포맷 전환, 낮은 리스크의 보정 작업
- `standard`
  - 일반 구현, bootstrap 정리, 검증 계획, 보통 수준의 리팩터링
- `high-reasoning`
  - production 설계, data/security/release 판단, migration, compatibility 검토

현재 tier가 권장보다 낮아도 항상 실패로 보지는 않는다. 다만 minimum 아래로 내려가면 산출물 품질 하한이 흔들릴 가능성이 크므로 상위 tier reviewer나 추가 검증을 붙이는 편이 안전하다.
현재 tier가 권장보다 높으면 품질 문제보다 비용/토큰 과사용 가능성을 먼저 점검한다.

## Runtime Engineer Specializations

`runtime-engineer`는 아래 specialization으로 구체화한다.

- `frontend`
- `api`
- `batch`
- `receiver`
- `game`
- `mobile`
- `tooling`

프로젝트 패밀리와 runtime role에 맞춰 specialization을 붙여 쓴다. 예: `runtime-engineer[api]`, `runtime-engineer[game]`

## 읽는 순서

1. [`orchestrator.md`](./orchestrator.md)
2. core role 중 현재 작업에 필요한 문서
3. extended 역할이 필요할 때만 해당 문서
4. [`../prompts/roles/README.md`](../prompts/roles/README.md)
5. [`../../../checklists/agent-role-selection.md`](../../../checklists/agent-role-selection.md)
6. [`../../../checklists/agent-handoff.md`](../../../checklists/agent-handoff.md)
7. [`../../../checklists/agent-completion-review.md`](../../../checklists/agent-completion-review.md)
