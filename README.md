# agent_base

`agent_base`는 새 프로젝트를 시작하거나 기존 저장소에 AI 작업 규칙을 이식할 때 사용하는 `프로젝트 생성 킷 + 규칙 템플릿 + agentic engineering base pack`이다.

이 패키지는 단순 scaffold 모음이 아니라 아래를 한 세트로 제공한다.

- 대화형 프로젝트 bootstrap 인터뷰
- 정규화된 project generation spec
- 프로젝트 패밀리와 runtime role 기준의 템플릿 선택 규칙
- 샘플 저장소 generator와 scaffold
- 저장 전 자동 검사를 위한 pre-commit hook pack
- 실패 기록과 harness 강화 환류 루프
- 역할 기반 agentic engineering 문서와 역할별 prompt library

## 무엇을 할 수 있나

- 새 프로젝트를 인터뷰 형식으로 시작해 생성 spec을 확정한다.
- `game`, `web-app`, `pwa`, `mobile-app`, `backend-service`, `batch-worker`, `receiver-integration`, `mockup-local`, `library-tooling` 패밀리 중 하나를 기준으로 템플릿을 고른다.
- 지원되는 언어/프레임워크 조합이면 최소 실행 가능한 샘플 저장소를 별도 디렉토리에 생성한다.
- 생성된 저장소 안에 `AGENTS.md`, `docs/ai/*`, 체크리스트, prompt 예시, pre-commit 설정을 같이 넣어 첫 build/test/문서화까지 이어갈 수 있게 한다.
- 필요하면 `orchestrator`, `runtime-engineer`, `data-steward`, `security-reviewer`, `qa-validator`, `docs-operator` 같은 역할로 Agent를 나눠 agentic workflow를 설계할 수 있다.

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

- `orchestrator`
- `product-analyst`
- `solution-architect`
- `bootstrap-planner`
- `runtime-engineer`
- `data-steward`
- `security-reviewer`
- `qa-validator`
- `docs-operator`
- `release-manager`
- `failure-curator`

역할별 책임과 handoff 규칙은 [`source/docs/ai/roles/README.md`](./source/docs/ai/roles/README.md) 에 정리돼 있다.

## 패키지 구조

- `source/`
  - canonical authoring source
  - generator, scaffold, 공통 규칙, 역할 문서, prompt, 예시가 여기서 관리된다
- `templates/`
  - 실제 저장소 루트에 바로 복사 가능한 완성형 템플릿
  - 프로젝트 패밀리 템플릿과 runtime role 템플릿이 함께 있다
- `checklists/`
  - 도입, 유지보수, 드리프트 점검용 체크리스트

## 시작 순서

1. [`source/AGENTS.md`](./source/AGENTS.md)를 읽는다.
2. [`source/docs/ai/project-bootstrap.md`](./source/docs/ai/project-bootstrap.md)로 인터뷰 절차를 따른다.
3. 가능하면 [`source/docs/ai/project-bootstrap-cli.md`](./source/docs/ai/project-bootstrap-cli.md)와 `source/scripts/project_bootstrap_cli.py`로 인터뷰와 spec 생성을 한 번에 수행한다.
4. [`source/docs/ai/project-generation-spec.md`](./source/docs/ai/project-generation-spec.md)로 생성 spec을 검토한다.
5. [`source/docs/ai/project-family-map.md`](./source/docs/ai/project-family-map.md)과 [`source/docs/ai/project-selection-mapping.md`](./source/docs/ai/project-selection-mapping.md)으로 템플릿, runtime role, 추천 agent 역할 세트를 정한다.
6. [`source/docs/ai/roles/README.md`](./source/docs/ai/roles/README.md)와 [`source/checklists/agent-role-selection.md`](./source/checklists/agent-role-selection.md)로 역할과 handoff 책임을 정한다.
7. [`source/docs/ai/stack-matrix.md`](./source/docs/ai/stack-matrix.md), [`source/docs/ai/database-rules.md`](./source/docs/ai/database-rules.md)를 기준으로 기술 스택과 DB 기준을 확정한다.
8. [`source/docs/ai/project-generator.md`](./source/docs/ai/project-generator.md)와 [`source/docs/ai/token-substitution.md`](./source/docs/ai/token-substitution.md)를 읽고 generator를 실행한다.
9. 생성된 샘플 저장소 안에서 `python3 scripts/install_git_hooks.py`를 실행한다.
10. 생성된 샘플 저장소 안에서 `.agent-base/pre-commit-config.json`의 preset profile을 실제 명령 체계에 맞게 보정한다.
11. 생성된 샘플 저장소 안에서 `command-catalog`, `architecture-map`, `project-creation`, `first-delivery`를 실제 프로젝트에 맞게 보정한다.
12. 역할 기반 분업을 할 경우 `agent-handoff`, `agent-completion-review`, `agent-failure-review` 체크리스트를 같이 사용한다.

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
- `.agent-base/pre-commit-config.json`
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
- 규칙 변경은 `source/`를 먼저 수정하고 `templates/*`를 다시 동기화한다

## 이 패키지가 다루지 않는 것

- 실제 비즈니스 기능 구현
- 완전 자동 제품 수준 스캐폴딩 엔진
- 조직 고유 배포 파이프라인의 세부 절차
- 특정 팀의 사람 조직도와 승인 체계

이런 항목은 생성된 저장소 안에서 repo-local overlay 문서나 추가 스크립트로 확장한다.
