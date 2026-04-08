# Document Routing

## 1. 목적

이 문서는 어떤 변경 사항을 어떤 문서에 기록해야 하는지 정하는 기준이다.

## 2. 문서 유형 매트릭스

| 문서 | 목적 | 담아야 할 내용 | 담지 말아야 할 내용 |
| --- | --- | --- | --- |
| `AGENTS.md` | 짧은 엔트리 | 목차, 우선순위, 금지사항, 상세 docs 위치 | 긴 정책 본문, 운영 절차 전체 |
| `docs/ai/*.md` | 상세 규약 | 코딩, 배포, 운영, 품질, 서비스별 규칙 | 기능별 운영 실무 절차의 모든 단계 |
| `docs/ai/database-rules.md` | DB 기준 | 테이블/컬럼 naming, 약어, COMMENT, migration, 위험 SQL | 특정 기능의 개별 데이터 정정 이력 |
| `docs/ai/project-bootstrap.md` | 저장소 생성 절차 | 프로젝트 패밀리 인터뷰, 템플릿 선택, 초기 문서화, 첫 프롬프트 실행 순서 | 기능별 세부 구현 설계 |
| `docs/ai/project-generation-spec.md` | 생성 입력 규격 | 저장소명, 프로젝트 패밀리, 언어, 프레임워크, 명령, 문서 세트 | 저장소 개별 예외의 장문 설명 |
| `docs/ai/project-family-map.md` | 패밀리 구조 | 프로젝트 패밀리와 런타임 역할의 관계 | 기능별 세부 구현 설계 |
| `docs/ai/project-selection-mapping.md` | 선택값 매핑 | 인터뷰 결과가 템플릿, 명령, 초기 산출물로 이어지는 기준 | 장문 구현 설명 |
| `docs/ai/stack-matrix.md` | 권장 기술 기준 | 언어, 프레임워크, 런타임, 버전 기본값과 허용 범위 | 실제 운영 절차 전부 |
| `docs/ai/repo-local-overrides.md` | 저장소별 예외 메모 | 기본값 유지 이유, 예외 허용 근거, defer note, 후속 보정 포인트 | 공통 규칙 전체 본문 |
| `checklists/project-creation.md` | 생성 체크 | 필수 치환값, 첫 명령, 첫 문서, 첫 검증 | 상세 구현 규약 |
| `checklists/project-interview.md` | 인터뷰 체크 | 질문 누락, 선택값 확정, 프로젝트 패밀리와 역할 정합성 | 장문 배경 설명 |
| `checklists/first-delivery.md` | 첫 전달 체크 | 첫 PR, 첫 배포, 첫 운영 문서 전 확인 항목 | 장문 배경 설명 |
| `checklists/database-change.md` | DB 변경 체크 | naming, COMMENT, migration, rollback, verification, 위험 SQL | 장문 배경 설명 |
| `README.md` | 기능 개요 | 구현 범위, 위치, 적용 순서, 현재 제약 | 상세 장애 대응 절차 |
| `runbook.md` | 운영 실행 절차 | 등록, 리허설, 장애 대응, 운영 팁 | 공통 코딩 규약 |
| `deployment-checklist.md` | 배포 체크 | DB, 설정, 반영 순서, 배포 후 확인 | 긴 배경 설명 |
| `local-dev-validation.md` | 검증 가이드 | local/dev 검증 방법, 샘플 호출, 기대 결과 | 운영용 상세 절차 |
| `manual.md` 또는 사용자 매뉴얼 | 사용자 사용법 | 화면, 입력 항목, 메뉴 흐름, 사용 절차 | 내부 코드 설계 규약 |

## 3. 언제 어떤 문서를 갱신하는가

### `AGENTS.md`

다음이 바뀌면 갱신을 검토한다.

- canonical 문서 구조
- 도구별 adapter 구조
- 최상위 금지사항
- 문서 참조 순서

### `docs/ai/*`

다음이 바뀌면 갱신을 검토한다.

- 공통 코딩 규약
- DB naming, abbreviation, constraint, COMMENT, risky SQL 기준
- 저장소 생성 절차
- 프로젝트 패밀리와 런타임 역할 체계
- 대화형 인터뷰 질문 구조
- refinement manifest와 follow-up 질문 구조
- 권장 언어, 프레임워크, 버전 기준
- lifecycle 기준
- 품질 게이트
- 런타임 역할별 구조
- 배포/롤백 기준

### `checklists/*`

다음이 바뀌면 갱신을 검토한다.

- 템플릿 복사 후 필수 치환값
- 첫 build/test 기준
- 첫 PR 또는 첫 배포 전 필수 문서
- 저장소 생성 후 반드시 남겨야 할 오버레이 기준
- high-priority refinement 상태와 defer note 확인 기준
- DB naming, migration, verification, rollback 확인 기준

### 운영 문서

다음이 바뀌면 `runbook`, `deployment-checklist`, `validation guide`, `manual` 갱신을 검토한다.

- 신규 테이블, 신규 컬럼, 공통 코드 추가
- 운영 설정, 토큰, 외부 연동 방식 변경
- 장애 대응 절차 변경
- 기능 사용법 변경
- 배포 순서, migration 순서, 검증 절차 변경
- 화면 흐름 변경
- data correction, backfill, 위험 SQL 실행 절차 변경

## 4. 판단 기준

### 원칙

- 상위 원칙과 분기 기준은 `docs/ai`
- 실제 실행 절차는 `runbook`, `manual`, `deployment-checklist`, `validation guide`
- 구현 배경과 범위는 `README`
- DB naming과 위험 SQL 기본 기준은 `docs/ai/database-rules.md`
- 특정 변경의 실행 체크는 `checklists/database-change.md`

### 예시

- 신규 Telegram 기능의 공통 개발 규약: `docs/ai/services/*`
- 신규 저장소를 시작할 때의 절차: `docs/ai/project-bootstrap.md`
- 새 저장소의 프로젝트 패밀리와 역할 관계: `docs/ai/project-family-map.md`
- 새 저장소의 언어/프레임워크/버전 기본값: `docs/ai/stack-matrix.md`
- 새 저장소의 repo-local 예외와 defer note: `docs/ai/repo-local-overrides.md`
- 새 저장소의 첫 build/test/문서 생성 체크: `checklists/project-creation.md`
- 신규 테이블과 migration naming 기준: `docs/ai/database-rules.md`
- DB 변경 실행 전 확인 항목: `checklists/database-change.md`
- Telegram 방 등록 실무 절차: `runbook.md` 또는 운영 매뉴얼
- 배포 직전 확인 항목: `deployment-checklist.md`
- local/dev 샘플 검증 절차: `local-dev-validation.md`
