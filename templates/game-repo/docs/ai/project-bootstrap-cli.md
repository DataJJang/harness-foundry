# Project Bootstrap CLI

## 1. 목적

이 문서는 `project-bootstrap` 절차를 실제 터미널 대화형 실행으로 옮긴 `project_bootstrap_cli.py` 사용법을 정의한다.

## 2. 언제 쓰나

- 새 프로젝트를 처음 만들 때
- Agent가 문서형 인터뷰 대신 고정된 질문 순서로 spec을 수집해야 할 때
- 인터뷰 결과를 바로 spec JSON으로 저장하고 generator까지 이어서 실행하고 싶을 때

## 3. 실행 명령

```bash
python3 source/scripts/project_bootstrap_cli.py \
  --output-root /tmp/generated-projects \
  --force
```

선택 옵션:

- `--output-root`
  - 생성될 샘플 저장소 루트 디렉토리
- `--spec-path`
  - 인터뷰 결과 spec JSON 저장 위치
- `--skip-generate`
  - spec만 저장하고 실제 샘플 저장소 생성은 건너뜀
- `--force`
  - 같은 이름의 샘플 저장소가 이미 있으면 덮어씀

## 4. 질문 순서

CLI는 아래 순서로 질문한다.

1. 프로젝트명
2. 저장소명
3. 프로젝트 목적
4. 프로젝트 패밀리
5. 프로젝트 성격
6. 조직/도메인 profile
  - `none`
  - `egov-public-sector`
7. 런타임 역할
8. 운영 제약 모드
  - `recommended-baseline`
  - `fixed-target`
  - `legacy-maintenance`
9. 입력 방식 선택
  - `quick-start`
  - `guided-review`
  - `full-detail`
10. `quick-start`면 추천 baseline을 보여주고 대부분의 값을 자동 채운다.
11. `fixed-target` 또는 `legacy-maintenance`면 고정 운영 환경, OS, runtime/framework policy, container 허용 여부를 먼저 확인한다.
12. `guided-review` 또는 `full-detail`이면 저장소 구성 방식부터 세부 항목을 순서대로 확인한다.
13. DB 관련 추가 항목
14. 기본 문서 세트
15. 추가 예외/메모
16. output root
17. spec 저장 경로

핵심 의도는 `최종 spec에는 값이 있어야 하지만, 초기 인터뷰에서 사용자가 모든 값을 같은 무게로 직접 입력하지는 않아도 된다`는 점이다.

## 5. 출력

CLI는 아래를 만든다.

- 정규화된 spec JSON
- spec 옆 `*.refinement.json`
- spec 옆 `*.refinement-status.json`
- `organizationProfile` 기반 overlay 문서 라우팅
- 자동 파생된 `requiredAgentRoles`, `optionalAgentRoles`, `roleSpecializations`, `agentWorkflowOrder`
- 선택된 template 이름
- 선택된 scaffold profile 이름
- 생성 지원 수준
- 필요 시 scaffold 지원 강등 이유
- 추천 coordination mode와 이유
- 필요 시 실제 샘플 저장소

spec은 `.agent-base/project-generation-spec.json`으로도 생성 저장소 안에 다시 남고, generator는 `.agent-base/generation-manifest.json`, `.agent-base/context-manifest.json`, `.agent-base/agent-role-plan.json`, `.agent-base/refinement-manifest.json`, `.agent-base/refinement-status.json`, `.agent-base/agent-workboard.json`, `.agent-base/model-routing.json`, `docs/ai/agent-handoff-log.md`를 같이 만든다. 이 중 `.agent-base/context-manifest.json`과 root `README.md`에는 추천 coordination mode와 이유가 같이 들어간다.
또한 생성된 저장소에는 `scripts/show_start_path.py`가 들어가며, 현재 repo state 기준 top 3 action, model tier warning, foundry provenance를 바로 보여줄 수 있다.
`organizationProfile`이 `egov-public-sector`라면 `context-manifest`, `generation-manifest`, root `README.md`에서 그 profile과 공공 특화 guide 경로를 같이 확인할 수 있다.
신규 전자정부 프로젝트에서 `backend-service`, `web-app`, `batch-worker`를 함께 시작한다면 생성 직후 후속 작업은 [`org-specific/egov-new-project-playbook.md`](./org-specific/egov-new-project-playbook.md) 순서로 정리하는 편이 좋다.

## 6. 주의사항

- `repositoryMode`가 `monorepo` 또는 `multi-repo`여도 v1 generator는 샘플 저장소 1개만 생성한다.
- 이 경우 CLI는 spec에는 해당 값을 기록하지만, 실제 다중 저장소 분리는 후속 수작업 또는 별도 생성기로 확장해야 한다.
- Java 계열은 `packageName`을 반드시 확정해야 한다.
- DB를 소유하는 저장소는 `dbEngine`, `schemaOwnership`, `migrationPath`를 함께 기록해야 한다.
- quick-start baseline은 일반적인 로컬 시작 경로를 위한 기본값이다. production, rollout, shared DB 같은 조건이 있으면 `guided-review` 또는 `full-detail`로 전환하는 편이 안전하다.
- `fixed-target` 또는 `legacy-maintenance`는 baseline 추천보다 실제 운영 제약을 우선한다.
- 이 경우 CLI는 quick-start를 그대로 유지하지 않고 최소 `guided-review`로 올려 runtime/framework/deployment를 직접 확인한다.
- 현재 runnable scaffold가 그 제약을 만족하지 못하면 generator는 실패하지 않고 `docs-only`로 강등하며, 이유를 summary와 generation manifest에 남긴다.

## 7. 후속 작업

CLI와 generator 실행 후에는 먼저 추천 coordination mode를 확인하고 아래처럼 시작한다.

- 가장 얇은 시작점이 필요하면 생성된 저장소에서 `python3 scripts/show_start_path.py`를 먼저 실행한다.
- baseline과 생성 provenance를 확인하려면 `.agent-base/generation-manifest.json`을 같이 본다.
- 현재 tool의 model tier를 알고 있으면 `python3 scripts/show_start_path.py --current-model-tier <tier>` 또는 `.agent-base/model-routing.json` 비교로 warning을 먼저 확인한다.
- tier는 모르고 모델명만 알면 `python3 scripts/show_start_path.py --current-model-name <slug> --model-tier-map-path .agent-base/model-tier-map.json`을 쓴다.

- `Lite`
  - `docs/ai/command-catalog.md`와 `.agent-base/pre-commit-config.json` 보정
  - high-priority blocker만 확인
  - 첫 build/test/smoke 실행
- `Coordinated`
  - high-priority refinement와 `docs/ai/repo-local-overrides.md` 정리
  - `.agent-base/agent-workboard.json` 확인
  - 필요 시 `--finalize-design-freeze`로 첫 execution handoff 고정
- `Full`
  - role plan, refinement, workboard를 같이 정리
  - handoff packet과 freshness check를 shared delivery 기본 절차로 사용
  - checklist, release/runbook, first validation을 역할별로 설명 가능한 상태까지 진행
