# Refinement Manifest

이 문서는 bootstrap CLI와 generator가 남기는 `.agent-base/refinement-manifest.json` 또는 spec 옆의 `*.refinement.json` 파일 의미를 정의한다.

## 목적

- bootstrap 인터뷰를 길게 만들지 않고도 생성 후 필요한 심화 질문을 조건부로 이어가게 한다.
- 모든 프로젝트에 같은 추가 질문을 반복하지 않고, spec에 따라 필요한 모듈만 좁혀서 보여준다.
- repo-local overlay, command 보정, 운영 문서 보완이 왜 필요한지 근거와 함께 남긴다.

## 언제 생기나

- `project_bootstrap_cli.py`가 spec를 저장할 때 spec 옆에 `*.refinement.json`을 같이 남긴다.
- `generate_project.py`가 샘플 저장소를 만들 때 `.agent-base/refinement-manifest.json`을 같이 남긴다.
- 상태 추적은 `.agent-base/refinement-status.json`과 `docs/ai/repo-local-overrides.md`로 이어진다.

## 기본 항목

- `version`
- `projectFamily`
- `repositoryName`
- `scaffoldProfile`
- `supportLevel`
- `summary`
  - `needsRefinement`
  - `moduleCount`
  - `highPriorityModuleIds`
  - `suggestedExecutionOrder`
  - `decisionModes`
- `modules[]`
  - `id`
  - `title`
  - `priority`
  - `triggerReason`
  - `questions`
  - `recommendedOutputs`
  - `recommendedPrompts`
  - `agentRoles`
  - `doneWhen`

## 사용 원칙

- high-priority module부터 본다.
- 모든 질문을 한 번에 확정할 필요는 없다.
- 각 질문은 아래 셋 중 하나로 처리한다.
  - `decide-now`
  - `keep-default`
  - `defer-with-note`
- defer를 택해도 왜 미루는지와 나중에 누가 결정할지 간단히 남긴다.
- refinement 결과는 `command-catalog`, `architecture-map`, `pre-commit-config`, repo-local overlay note 같은 실제 산출물로 이어져야 한다.
- refinement 결과는 가능하면 `refinement-status.json`과 `repo-local-overrides.md`에도 같이 남긴다.

## 대표 모듈 예시

- `repository-alignment`
  - 실제 build/test/smoke 명령, source of truth 문서, pre-commit 범위를 확정
- `runtime-shape`
  - 프로젝트 패밀리별 구조, 주요 경계, 첫 검증 포인트 확정
- `data-and-schema`
  - schema ownership, migration path, verification, rollback 기준 확정
- `security-and-environments`
  - secret 주입, 인증 경계, 환경별 차이와 로그 제약 확정
- `delivery-and-rollout`
  - 배포 순서, rollback trigger, smoke owner, 운영 점검 기준 확정
- `repository-topology`
  - monorepo 또는 multi-repo 확장 경로 명시
- `scaffold-gap`
  - structure-only 또는 docs-only scaffold의 수작업 보완 범위 명시

## 추천 흐름

1. `.agent-base/refinement-manifest.json` 또는 spec 옆 `*.refinement.json`을 연다.
2. `highPriorityModuleIds`를 먼저 정리한다.
3. [`prompts/post-bootstrap-refinement.md`](./prompts/post-bootstrap-refinement.md)로 조건부 follow-up 질의를 진행한다.
4. `.agent-base/refinement-status.json`과 `docs/ai/repo-local-overrides.md`에 현재 결정을 기록한다.
5. 결정된 내용을 `command-catalog`, `architecture-map`, `pre-commit-config`, 운영 문서에 반영한다.
6. 남은 defer 항목은 `checklists/project-creation.md`와 `checklists/first-delivery.md`에서 다시 확인한다.
