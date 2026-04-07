# Project Generation Spec

## 1. 목적

이 문서는 새 저장소를 생성할 때 반드시 확정해야 하는 정규화 입력값과 프로젝트 패밀리별 필수 산출 구조를 정의한다.

## 2. 필수 입력값

생성기 입력 JSON key는 아래 camelCase 이름을 사용한다.

| 항목 | JSON key | 설명 | 필수 여부 |
| --- | --- | --- | --- |
| 저장소명 | `repositoryName` | git 저장소 이름 | 필수 |
| 프로젝트명 | `projectName` | 사용자에게 보이는 프로젝트 이름 | 필수 |
| 프로젝트 목적 | `projectPurpose` | 왜 만드는지에 대한 1~3문장 설명 | 필수 |
| 프로젝트 패밀리 | `projectFamily` | `game`, `web-app`, `pwa`, `mobile-app`, `backend-service`, `batch-worker`, `receiver-integration`, `mockup-local`, `library-tooling` | 필수 |
| 프로젝트 성격 | `projectNature` | `prototype`, `production`, `internal-tool`, `demo`, `local-only`, `research` | 필수 |
| 저장소 구성 방식 | `repositoryMode` | `single-repo`, `monorepo`, `multi-repo` | 필수 |
| 대상 사용자 | `targetUsers` | 내부 사용자, 운영자, 일반 고객, 게이머 등 | 필수 |
| 대상 플랫폼 | `targetPlatforms` | browser, Android, iOS, Windows, macOS, server, CLI 등 | 필수 |
| 런타임 역할 | `runtimeRoles` | `frontend`, `api`, `batch`, `receiver`, `client`, `tooling`, `worker` 중 하나 이상 | 필수 |
| 기본 언어 | `language` | TypeScript 또는 Java 등 | 필수 |
| 런타임 버전 | `runtimeVersion` | Node.js, Java 등 | 필수 |
| 프레임워크 | `framework` | React, Spring Boot 등 | 필수 |
| 빌드 도구 | `buildTool` | npm, Gradle 등 | 필수 |
| 테스트 도구 | `testTool` | Jest, Gradle test, repo-local tool | 필수 |
| 데이터 저장소 | `datastore` | 없음, MariaDB, PostgreSQL, SQLite, Firestore 등 | 필수 |
| cache | `cache` | 없음, Redis, in-memory 등 | 필수 |
| 배포 유형 | `deploymentType` | local-only, static-hosting, container, VM, store-release 등 | 필수 |
| 서비스 기동 형태 | `startupMode` | SPA, mobile package, Unity player, long-running service, scheduled job, event-driven worker, CLI 등 | 필수 |
| 로깅 방식 | `loggingMode` | console, file, structured JSON, remote collector 등 | 필수 |
| 동작 OS | `targetOs` | Windows, macOS, Linux, Android, iOS 등 | 필수 |
| 보안/인증 방식 | `securityProfile` | 없음, session, JWT, platform auth, store auth 등 | 필수 |
| 그룹명/패키지명 | `packageName` | Java 계열 namespace 기준 | Java 계열 필수 |
| 대상 환경 | `targetEnvironments` | `local`, `dev`, `stg`, `prd` 중 사용 환경 | 필수 |
| 핵심 외부 연동 | `externalIntegrations` | DB, Redis, MQTT, Telegram, 내부 API 등 | 필수 |
| DB 엔진/버전 | `dbEngine` | MariaDB, MySQL, PostgreSQL 등 | DB 소유 저장소 필수 |
| schema ownership | `schemaOwnership` | schema, migration, seed를 이 저장소가 소유하는지 여부 | DB 관련 저장소 필수 |
| migration 위치 | `migrationPath` | `sql`, `db/migration`, 별도 DDL 경로 등 | DB 관련 저장소 필수 |
| 기본 문서 세트 | `baseDocumentSet` | README, runbook, deployment-checklist, validation guide 등 | 필수 |
| 예외 사항 | `exceptions` | 공통 권장 스택을 벗어나는 항목과 이유 | 조건부 필수 |

## 2-1. 파생 coordination 필드

아래 필드는 bootstrap CLI와 generator가 자동으로 파생하거나 보정한다. 수동 spec를 쓸 때도 비워 두지 않는 것을 권장한다.

| 항목 | JSON key | 설명 |
| --- | --- | --- |
| 필수 agent 역할 | `requiredAgentRoles` | 기본적으로 먼저 확정하는 core 역할 목록 |
| 선택 agent 역할 | `optionalAgentRoles` | 조건이 생길 때 추가하는 extended 또는 conditional 역할 목록 |
| 역할별 specialization | `roleSpecializations` | `runtime-engineer: game` 같은 specialization |
| handoff 순서 | `agentWorkflowOrder` | orchestrator부터 validator까지의 기본 순서 |
| 역할 override | `agentRoleOverrides` | 저장소별 예외 역할 정의 |

자동 파생 규칙:

- `projectFamily`, `runtimeRoles`, `projectNature`, `datastore`, `schemaOwnership`, `securityProfile`, `deploymentType`를 기준으로 role set을 추천한다.
- 기본은 core roles를 먼저 채우고, 위험/운영/전환 조건이 생길 때 optional 역할을 확장한다.
- DB를 소유하면 `data-steward`를 필수로 올린다.
- `production` 또는 인증/인가가 있으면 `security-reviewer`를 필수로 올린다.
- `deploymentType != local-only`이면 `release-manager`를 기본 optional로 올린다.
- `runtimeRoles`에 따라 `runtime-engineer:*` specialization을 자동으로 붙인다.

## 2-2. 생성기 입력 예시

```json
{
  "repositoryName": "sample-backend-service",
  "projectName": "Sample Backend Service",
  "projectPurpose": "Provide a starter backend API for internal services.",
  "projectFamily": "backend-service",
  "projectNature": "prototype",
  "repositoryMode": "single-repo",
  "targetUsers": ["internal-operators"],
  "targetPlatforms": ["server"],
  "runtimeRoles": ["api"],
  "language": "Java",
  "runtimeVersion": "11",
  "framework": "Spring Boot",
  "buildTool": "Gradle",
  "testTool": "Gradle test",
  "datastore": "MariaDB",
  "cache": "Redis",
  "deploymentType": "container",
  "startupMode": "long-running-service",
  "loggingMode": "structured-json",
  "targetOs": ["Linux"],
  "securityProfile": "JWT",
  "packageName": "com.example.sample",
  "targetEnvironments": ["local", "dev", "stg"],
  "externalIntegrations": ["internal-api"],
  "dbEngine": "MariaDB 10.x",
  "schemaOwnership": "owned",
  "migrationPath": "db/migration",
  "baseDocumentSet": ["README", "deployment-checklist", "test-plan"],
  "exceptions": [],
  "requiredAgentRoles": ["orchestrator", "runtime-engineer", "qa-validator", "docs-operator"],
  "optionalAgentRoles": ["data-steward", "security-reviewer", "release-manager"],
  "roleSpecializations": ["runtime-engineer: api"],
  "agentWorkflowOrder": ["orchestrator", "solution-architect", "runtime-engineer", "qa-validator", "docs-operator"],
  "agentRoleOverrides": []
}
```

## 2-3. 실행형 산출물

generator는 spec를 받아 아래 산출물을 같이 남긴다.

- `.agent-base/project-generation-spec.json`
- `.agent-base/generation-manifest.json`
- `.agent-base/agent-role-plan.json`

`agent-role-plan.json`에는 필수 역할, 선택 역할, specialization, workflow order가 들어가며 multi-agent handoff의 기본 기준점으로 쓴다.

## 3. 프로젝트 패밀리별 필수 산출 구조

### Game

- `AGENTS.md`
- `docs/ai/*`
- `checklists/*`
- Unity 버전 또는 game engine 기준
- build/test/scene validation 또는 editor automation 기준
- target platform과 asset 또는 content pipeline 기준
- 필요 시 backend 또는 tooling 연계 문서

### Web App / PWA

- `AGENTS.md`
- `docs/ai/*`
- `checklists/*`
- `package.json`
- build/test 명령이 정리된 `command-catalog`
- route, env, i18n, API binding 기준
- 필요 시 PWA cache와 offline 정책

### Mobile App

- `AGENTS.md`
- `docs/ai/*`
- `checklists/*`
- mobile build and release 기준
- platform config 또는 signing 위치
- package, app versioning, runtime API binding 기준

### Backend Service

- `AGENTS.md`
- `docs/ai/*`
- `checklists/*`
- `build.gradle`
- `src/main/resources/application.yml`
- controller/service/model/repository 책임 기준
- compile/test/smoke 기준
- DB naming, migration, verification query 기준

### Batch Worker

- `AGENTS.md`
- `docs/ai/*`
- `checklists/*`
- `build.gradle`
- `jobs`, `service`, `mapper`, `model`, `resources/mapper` 구조 기준
- 운영 SQL/runbook 기준
- DB naming, migration, seed, backfill 기준

### Receiver Integration

- `AGENTS.md`
- `docs/ai/*`
- `checklists/*`
- `build.gradle`
- ingress/parser/handler/service/publish 구조 기준
- sample payload, publish target, diagnostics 기준
- persistence가 있으면 DB naming, migration, verification 기준

### Mockup Local / Library Tooling

- `AGENTS.md`
- `docs/ai/*`
- `checklists/*`
- 가장 가벼운 manifest와 build/test 명령
- local execution 방법과 범위 제한 문서
- 배포 생략 또는 축약 여부 명시

## 4. 공통 생성 규칙

- `AGENTS.md`는 짧게 유지한다.
- 긴 규칙은 `docs/ai/*`에 둔다.
- 첫 build, compile, test 명령은 `command-catalog.md`에 바로 기록한다.
- 프로젝트 패밀리 기준으로 필요한 템플릿을 선택한다.
- `repositoryMode`는 `single-repo`, `monorepo`, `multi-repo` 중 하나로 확정한다.
- generator v1은 `repositoryMode`와 관계없이 샘플 저장소 1개를 생성하고, 모노레포/멀티레포 분리는 후속 오버레이 작업으로 남긴다.
- 하위 역할과 다른 불필요한 규칙 파일은 넣지 않는다.
- 공통 권장값에서 벗어나는 언어, 프레임워크, 버전, 테스트 도구는 저장소 로컬 오버레이 문서에 근거를 남긴다.
- DB를 소유하는 저장소는 `database-rules.md`와 `checklists/database-change.md`를 기준 문서로 포함한다.

## 5. 예외 문서화 기준

다음은 repo-local 오버레이가 필수다.

- 공통 권장 버전과 다른 JDK, Node.js, Spring Boot, React, Vite 사용
- 공통과 다른 빌드 도구 또는 package manager 사용
- 공통과 다른 테스트 프레임워크 사용
- 공통과 다른 배포 환경 또는 외부 연동 의존성 사용
- 공통과 다른 DB 엔진, naming 정책, migration 위치, seed 전략 사용
- 공통 패밀리 기본값과 다른 게임 엔진, 앱 프레임워크, mobile release 전략, local-only 제약 사용
