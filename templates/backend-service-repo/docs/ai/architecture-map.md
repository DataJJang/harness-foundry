# Architecture Map

## 1. 목적

이 문서는 저장소에서 어떤 문서와 파일이 어떤 사실의 system of record인지 빠르게 찾기 위한 맵이다.

## 2. 우선 읽기 순서

1. `AGENTS.md`
2. `docs/ai/README.md`
3. 프로젝트 패밀리와 런타임 역할별 상세 규칙
4. `docs/ai/governance/*`
5. 저장소 자체 문서

## 3. System of Record 기준

### AI 규약

- 엔트리: `AGENTS.md`
- 상세 규칙: `docs/ai/*`
- 저장소별 예외와 defer note: `docs/ai/repo-local-overrides.md`
- 프롬프트 템플릿: `docs/ai/prompts/*`
- 저장소 생성 절차: `docs/ai/project-bootstrap.md`
- 생성 입력 규격: `docs/ai/project-generation-spec.md`
- 권장 기술 기준: `docs/ai/stack-matrix.md`
- 저장소 생성 및 첫 전달 체크리스트: `checklists/*`

### 코드 구조와 빌드

- Frontend: `package.json`, `src/`
- Java API / Batch / Receiver: `build.gradle`, `src/main/java`, `src/test/java`

### 환경설정

- 기본 설정 및 profile key: `src/main/resources/application.yml`
- 추가 환경 문서가 있으면 runbook 또는 deployment-checklist에 기록

### 운영 문서

- 배포 기준: `deployment-checklist` 계열 문서
- 장애 대응: `runbook` 계열 문서
- 사용자 절차: `manual` 계열 문서
- 로컬 또는 stage 검증: `validation guide` 계열 문서

## 4. 사실을 찾는 기준

- 새 저장소 생성 기준: `project-bootstrap`, `project-generation-spec`, `stack-matrix`, `checklists/project-creation.md`
- API 계약: controller, model, VO, repository, 관련 문서
- DB 사실: DDL, migration SQL, query, mapper XML, entity
- 배포 사실: deployment-checklist, release-and-rollback
- 운영 점검: runbook, lifecycle, quality gates
- UI 흐름: page, shared component, route, i18n, manual

## 5. 드리프트 확인 기준

- 코드가 문서와 다르면 먼저 실제 코드와 설정을 확인한다.
- 문서 갱신이 필요하면 `source/docs/ai/`를 먼저 고치고, 그 다음 템플릿 복제본을 갱신한다.
