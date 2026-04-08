# Start Bootstrap

이 문서는 `새 프로젝트` 또는 `새 저장소`를 시작할 때 가장 먼저 읽는 짧은 진입 가이드다.

## 언제 쓰는가

- 새 프로젝트를 만든다.
- 프로젝트 패밀리, 기술 스택, 생성 템플릿을 아직 정하지 않았다.
- 기존 저장소가 아니라 새 저장소를 별도 디렉토리에 생성한다.

## 빠른 시작 순서

1. [`project-bootstrap.md`](./project-bootstrap.md)
2. [`project-bootstrap-cli.md`](./project-bootstrap-cli.md)
3. [`project-generation-spec.md`](./project-generation-spec.md)
4. [`project-selection-mapping.md`](./project-selection-mapping.md)
5. [`roles/README.md`](./roles/README.md)
6. [`project-generator.md`](./project-generator.md)

## Coordination Mode Quick Pick

모드는 고정 등급이 아니라 현재 coordination cost를 설명하는 운영 레벨이다. 기본은 가장 가벼운 모드로 시작하고, 실제 리스크가 생길 때만 올린다.

- `Lite`
  - single-repo, local-first, demo/prototype, no DB/security/deployment risk
  - 생성 후에는 blocking refinement와 첫 build/test만 먼저 본다
- `Coordinated`
  - DB, security, external integration, container/static delivery처럼 공유 기준이 필요한 작업
  - 생성 후에는 high-priority refinement와 first execution handoff까지만 기본으로 맞춘다
- `Full`
  - production, monorepo/multi-repo, rollout/release ownership, schema ownership 같은 고위험 작업
  - 생성 후에는 role plan, workboard, packet freshness까지 기본 절차로 본다

generator가 만든 `.agent-base/context-manifest.json`과 root `README.md`는 이 세 모드 중 추천값과 이유를 함께 남긴다.

## 기본 결정 항목

- `projectFamily`
- `projectNature`
- `repositoryMode`
- `runtimeRole[]`
- `language`
- `framework`
- `datastore`
- `cache`
- `deploymentType`
- `startupMode`
- `loggingMode`
- `targetOs[]`
- `securityProfile`

## 처음에 필요한 역할

- 항상 시작:
  - `orchestrator`
  - `bootstrap-planner`
  - `runtime-engineer`
  - `qa-validator`
  - `docs-operator`
- 조건부:
  - `data-steward`
  - `security-reviewer`

## 생성 후 바로 할 일

### Lite

1. `.agent-base/context-manifest.json`에서 추천 mode와 fast path 문서를 확인한다.
2. `.agent-base/refinement-manifest.json`에서 high-priority blocker만 먼저 본다.
3. `docs/ai/command-catalog.md`와 `.agent-base/pre-commit-config.json`을 실제 명령으로 맞춘다.
4. 첫 build/test/smoke를 실행한다.
5. 병렬 작업이나 DB/security/release risk가 생기면 그때 `agent-workboard` 절차로 확장한다.

### Coordinated

1. `.agent-base/context-manifest.json`, `.agent-base/refinement-manifest.json`, `.agent-base/agent-workboard.json`을 본다.
2. `python3 scripts/update_refinement_status.py --interactive --append-to-overrides`로 high-priority refinement를 정리한다.
3. blocker가 풀리면 `python3 scripts/update_agent_workboard.py --finalize-design-freeze`로 첫 execution handoff를 고정한다.
4. `docs/ai/command-catalog.md`와 `.agent-base/pre-commit-config.json`을 보정한다.
5. 첫 build/test/smoke를 실행하고 필요할 때만 handoff history를 남긴다.

### Full

1. `.agent-base/project-generation-spec.json`, `.agent-base/agent-role-plan.json`, `.agent-base/refinement-manifest.json`, `.agent-base/agent-workboard.json`을 같이 본다.
2. high-priority refinement와 역할 분업 경계를 먼저 고정한다.
3. `python3 scripts/update_agent_workboard.py --finalize-design-freeze`와 `--check-packets --strict`를 shared delivery 기본 절차로 둔다.
4. `docs/ai/command-catalog.md`, `docs/ai/repo-local-overrides.md`, release/runbook 계열 문서를 같이 맞춘다.
5. 첫 build/test/smoke와 checklist를 role별로 설명 가능한 상태로 만든다.
