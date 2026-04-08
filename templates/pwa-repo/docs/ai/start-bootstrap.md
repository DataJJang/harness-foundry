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

1. `.agent-base/project-generation-spec.json` 확인
2. `.agent-base/agent-role-plan.json` 확인
3. `.agent-base/refinement-manifest.json` 확인
4. `.agent-base/refinement-status.json`과 `docs/ai/repo-local-overrides.md` 준비
5. `python3 scripts/update_refinement_status.py --interactive --append-to-overrides`
6. `.agent-base/agent-workboard.json` 확인
7. `python3 scripts/update_agent_workboard.py --interactive --append-handoff`
8. `python3 scripts/install_git_hooks.py`
9. `docs/ai/command-catalog.md` 보정
10. `checklists/project-creation.md`
11. `checklists/first-delivery.md`
