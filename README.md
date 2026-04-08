# harness-foundry

`harness-foundry`는 새 프로젝트를 시작하거나 기존 저장소에 AI 작업 규칙을 이식할 때 쓰는 `generator + template pack + agentic engineering base`다.

목표는 scaffold만 찍고 끝내는 것이 아니라, 생성 직후의 `첫 실행`, `첫 검증`, `첫 handoff`까지 바로 이어질 수 있는 기준을 같이 넣는 것이다.

## Start Here

이 README는 전체 설명보다 빠른 진입을 우선한다. 기본 진입점은 `Python 스크립트 실행`보다 `AI IDE 질의`다. 먼저 아래 3개 중 하나만 고르면 된다.

요구사항은 간단하다.

- `AI IDE 문서/질의 기반 사용`
  - Python 없이도 가능
- `generator / helper script / updater / template rebuild`
  - `python3`가 필요

### 1. AI IDE로 새 프로젝트를 시작하고 싶다

AI에게 아래처럼 요청하면 된다.

```text
`source/AGENTS.md`와 `source/docs/ai/start-bootstrap.md`를 읽고,
이 저장소 기준으로 새 프로젝트 bootstrap을 도와줘.
먼저 필요한 질문부터 좁혀서 진행하고,
필요한 경우에만 CLI나 스크립트 실행을 제안해줘.
```

관련 문서:

- [`source/AGENTS.md`](./source/AGENTS.md)
- [`source/docs/ai/start-bootstrap.md`](./source/docs/ai/start-bootstrap.md)
- [`source/docs/ai/prompts/README.md`](./source/docs/ai/prompts/README.md)

### 2. AI IDE로 기존 저장소에 기준을 이식하고 싶다

AI에게 아래처럼 요청하면 된다.

```text
`source/AGENTS.md`와 `source/docs/ai/start-adoption.md`를 읽고,
현재 저장소에 harness-foundry 기준을 도입하기 위한
inventory와 adoption plan부터 잡아줘.
```

이후 필요하면 inventory, migration, compatibility 문서로 확장하면 된다.

- [`source/AGENTS.md`](./source/AGENTS.md)
- [`source/docs/ai/start-adoption.md`](./source/docs/ai/start-adoption.md)
- [`source/docs/ai/repository-inventory.md`](./source/docs/ai/repository-inventory.md)
- [`source/docs/ai/migration-strategy.md`](./source/docs/ai/migration-strategy.md)

### 3. 이미 생성된 저장소를 AI IDE로 바로 진행하고 싶다

생성된 저장소 안에서는 긴 문서보다 아래처럼 요청하는 편이 가장 빠르다.

```text
`AGENTS.md`, `.agent-base/context-manifest.json`,
`.agent-base/refinement-manifest.json`, `.agent-base/model-routing.json`을 읽고
지금 할 3가지 액션과 현재 티어 기준 주의사항만 먼저 정리해줘.
필요하면 `.agent-base/agent-workboard.json`도 같이 봐줘.
```

### 4. CLI로 직접 실행하고 싶다

스크립트 실행은 여전히 지원하지만, 기본 진입점이라기보다 `자동화`, `재현`, `도우미 출력 확인` 용도로 보는 편이 맞다.

```bash
python3 ./source/scripts/project_bootstrap_cli.py \
  --output-root /tmp/generated-projects \
  --force

python3 scripts/show_start_path.py
```

`show_start_path.py`는 현재 저장소의 추천 coordination mode, blocker, workboard 상태를 읽고 지금 바로 할 3가지 액션만 보여주는 optional helper다. 현재 model tier를 알면 `--current-model-tier standard`처럼 함께 넘겨 경고를 바로 볼 수 있다. tier는 모르고 모델명만 알면 `--current-model-name <slug> --model-tier-map-path .agent-base/model-tier-map.json`으로 비교할 수 있다.

## Try It In 2 Minutes

1. 이 저장소를 AI IDE에서 연다.
2. 위 `AI IDE` 예시 중 하나를 그대로 질의한다.
3. AI가 `AGENTS.md`와 fast-path 문서를 읽고 다음 액션을 정리하게 한다.
4. 자동화나 helper 출력이 필요할 때만 Python 스크립트를 직접 실행한다.

## Coordination Depth

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

## What You Get

- 대화형 프로젝트 bootstrap 인터뷰
- 정규화된 `project generation spec`
- 프로젝트 패밀리와 runtime role 기준의 템플릿 선택
- 지원 스택에 대한 샘플 저장소 generator와 scaffold
- `AGENTS.md`, `docs/ai/*`, prompt, checklist, pre-commit 설정
- refinement, workboard, handoff packet 기반의 실행 협업 흐름
- 역할, refinement, execution lane별 vendor-neutral model tier routing과 starter warning
- adoption, migration, compatibility, parity, cutover 기준
- 실패 기록과 harness 강화 환류 루프

## Read Next

- 새 프로젝트 bootstrap: [`source/docs/ai/start-bootstrap.md`](./source/docs/ai/start-bootstrap.md)
- 기존 저장소 adoption: [`source/docs/ai/start-adoption.md`](./source/docs/ai/start-adoption.md)
- context loading: [`source/docs/ai/context-profiles.md`](./source/docs/ai/context-profiles.md)
- 역할 정의: [`source/docs/ai/roles/README.md`](./source/docs/ai/roles/README.md)
- prompt library: [`source/docs/ai/prompts/README.md`](./source/docs/ai/prompts/README.md)
- generator 상세: [`source/docs/ai/project-generator.md`](./source/docs/ai/project-generator.md)
- model tier routing: [`source/docs/ai/governance/model-routing.md`](./source/docs/ai/governance/model-routing.md)
- model tier mapping: [`source/docs/ai/tools/model-tier-mapping.md`](./source/docs/ai/tools/model-tier-mapping.md)

<details>
<summary>Core Concepts</summary>

### Project Family

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

### Runtime Role

`frontend`, `api`, `batch`, `receiver`, `client`, `tooling`, `worker`는 상위 패밀리를 대체하지 않는 하위 아키텍처 라벨이다.

### Agentic Role

구현과 검증, 문서화를 분리하기 위해 역할 기반 흐름을 지원한다.

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

</details>

<details>
<summary>Generated Repository Includes</summary>

생성된 저장소는 보통 아래를 기본으로 받는다.

- root `README.md`
- root `AGENTS.md`
- `docs/ai/*`
- `docs/ai/roles/*`
- `docs/ai/prompts/*`
- `.agent-base/project-generation-spec.json`
- `.agent-base/generation-manifest.json`
- `.agent-base/context-manifest.json`
- `.agent-base/pre-commit-config.json`
- `.agent-base/refinement-manifest.json`
- `.agent-base/refinement-status.json`
- `.agent-base/agent-role-plan.json`
- `.agent-base/agent-workboard.json`
- `.agent-base/model-routing.json`
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

</details>

<details>
<summary>Execution Collaboration Model</summary>

- `.agent-base/agent-role-plan.json`
  - 어떤 역할이 필요한지와 기본 순서를 정한다.
- `.agent-base/refinement-status.json`
  - bootstrap 이후 결정과 defer 상태를 추적한다.
- `.agent-base/agent-workboard.json`
  - 실제 실행 lane, owned path, blocker, next handoff를 관리한다.
- `.agent-base/model-routing.json`
  - 현재 역할, refinement, lane 기준에 맞는 vendor-neutral model tier 정책을 남긴다.
- `docs/ai/handoff-packets/*.md`
  - 다음 실행 에이전트가 바로 읽을 current contract를 남긴다.
- `docs/ai/agent-handoff-log.md`
  - 에이전트 간 baton history를 시간순으로 남긴다.
- `.agent-base/coordination.lock`
  - updater 스크립트가 상태 파일을 직렬화할 때 잡는 공유 잠금 경로다.

권장 흐름은 `update_refinement_status.py`로 high-priority refinement를 정리하고, blocker가 풀리면 `update_agent_workboard.py --finalize-design-freeze`로 첫 execution handoff packet을 만든 뒤, 이후 `update_agent_workboard.py`로 lane과 baton history를 갱신하는 방식이다. 전달 직전에는 `python3 scripts/update_agent_workboard.py --check-packets --strict`로 current packet이 아직 fresh한지 확인한다.

</details>

<details>
<summary>Repository Layout</summary>

- `source/`
  - canonical authoring source
  - generator, scaffold, 공통 규칙, 역할 문서, prompt, 예시가 여기서 관리된다
- `templates/`
  - 실제 저장소 루트에 바로 복사 가능한 완성형 템플릿
  - `source/`와 `template-build.json`에서 생성되는 generated artifact다
- `template-build.json`
  - template별 keep/prune 규칙
  - 어떤 `.cursor` rule과 `.github` instruction을 남길지 선언한다
- `template_overlays/`
  - 공통 베이스만으로 표현할 수 없는 template별 차이를 두는 선택형 overlay
- `tools/build_templates.py`
  - `source/`를 바탕으로 `templates/*`를 다시 생성하는 maintenance script
- `checklists/`
  - 도입, 유지보수, 드리프트 점검용 체크리스트

</details>

## For Maintainers

- `templates/*`는 배포 산출물이며 직접 수정하지 않는다.
- 공통 규칙, 문서, 스크립트는 항상 `source/`에서 수정한다.
- 템플릿별 차이는 먼저 `template-build.json`의 keep/prune 규칙으로 해결한다.
- 그래도 표현할 수 없는 차이만 `template_overlays/<template-name>/`에 둔다.

재생성 예시:

```bash
python3 ./tools/build_templates.py
python3 ./tools/build_templates.py --check
```

## Not In Scope

- 실제 비즈니스 기능 구현
- 완전 자동 제품 수준 스캐폴딩 엔진
- 조직 고유 배포 파이프라인의 세부 절차
- 특정 팀의 사람 조직도와 승인 체계

이런 항목은 생성된 저장소 안에서 repo-local overlay 문서나 추가 스크립트로 확장한다.
