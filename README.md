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
- `.agent-base/pre-commit-config.json`
- `.agent-base/agent-role-plan.json`
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
- 규칙 변경은 `source/`와 `template-build.json`을 먼저 수정하고 `tools/build_templates.py`로 `templates/*`를 다시 생성한다

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
