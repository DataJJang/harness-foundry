# Project Bootstrap

짧은 진입 가이드가 필요하면 먼저 [`start-bootstrap.md`](./start-bootstrap.md)를 읽고, 이 문서는 bootstrap deep path에서 사용한다.

## 1. 목적

이 문서는 `harness-foundry` 템플릿으로 새 저장소를 시작할 때 Agent가 어떤 순서로 사용자와 대화하고, 어떤 선택을 확정한 뒤, 어떤 문서를 생성해야 하는지 정의한다.

## 2. 기본 생성 순서

1. 프로젝트 대화형 인터뷰를 시작한다.
2. 가능하면 [`project-bootstrap-cli.md`](./project-bootstrap-cli.md) 와 `source/scripts/project_bootstrap_cli.py`를 사용해 인터뷰를 실행한다.
3. 프로젝트 패밀리를 확정한다.
4. 프로젝트 성격, 저장소 구성 방식, 대상 플랫폼, 런타임 역할을 확정한다.
5. [`stack-matrix.md`](./stack-matrix.md) 기준으로 언어, 프레임워크, 런타임, 빌드 도구, 테스트 도구를 확정한다.
6. DB, cache, 배포 유형, 서비스 기동 형태, 로깅 방식, 동작 OS를 확정한다.
7. [`project-generation-spec.md`](./project-generation-spec.md) 입력값을 모두 채운다.
8. [`project-selection-mapping.md`](./project-selection-mapping.md) 기준으로 적합한 템플릿, 초기 산출물, 추천 agent 역할 세트를 확정한다.
9. [`roles/README.md`](./roles/README.md) 와 [`../../checklists/agent-role-selection.md`](../../checklists/agent-role-selection.md) 를 사용해 required/optional 역할을 고른다.
10. bootstrap CLI 또는 generator가 파생한 `requiredAgentRoles`, `optionalAgentRoles`, `roleSpecializations`, `agentWorkflowOrder`를 확인한다.
11. spec JSON을 저장하고 [`project-generator.md`](./project-generator.md) 기준으로 생성기를 실행한다.
12. spec 옆 `*.refinement.json` 또는 생성된 저장소의 `.agent-base/refinement-manifest.json`을 보고 high-priority 심화 모듈부터 처리한다.
13. 생성된 저장소에서 `python3 scripts/update_refinement_status.py --interactive --append-to-overrides`를 실행해 다음 pending module부터 정리한다.
14. spec 옆 `*.refinement-status.json` 또는 생성된 저장소의 `.agent-base/refinement-status.json`에 현재 결정을 기록한다.
15. `docs/ai/repo-local-overrides.md`에 기본값 유지 이유, 예외, defer note를 남긴다.
16. 생성된 샘플 저장소의 `.agent-base/context-manifest.json`을 보고 fast path 문서와 core roles를 먼저 확인한다.
17. 생성된 샘플 저장소의 `.agent-base/agent-workboard.json`을 열어 design-freeze, runtime, validator, docs lane의 owned path와 next handoff를 확정한다.
18. 생성된 저장소에서 `python3 scripts/update_agent_workboard.py --interactive --append-handoff`를 실행해 현재 실행 lane과 handoff history를 갱신한다.
19. 생성된 샘플 저장소에서 `python3 scripts/install_git_hooks.py`를 실행해 local pre-commit gate를 설치한다.
20. 생성된 샘플 저장소에서 `AGENTS.md`, `docs/ai/command-catalog.md`, `docs/ai/architecture-map.md`를 저장소 실정에 맞게 보정한다.
21. DB를 소유하는 저장소면 [`database-rules.md`](./database-rules.md) 기준으로 naming, COMMENT, migration, 위험 SQL 원칙을 확정한다.
22. [`../../checklists/project-interview.md`](../../checklists/project-interview.md), [`../../checklists/agent-role-selection.md`](../../checklists/agent-role-selection.md), [`../../checklists/project-creation.md`](../../checklists/project-creation.md) 를 완료한다.
23. `docs/ai/prompts/examples/*`, `docs/ai/prompts/*.md`, `docs/ai/prompts/roles/*.md`를 사용해 첫 프롬프트를 실행한다.
24. 첫 build/test/문서 세트를 만든다.
25. 역할 간 분업이 있으면 [`../../checklists/agent-handoff.md`](../../checklists/agent-handoff.md) 와 `docs/ai/agent-handoff-log.md`로 handoff artifact를 정리한다.
26. 첫 공유 전달 전 [`../../checklists/first-delivery.md`](../../checklists/first-delivery.md) 와 [`../../checklists/agent-completion-review.md`](../../checklists/agent-completion-review.md) 를 점검한다.

## 3. 대화형 인터뷰 질문 순서

질문 순서는 고정한다. Agent는 아래 순서대로 물어보고, 앞선 답변이 뒤 선택지를 제한하게 한다.

1. 프로젝트명
2. 저장소명
3. 프로젝트 목적
4. 프로젝트 패밀리
5. 프로젝트 성격
6. 저장소 구성 방식
   - `prototype`
   - `production`
   - `internal-tool`
   - `demo`
   - `local-only`
   - `research`
7. 대상 사용자
8. 대상 플랫폼
9. 하위 런타임 역할
10. 프로그램 언어
11. 언어별 프레임워크
12. 데이터 저장소
13. cache
14. 배포 유형
15. 서비스 기동 형태
16. 로깅 방식
17. 동작 OS
18. 보안 또는 인증 방식
19. 외부 연동
20. 기본 문서 세트
21. spec 저장 경로와 output root

인터뷰 자체에서 역할을 직접 묻지 않아도 된다. 역할은 인터뷰 결과를 바탕으로 `project-selection-mapping.md`와 `roles/README.md`에서 파생하고, CLI/generator는 그 결과를 spec와 `.agent-base/agent-role-plan.json`에 남긴다.

## 4. 프로젝트 패밀리 선택 기준

| 패밀리 | 선택 기준 | 기본 권장 방향 |
| --- | --- | --- |
| `game` | Unity 등 게임 클라이언트, 도구, 레벨/컨텐츠, 게임 서버 연계 | Unity LTS, C#, client 중심 |
| `web-app` | 브라우저 기반 일반 웹 애플리케이션 | TypeScript, React, Vite |
| `pwa` | 설치형 웹앱, 오프라인/캐시 전략이 필요한 웹 서비스 | TypeScript, React, Vite, PWA 플러그인 |
| `mobile-app` | Android/iOS 중심 앱 | Flutter 또는 React Native 기본 |
| `backend-service` | API, admin backend, 인증, 비즈니스 처리 중심 | Java 11, Spring Boot |
| `batch-worker` | 스케줄러, 집계, 대량 처리, 동기화, 배치성 작업 | Java 11, Spring Boot, MyBatis |
| `receiver-integration` | MQTT, webhook, queue consumer, 프로토콜 수신 | Java 11, Spring Boot |
| `mockup-local` | 로컬 목업, 데모, 화면 시안, 검증용 툴 | 가장 가벼운 스택 우선 |
| `library-tooling` | 공통 SDK, CLI, editor tooling, build helper | 목적 맞춤 경량 스택 |

## 5. 의사결정 트리 기본 규칙

- `game + Unity`를 선택하면 `C# + Unity LTS`를 먼저 제안한다.
- `web-app`과 `pwa`는 `TypeScript + React + Vite`를 기본으로 제안한다.
- `mobile-app`은 `Flutter`를 기본 권장으로 제안하고, 팀 경험이나 native 요구가 있으면 `React Native`, `Kotlin`, `Swift`를 선택지로 제공한다.
- `backend-service`는 `Java 11 + Spring Boot 2.3.x`를 기본으로 제안한다.
- `batch-worker`, `receiver-integration`은 `Java 11 + Spring Boot 2.7.x`를 기본으로 제안한다.
- `mockup-local`은 DB, cache, 배포를 `없음` 또는 최소 옵션으로 허용한다.
- `production` 성격이면 보안, 배포, 운영 문서를 필수로 생성한다.
- `local-only` 성격이면 운영/배포 문서는 축약 가능하나 첫 build/test 기준은 생략하지 않는다.
- 인터뷰 결과는 생성기 입력용 JSON으로 정규화한다.
- `repositoryMode`가 `monorepo` 또는 `multi-repo`여도 generator v1은 샘플 저장소 1개만 생성한다.

## 6. 저장소 생성 직후 반드시 확정할 것

- 저장소명과 기본 브랜치 전략
- 저장소 구성 방식
- 프로젝트 패밀리
- 프로젝트 성격
- 하위 런타임 역할
- 패키지명 또는 그룹명
- 언어와 런타임 버전
- 프레임워크와 빌드 도구
- 테스트 도구
- 첫 build, compile, test 명령
- 대상 환경 `local/dev/stg/prd`
- 기본 운영 문서 세트
- 핵심 외부 연동
- DB를 소유하는 경우 DB 엔진/버전, migration 위치, verification query 작성 기준

## 7. 런타임 역할별 첫 보정 포인트

### Frontend

- `package.json` 기준 build/test 명령을 확정한다.
- 기본 route, env 파일, API base URL, 정적 자산 전략을 정리한다.
- 화면 구조와 `ListPage/DetailPage/RegistrationPage/ModifyPage/Shared/Api` 패턴을 쓸지 결정한다.

### API

- `build.gradle` 기준 Java, Spring Boot, Gradle 기준선을 확정한다.
- controller/service/repository/query repository 책임 분리를 문서화한다.
- `application.yml`의 profile, 보안, DB 연결 기준을 정리한다.

### Batch

- `jobs`, `service`, `mapper`, `model`, `resources/mapper` 구조를 확정한다.
- job 등록 포인트, 스케줄 방식, SQL/runbook 문서 세트를 정리한다.
- 최소 compile/test와 job smoke 절차를 정의한다.

### Receiver

- ingress, parser/decoder, handler/service, publish 흐름을 확정한다.
- 샘플 payload와 실패 로그 기준을 먼저 남긴다.
- broker, port, topic, retry, idempotency, publish target의 문서화 위치를 정한다.

## 8. 첫 프롬프트 실행 순서

권장 순서는 아래와 같다.

1. `project-bootstrap-interview`
2. `project-spec-finalizer`
3. `scaffold-planning`
4. `project-generator-run`
5. `post-bootstrap-refinement`
6. `build-guide`
7. `test-plan`
8. DB를 소유하면 `database-review` 예시 또는 `impact-analysis`
9. 필요 시 `deployment-checklist`
10. 운영 기능이면 `operations-manual`
11. 구조가 흔들리면 `impact-analysis`

실행 예시는 [`prompts/examples/README.md`](./prompts/examples/README.md) 를 따른다.

## 9. 완료 기준

- 인터뷰 결과로 프로젝트 패밀리와 런타임 역할이 확정되었다.
- `project-generation-spec`이 모두 채워졌다.
- 생성기로 별도 디렉토리에 샘플 저장소가 생성되었다.
- 토큰 치환 규칙에 따라 저장소 메타데이터가 모두 반영되었다.
- 조건부 refinement module이 high-priority 순서로 검토되었다.
- `stack-matrix` 기준선과 예외가 문서화되었다.
- DB를 소유하면 `database-rules` 기준과 migration 위치가 확정되었다.
- command catalog에 첫 build/test/smoke 기준이 들어갔다.
- 첫 프롬프트 실행 결과로 build guide, test plan, 필요한 운영/배포 문서가 준비되었다.
- 첫 공유 전달 전에 `first-delivery` 체크리스트를 통과했다.
