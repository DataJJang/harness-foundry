# harness-foundry

`harness-foundry`는 새 프로젝트를 시작하거나 기존 저장소에 AI 작업 규칙을 이식할 때 사용하는 `프로젝트 생성 킷 + 규칙 템플릿 + agentic engineering base pack`이다.

이 패키지는 단순 scaffold 모음이 아니라 아래를 한 세트로 제공한다.

- 대화형 프로젝트 bootstrap 인터뷰
- 정규화된 project generation spec
- 기존 저장소 inventory와 adoption spec
- 프로젝트 패밀리와 runtime role 기준의 템플릿 선택 규칙
- 샘플 저장소 generator와 scaffold
- 저장 전 자동 검사를 위한 pre-commit hook pack
- 실패 기록과 harness 강화 환류 루프
- 역할 기반 agentic engineering 문서와 역할별 prompt library
- brownfield migration, compatibility, parity, cutover 기준

## 무엇을 할 수 있나

- 새 프로젝트를 인터뷰 형식으로 시작해 생성 spec을 확정한다.
- `game`, `web-app`, `pwa`, `mobile-app`, `backend-service`, `batch-worker`, `receiver-integration`, `mockup-local`, `library-tooling` 패밀리 중 하나를 기준으로 템플릿을 고른다.
- 지원되는 언어/프레임워크 조합이면 최소 실행 가능한 샘플 저장소를 별도 디렉토리에 생성한다.
- 생성된 저장소 안에 `AGENTS.md`, `docs/ai/*`, 체크리스트, prompt 예시, pre-commit 설정을 같이 넣어 첫 build/test/문서화까지 이어갈 수 있게 한다.
- 필요하면 `orchestrator`, `runtime-engineer`, `data-steward`, `security-reviewer`, `qa-validator`, `docs-operator` 같은 역할로 Agent를 나눠 agentic workflow를 설계할 수 있다.
- 기존 저장소에는 `legacy-analyst`, `migration-planner`, `compatibility-reviewer`, `cutover-manager` 역할을 추가해 adoption/migration 흐름을 설계할 수 있다.

## 이 패키지의 핵심 개념

### 1. Project Family

상위 분류는 서비스 유형이 아니라 `프로젝트 패밀리`다.

- `game`
- `web-app`
- `pwa`
- `mobile-app`
- `backend-service`
- `batch-worker`
- `receiver-integration`
- `mockup-local`
- `library-tooling`

### 2. Runtime Role

`frontend`, `api`, `batch`, `receiver`, `client`, `tooling`, `worker`는 상위 패밀리를 대체하지 않는 하위 아키텍처 라벨이다.

### 3. Agentic Role

구현과 검증, 문서화를 명확히 분리하기 위해 역할 기반 흐름을 지원한다.

core roles:

- `orchestrator`
- `bootstrap-planner`
- `runtime-engineer`
- `qa-validator`
- `docs-operator`
- `data-steward`
- `security-reviewer`

extended roles:

- `product-analyst`
- `solution-architect`
- `release-manager`
- `failure-curator`
- `legacy-analyst`
- `migration-planner`
- `compatibility-reviewer`
- `refactor-guardian`
- `cutover-manager`

역할별 책임과 handoff 규칙은 [`source/docs/ai/roles/README.md`](./source/docs/ai/roles/README.md) 에 정리돼 있다.

### 4. Collaboration Depth

같은 규칙 팩이라도 모든 저장소가 같은 절차 깊이를 강제하지는 않는다.

기본 원칙은 가장 가벼운 모드로 시작하고, shared ownership, DB/security risk, release coordination이 생길 때만 한 단계씩 올리는 것이다.

- `Lite`
  - local-first, low-risk, 1인 또는 소규모 시작 경로
  - blocking refinement와 첫 build/test만 먼저 본다
- `Coordinated`
  - DB, security, integration, shared handoff가 있는 기본 협업 경로
  - refinement, workboard, first execution handoff를 맞춘다
- `Full`
  - production, monorepo/multi-repo, release/rollback, schema ownership처럼 coordination cost가 큰 경로
  - role plan, workboard, packet freshness를 기본 절차로 쓴다

generator는 생성된 root `README.md`와 `.agent-base/context-manifest.json`에 추천 mode와 이유를 같이 남긴다.

## 패키지 구조

- `source/`
  - canonical authoring source
  - generator, scaffold, 공통 규칙, 역할 문서, prompt, 예시가 여기서 관리된다
- `templates/`
  - 실제 저장소 루트에 바로 복사 가능한 완성형 템플릿
  - `source/`와 `template-build.json`에서 생성되는 generated artifact다
  - 프로젝트 패밀리 템플릿과 runtime role 템플릿이 함께 있다
- `template-build.json`
  - template별 keep/prune 규칙
  - 어떤 `.cursor` rule과 `.github` instruction을 남길지 선언한다
- `template_overlays/`
  - 공통 베이스만으로 표현할 수 없는 template별 차이를 두는 선택형 overlay
- `tools/build_templates.py`
  - `source/`를 바탕으로 `templates/*`를 다시 생성하는 maintenance script
- `checklists/`
  - 도입, 유지보수, 드리프트 점검용 체크리스트

## 시작 순서

### 새 프로젝트 bootstrap

1. [`source/AGENTS.md`](./source/AGENTS.md)
2. [`source/docs/ai/context-profiles.md`](./source/docs/ai/context-profiles.md)
3. [`source/docs/ai/start-bootstrap.md`](./source/docs/ai/start-bootstrap.md)
4. [`source/docs/ai/project-selection-mapping.md`](./source/docs/ai/project-selection-mapping.md)
5. [`source/docs/ai/roles/README.md`](./source/docs/ai/roles/README.md)

그 다음에만 deep path로 확장한다.

- [`source/docs/ai/project-bootstrap-cli.md`](./source/docs/ai/project-bootstrap-cli.md)
- [`source/docs/ai/project-generation-spec.md`](./source/docs/ai/project-generation-spec.md)
- [`source/docs/ai/project-generator.md`](./source/docs/ai/project-generator.md)
- [`source/docs/ai/stack-matrix.md`](./source/docs/ai/stack-matrix.md)
- 필요 시 [`source/docs/ai/database-rules.md`](./source/docs/ai/database-rules.md)

### 기존 저장소 adoption / migration

1. [`source/AGENTS.md`](./source/AGENTS.md)
2. [`source/docs/ai/context-profiles.md`](./source/docs/ai/context-profiles.md)
3. [`source/docs/ai/start-adoption.md`](./source/docs/ai/start-adoption.md)
4. [`source/docs/ai/repository-inventory.md`](./source/docs/ai/repository-inventory.md)
5. [`source/docs/ai/project-selection-mapping.md`](./source/docs/ai/project-selection-mapping.md)
6. [`source/docs/ai/roles/README.md`](./source/docs/ai/roles/README.md)

그 다음에만 migration deep path로 확장한다.

- [`source/docs/ai/project-adoption.md`](./source/docs/ai/project-adoption.md)
- [`source/docs/ai/adoption-spec.md`](./source/docs/ai/adoption-spec.md)
- [`source/docs/ai/migration-strategy.md`](./source/docs/ai/migration-strategy.md)
- [`source/docs/ai/compatibility-matrix.md`](./source/docs/ai/compatibility-matrix.md)
- [`source/docs/ai/parity-validation.md`](./source/docs/ai/parity-validation.md)

## Context Loading 원칙

- 시작할 때는 필요한 문서만 읽는다.
- 먼저 `core roles`만 확정한다.
- `extended roles`는 migration, cutover, release, repeated failure 같은 조건이 생길 때만 추가한다.
- simple 작업에는 bootstrap/adoption 문맥을 동시에 얹지 않는다.

## Agentic Workflow 예시

기본 추천 흐름은 아래와 같다.

```text
사용자 요청
  -> orchestrator
  -> bootstrap-planner / product-analyst
  -> solution-architect
  -> runtime-engineer
  -> data-steward / security-reviewer
  -> qa-validator
  -> docs-operator
  -> release-manager
  -> failure-curator
```

이 흐름은 프로젝트 패밀리와 변경 범위에 따라 축소하거나 병렬화할 수 있다.

## 프로젝트 패밀리 템플릿

- `game-repo`
- `web-app-repo`
- `pwa-repo`
- `mobile-app-repo`
- `backend-service-repo`
- `batch-worker-repo`
- `receiver-integration-repo`
- `mockup-local-repo`
- `library-tooling-repo`

## Runtime Role 템플릿

- `frontend-repo`
- `api-repo`
- `batch-repo`
- `receiver-repo`

이 role 템플릿은 상위 프로젝트 패밀리를 대체하지 않는다. 생성 후 저장소에 추가 규칙을 얹거나 specialization overlay를 구성할 때 사용한다.

## 실제 생성 예시

```bash
python3 ./source/scripts/project_bootstrap_cli.py \
  --output-root /tmp/generated-projects \
  --force
```

이 명령은 대화형 인터뷰를 진행한 뒤 `/tmp/generated-projects/<repositoryName>` 형태의 샘플 저장소를 만든다.

## 생성된 저장소가 기본으로 받는 것

- root `README.md`
- root `AGENTS.md`
- `docs/ai/*`
- `docs/ai/roles/*`
- `docs/ai/prompts/*`
- `docs/ai/prompts/roles/*`
- `.agent-base/project-generation-spec.json`
- `.agent-base/generation-manifest.json`
- `.agent-base/context-manifest.json`
  - fast/deep path와 추천 coordination mode를 같이 담는다
- `.agent-base/pre-commit-config.json`
- `.agent-base/refinement-manifest.json`
- `.agent-base/refinement-status.json`
- `.agent-base/agent-role-plan.json`
- `.agent-base/agent-workboard.json`
- `docs/ai/repo-local-overrides.md`
- `docs/ai/agent-handoff-packets.md`
- `docs/ai/agent-handoff-log.md`
- `scripts/show_start_path.py`
- `scripts/update_refinement_status.py`
- `scripts/update_agent_workboard.py`
- `.githooks/*`
- `checklists/project-creation.md`
- `checklists/first-delivery.md`
- `checklists/agent-role-selection.md`
- `checklists/agent-handoff.md`
- `checklists/agent-completion-review.md`

## 핵심 원칙

- canonical entry file은 항상 `AGENTS.md`
- 상세 규칙 system of record는 `docs/ai/`
- 생성은 `인터뷰 -> spec -> role selection -> mapping -> generator -> 보정 -> 첫 검증` 순서로 진행
- 언어, 프레임워크, 런타임, DB 규칙은 문서 기준으로 먼저 확정
- 템플릿 복사 후에는 반드시 repo-local 명령과 환경 설정으로 보정
- 템플릿 복사 후에는 local pre-commit hook와 실패 학습 루프를 저장소 운영 기준에 맞게 활성화
- multi-agent로 진행할 때는 역할별 입력, 출력, handoff artifact를 명시한다
- 설계가 끝난 뒤에는 `agent-role-plan`만 보지 말고 `agent-workboard`로 owned path, next handoff, blocker를 고정한다
- planning에서 execution으로 넘어갈 때는 current handoff packet까지 남겨 다음 runner의 시작 기준을 고정한다
- 규칙 변경은 `source/`와 `template-build.json`을 먼저 수정하고 `tools/build_templates.py`로 `templates/*`를 다시 생성한다

## 실행 협업 기준

- `.agent-base/agent-role-plan.json`: 어떤 역할이 필요한지와 기본 순서를 정한다.
- `.agent-base/refinement-status.json`: bootstrap 이후 결정과 defer 상태를 추적한다.
- `.agent-base/agent-workboard.json`: 실제 실행 lane, owned path, blocker, next handoff를 관리한다.
- `docs/ai/handoff-packets/*.md`: 다음 실행 에이전트가 바로 읽을 current contract를 남긴다.
- `docs/ai/agent-handoff-log.md`: 에이전트 간 baton history를 시간순으로 남긴다.
- `.agent-base/coordination.lock`: updater 스크립트가 상태 파일을 직렬화할 때 잡는 공유 잠금 경로다.

권장 흐름은 `update_refinement_status.py`로 high-priority refinement를 정리하고, blocker가 풀리면 `update_agent_workboard.py --finalize-design-freeze`로 첫 execution handoff packet을 만든 뒤, 이후 `update_agent_workboard.py`로 lane과 baton history를 갱신하는 방식이다. 전달 직전에는 `python3 scripts/update_agent_workboard.py --check-packets --strict`로 current packet이 아직 fresh한지 확인한다. 두 updater는 같은 `coordination.lock`을 잡고 JSON/Markdown을 atomic write로 갱신하므로, 같은 저장소에서 동시에 상태를 바꿀 때도 overwrite 위험을 줄인다. 잠금이 오래 잡혀 있으면 `--lock-timeout-seconds`로 fail-fast 하도록 실행할 수 있다.

처음 진입할 때는 생성된 저장소에서 `python3 scripts/show_start_path.py`를 먼저 실행하는 편이 좋다. 이 명령은 추천 coordination mode와 현재 blocker/workboard 상태를 읽고, 지금 바로 할 3가지 액션만 얇게 보여준다.

## Template Authoring 원칙

- `templates/*`는 배포 산출물이며 직접 수정하지 않는다
- 공통 규칙, 문서, 스크립트는 항상 `source/`에서 수정한다
- 템플릿별 차이는 먼저 `template-build.json`의 keep/prune 규칙으로 해결한다
- 그래도 표현할 수 없는 차이만 `template_overlays/<template-name>/`에 둔다

재생성 예시:

```bash
python3 ./tools/build_templates.py
python3 ./tools/build_templates.py --check
```

## 이 패키지가 다루지 않는 것

- 실제 비즈니스 기능 구현
- 완전 자동 제품 수준 스캐폴딩 엔진
- 조직 고유 배포 파이프라인의 세부 절차
- 특정 팀의 사람 조직도와 승인 체계

이런 항목은 생성된 저장소 안에서 repo-local overlay 문서나 추가 스크립트로 확장한다.
