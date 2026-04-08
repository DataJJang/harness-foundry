# Project Selection Mapping

## 1. 목적

이 문서는 인터뷰에서 선택한 값이 어떤 템플릿, 문서, 명령, 초기 산출물로 이어지는지 정의한다.

## 2. 기본 매핑 규칙

- `projectFamily`가 최상위 템플릿 선택 기준이다.
- 생성기는 `projectFamily`로 기본 템플릿을 고르고, 언어/프레임워크 조합으로 scaffold profile을 고른다.
- `runtimeRole[]`는 서비스 규칙 문서와 추가 템플릿 오버레이 선택 기준이다.
- `runtimeRole[]`와 `projectFamily`는 required/optional agent 역할과 specialization을 자동 파생하는 기준이다.
- `repositoryMode`는 생성기 출력의 한계와 후속 오버레이 범위를 결정한다.
- `constraintMode`와 `hardConstraints`는 scaffold 적용 가능 여부를 baseline보다 먼저 결정한다.
- `projectNature`, `deploymentType`, `datastore`, `cache`는 생성해야 할 문서 종류를 제한하거나 확장한다.
- `production` 또는 외부 사용자 대상이면 운영/배포/보안 문서는 필수다.

## 3. 패밀리별 기본 템플릿 매핑

| projectFamily | 기본 템플릿 | 기본 문서 세트 | 기본 명령 기준 |
| --- | --- | --- | --- |
| `game` | `templates/game-repo` | bootstrap, build-guide, test-plan, ops or deployment when needed | engine build, validation, smoke |
| `web-app` | `templates/web-app-repo` | bootstrap, build-guide, test-plan | npm build, UI smoke |
| `pwa` | `templates/pwa-repo` | bootstrap, build-guide, test-plan, deployment-checklist | npm build, offline and install smoke |
| `mobile-app` | `templates/mobile-app-repo` | bootstrap, build-guide, test-plan, deployment-checklist | app build, device smoke |
| `backend-service` | `templates/backend-service-repo` | bootstrap, build-guide, test-plan, deployment-checklist, operations-manual | gradle compile and test, API smoke |
| `batch-worker` | `templates/batch-worker-repo` | bootstrap, build-guide, test-plan, operations-manual | gradle compile and test, job smoke |
| `receiver-integration` | `templates/receiver-integration-repo` | bootstrap, build-guide, test-plan, operations-manual | gradle compile and test, payload smoke |
| `mockup-local` | `templates/mockup-local-repo` | bootstrap, build-guide, test-plan | local preview and walkthrough |
| `library-tooling` | `templates/library-tooling-repo` | bootstrap, build-guide, test-plan | package build and sample invocation |

## 3.1 기본 scaffold profile 매핑

| projectFamily | language / framework | scaffold profile | 지원 수준 |
| --- | --- | --- | --- |
| `web-app` | `TypeScript + React` | `web-react-vite` | supported |
| `pwa` | `TypeScript + React` | `pwa-react-vite` | supported |
| `mockup-local` | 경량 정적 mockup | `mockup-local-static` | supported |
| `backend-service` | `Java + Spring Boot` | `java-spring-service` | supported |
| `batch-worker` | `Java + Spring Boot` | `java-spring-batch` | supported |
| `receiver-integration` | `Java + Spring Boot` | `java-spring-receiver` | supported |
| `library-tooling` | `TypeScript` | `typescript-library-tooling` | supported |
| `library-tooling` | `Java` | `java-library-tooling` | supported |
| `game` | `C# + Unity` | `unity-game` | structure-only |
| `mobile-app` | `Dart + Flutter` | `flutter-mobile` | structure-only |

## 4. 하위 역할 추가 매핑

- `runtimeRole`에 `api`가 있으면 `services/api.md`를 읽고 API 계약, validation, security 기준을 추가한다.
- `runtimeRole`에 `batch`가 있으면 `services/batch.md`를 읽고 scheduler, job, mapper, SQL 기준을 추가한다.
- `runtimeRole`에 `receiver`가 있으면 `services/receiver.md`를 읽고 ingress, parser, publish, diagnostics 기준을 추가한다.
- `runtimeRole`에 `frontend`가 있으면 `services/frontend.md`를 읽고 route, state, i18n, UI smoke 기준을 추가한다.

## 4.1 프로젝트 패밀리별 추천 agent 역할

| projectFamily | core roles | extended roles |
| --- | --- | --- |
| `game` | `orchestrator`, `bootstrap-planner`, `runtime-engineer[game]`, `qa-validator`, `docs-operator` | `product-analyst`, `solution-architect`, `release-manager`, `failure-curator` |
| `web-app` | `orchestrator`, `bootstrap-planner`, `runtime-engineer[frontend]`, `qa-validator`, `docs-operator` | `product-analyst`, `solution-architect`, `security-reviewer`, `release-manager`, `failure-curator` |
| `pwa` | `orchestrator`, `bootstrap-planner`, `runtime-engineer[frontend]`, `security-reviewer`, `qa-validator`, `docs-operator` | `product-analyst`, `solution-architect`, `release-manager`, `failure-curator` |
| `mobile-app` | `orchestrator`, `runtime-engineer[mobile]`, `qa-validator`, `docs-operator` | `product-analyst`, `security-reviewer`, `release-manager`, `failure-curator` |
| `backend-service` | `orchestrator`, `bootstrap-planner`, `runtime-engineer[api]`, `data-steward`, `security-reviewer`, `qa-validator`, `docs-operator` | `product-analyst`, `solution-architect`, `release-manager`, `failure-curator` |
| `batch-worker` | `orchestrator`, `runtime-engineer[batch]`, `data-steward`, `qa-validator`, `docs-operator` | `solution-architect`, `security-reviewer`, `release-manager`, `failure-curator` |
| `receiver-integration` | `orchestrator`, `runtime-engineer[receiver]`, `data-steward`, `security-reviewer`, `qa-validator`, `docs-operator` | `solution-architect`, `release-manager`, `failure-curator` |
| `mockup-local` | `orchestrator`, `bootstrap-planner`, `runtime-engineer[frontend or game]`, `docs-operator` | `qa-validator`, `failure-curator` |
| `library-tooling` | `orchestrator`, `runtime-engineer[tooling]`, `qa-validator`, `docs-operator` | `solution-architect`, `failure-curator` |

## 4.2 역할 매핑 규칙

- `orchestrator`는 multi-agent 흐름이면 항상 필요하다.
- bootstrap CLI와 generator는 이 문서의 패밀리별 매핑을 기준으로 `requiredAgentRoles`, `optionalAgentRoles`, `roleSpecializations`, `agentWorkflowOrder`를 자동 보정한다.
- 기본은 core roles만 먼저 확정하고, extended roles는 조건이 생길 때만 추가한다.
- DB schema, migration, seed, data correction을 소유하면 `data-steward`를 필수로 둔다.
- 인증, 권한, 보안 설정, 외부 공개 API, production 배포가 있으면 `security-reviewer`를 필수로 둔다.
- 실제 공유 전달이나 운영 영향이 있는 변경이면 `docs-operator`와 `qa-validator`를 필수로 둔다.
- 배포 순서, 롤백, 운영 점검이 중요하면 `release-manager`를 추가한다.
- 반복 실패가 있거나 harness 강화를 병행해야 하면 `failure-curator`를 추가한다.

## 5. 문서 세트 확장 규칙

- `datastore != 없음`이면 `database-rules.md`와 `checklists/database-change.md`를 포함한다.
- `deploymentType != local-only`이면 `deployment-checklist`를 생성한다.
- `projectNature == production`이면 `operations-manual`, `release-and-rollback`, `quality-gates` 검토를 필수로 한다.
- `cache != 없음`이면 config와 deploy-check 문서에 cache 의존성을 명시한다.
- `securityProfile != 없음`이면 보안 baseline과 인증 방식 문서를 같이 만든다.

## 6. 생성기 출력 규칙

- 생성기는 `templates/<family>-repo`를 먼저 복사한다.
- `repositoryMode`가 `monorepo` 또는 `multi-repo`여도 v1 생성기는 샘플 저장소 1개만 만든다.
- 이후 지원되는 scaffold profile이 있으면 코드와 설정 skeleton을 추가한다.
- 다만 `hardConstraints`가 현재 runnable scaffold baseline과 충돌하면 scaffold는 추가하지 않고 `docs-only`로 강등한다.
- scaffold profile이 `structure-only`면 실행 가능한 전체 기능 대신 최소 디렉토리와 엔트리 파일만 만든다.
- 생성기는 최소 아래 산출물을 만든다.
  - root `README.md`
  - `.agent-base/project-generation-spec.json`
  - `.agent-base/generation-manifest.json`
  - `.agent-base/context-manifest.json`
  - `.agent-base/agent-role-plan.json`
  - family-appropriate scaffold files
- 지원되지 않는 스택 조합이거나 현재 constraint 조합이 scaffold baseline을 막으면 docs template만 생성하고 `TODO_UNSUPPORTED_SCAFFOLD.md`를 남긴다.

## 7. Brownfield / Adoption 연결 규칙

- 기존 저장소는 generator보다 `project-adoption`, `adoption-spec`, `repository-inventory`를 먼저 사용한다.
- brownfield에서는 `legacy-analyst`, `migration-planner`, `compatibility-reviewer`를 우선 검토한다.
- cutover 또는 구조 분리가 있으면 `refactor-guardian`, `cutover-manager`를 추가한다.
