# eGov New Project Playbook

## 1. 목적

이 문서는 `organizationProfile = egov-public-sector`로 신규 프로젝트를 시작할 때, 생성 직후부터 실제 개발 착수 전까지 무엇을 확정해야 하는지 정리한 실행 가이드다.

대상은 아래 같은 조합이다.

- `backend-service`
- `web-app`
- `batch-worker`

저장소가 3개로 분리돼 있어도 되고, 단일 저장소 안에서 논리적으로 3개 영역으로 나뉘어 있어도 된다. 핵심은 `화면`, `업무/API`, `정기 처리`를 분리해서 생각하는 것이다.

## 2. 언제 이 문서를 먼저 보나

- 전자정부프레임워크 기반 신규 구축을 시작한다.
- 발주기관 산출물 형식과 운영 절차가 이미 정해져 있다.
- KRDS 또는 기관 UI/UX 기준을 따라야 한다.
- 백엔드, 프런트엔드, 배치를 따로 개발하거나 최소한 논리적으로 분리해 관리해야 한다.
- 신규처럼 보여도 실제로는 기존 기관 공통 규칙과 운영 환경을 따라야 한다.

바로 실행에 옮길 때는 아래 문서를 같이 여는 편이 좋다.

- [`../../../checklists/egov-new-project-kickoff.md`](../../../checklists/egov-new-project-kickoff.md)
- [`../prompts/org-specific/egov-public-sector/egov-new-project-kickoff.md`](../prompts/org-specific/egov-public-sector/egov-new-project-kickoff.md)

## 3. 기본 원칙

- family는 공통 family를 그대로 쓴다.
  - `backend-service`, `web-app`, `batch-worker`
- 공공 특화 규칙은 `organizationProfile = egov-public-sector`로 켠다.
- 최신 baseline보다 실제 기관 운영 환경이 우선이면 `constraintMode = fixed-target` 또는 `legacy-maintenance`를 쓴다.
- 코딩 전에 먼저 확정해야 할 것은 `운영 제약`, `공통 산출물`, `기관 표준`, `데이터 ownership`이다.
- 신규 구축이어도 brownfield처럼 생각한다.
  - 실제로는 기존 DB, 공통컴포넌트, 운영 절차, 검수 방식에 묶이는 경우가 많기 때문이다.

## 4. 권장 프로젝트 구성

### Front-end

- 용도:
  - 대민/내부 화면
  - 검색, 목록, 상세, 등록/수정, 첨부파일, 팝업
- family:
  - `web-app`

### Back-end

- 용도:
  - 업무 API
  - 인증/인가
  - 데이터 조회/저장
  - 외부 연계
- family:
  - `backend-service`

### Batch

- 용도:
  - 야간/정기 집계
  - 상태 변경
  - 대량 처리
  - 재처리/재실행
- family:
  - `batch-worker`

## 5. 생성 직후 공통으로 먼저 할 일

모든 프로젝트는 코딩 전에 아래를 먼저 끝내는 편이 안전하다.

1. `.agent-base/context-manifest.json`에서 추천 coordination mode와 fast path를 확인한다.
2. `.agent-base/refinement-manifest.json`에서 high-priority module을 먼저 본다.
3. `docs/ai/command-catalog.md`를 실제 명령으로 맞춘다.
4. `docs/ai/repo-local-overrides.md`에 기관/사업별 예외를 기록한다.
5. `docs/ai/architecture-map.md` 초안을 만든다.
6. 공공 overlay 기준 문서를 함께 읽는다.
  - [`egov-public-sector-guide.md`](./egov-public-sector-guide.md)
  - [`../../../checklists/public-sector-ui-review.md`](../../../checklists/public-sector-ui-review.md)

공통으로 가장 먼저 확정해야 할 refinement는 보통 아래다.

- `repository-alignment`
- `runtime-shape`
- `public-sector-profile`
- `security-and-environments`
- `data-and-schema`
- `delivery-and-rollout`

## 6. Front-end에서 반드시 이어서 해야 할 일

### 6.1 화면 구조와 공통 자산 범위 확정

- 라우트 구조
- 화면 유형 분류
  - 검색/목록
  - 상세
  - 등록/수정
  - 첨부파일
  - 팝업
- 공통 레이아웃, 헤더, 푸터, 탭, breadcrumb
- 공통 JS/CSS, include, template 재사용 범위

### 6.2 KRDS / 기관 UI 기준 반영

- KRDS를 그대로 따를지, 기관 디자인 시스템을 우선할지 정한다.
- 컴포넌트 선택 기준을 정한다.
- 필수 입력, 도움말, 오류 메시지, 경고 메시지 문구 기준을 맞춘다.
- 제목 구조, 레이블, 표 구조, 버튼 위치, 첨부파일 표시 방식을 통일한다.

### 6.3 접근성과 개인정보 노출 기준 고정

- 키보드 접근
- 포커스 이동
- 명도 대비
- 시맨틱 마크업
- 필수 입력 표시
- 스크린리더용 제목/설명
- 주민번호, 연락처, 계정, 파일명 등 노출 기준

### 6.4 API 연결 기준 고정

- API base URL
- 인증 토큰/세션 처리 방식
- 공통 오류 응답 처리
- 권한별 화면 노출 기준
- 파일 업로드/다운로드 처리 기준

### 6.5 첫 검증 항목

- 최소 1개 검색 화면
- 최소 1개 상세 화면
- 최소 1개 등록/수정 화면
- 최소 1개 첨부파일 흐름
- 접근성 quick review
- 개인정보/민감정보 노출 점검

실무 검토는 아래 문서를 같이 쓰는 편이 좋다.

- [`egov-public-sector-guide.md`](./egov-public-sector-guide.md)
- [`../../../checklists/public-sector-ui-review.md`](../../../checklists/public-sector-ui-review.md)
- [`../prompts/org-specific/egov-public-sector/egov-public-form-list-review.md`](../prompts/org-specific/egov-public-sector/egov-public-form-list-review.md)

## 7. Back-end에서 반드시 이어서 해야 할 일

### 7.1 업무/API 구조 확정

- controller, service, repository, mapper 경계
- 인증/인가 처리 위치
- 예외 처리와 공통 응답 포맷
- 외부 연계 위치와 timeout/retry 기준

### 7.2 환경과 설정 source of truth 확정

- profile 구분
- 환경변수와 설정 파일 위치
- 암호화/secret 관리 방식
- 로그 정책
- health endpoint와 smoke endpoint 기준

### 7.3 데이터 ownership 확정

- DB를 직접 소유하는지 여부
- 스키마 naming 기준
- 테이블/컬럼 comment 기준
- migration 책임 주체
- 초기 기준데이터와 seed 방식
- 검증 SQL와 rollback 가능 범위

### 7.4 기관 공통 자산과 호환성 정리

- 공통컴포넌트 재사용 여부
- 공통 util/service/helper 범위
- 전자정부프레임워크 버전 제약
- WAS/JDK/OS 제약
- 기존 운영 로그와 배포 절차 호환성

### 7.5 첫 검증 항목

- 첫 compile
- 최소 1개 핵심 API smoke
- 인증이 필요한 API 1개 검증
- DB 연결 또는 mock/stub 기준 검증
- 외부 연계 없는 상태의 최소 기동 검증

## 8. Batch에서 반드시 이어서 해야 할 일

### 8.1 Job 구조와 실행 경계 확정

- job, step, tasklet/chunk 경계
- service, mapper, model 경계
- scheduler 유무
- 수동 실행 경로
- 재실행 기준

### 8.2 운영 관점 기준 확정

- 배치 실행 시각과 주기
- 수동 재처리 방법
- 실패 시 복구 절차
- 중복 실행 방지 기준
- 성공/실패 로그와 운영 확인 포인트

### 8.3 데이터 처리 기준 확정

- 읽는 테이블 / 쓰는 테이블
- cutoff 기준
- 재집계/재실행 시 일관성 보장 방식
- 상태값 전이 규칙
- 검증 SQL와 결과 확인 방법

### 8.4 첫 검증 항목

- 수동 1회 실행
- 재실행 가능 여부 확인
- 실패 로그 확인
- 결과 검증 SQL 확인
- 스케줄 on/off 기준 확인

## 9. 세 프로젝트를 함께 묶어 맞춰야 하는 것

### API 계약

- 백엔드가 기준 원본을 가진다.
- 프런트엔드는 그 계약 기준으로 바인딩한다.
- 응답 포맷, 코드값, 오류 메시지 구조를 초기에 고정한다.

### 데이터 ownership

- 백엔드와 배치가 같은 DB를 쓰면 ownership과 변경 순서를 먼저 정한다.
- 배치가 생성/집계/상태 전이를 수행하면 백엔드 화면과 정합성 검증 기준을 같이 만든다.

### 공통 자산 기준

- 공통 코드/공통 JS/CSS/공통 메시지/공통 코드 테이블의 기준 원본을 정한다.
- 어느 프로젝트가 원본인지, 복제인지, 참조인지 분명히 한다.

### 반영 순서와 rollback

- 보통은 `backend -> frontend -> batch` 순이 안전하다.
- 다만 배치가 신규 테이블/상태값을 먼저 준비해야 하면 `backend + batch`를 먼저 잠그고 프런트를 붙이는 편이 낫다.
- rollback 시 어떤 프로젝트부터 되돌릴지 미리 정한다.

## 10. 신규 전자정부 프로젝트 권장 진행 순서

### 단계 1. bootstrap 직후

- spec 검토
- constraint 검토
- command-catalog 보정
- architecture-map 초안
- refinement high-priority 정리

### 단계 2. 설계 고정

- 백엔드 API/DB/보안 기준 고정
- 프런트 화면 유형/공통 컴포넌트 기준 고정
- 배치 job/scheduler/운영 기준 고정
- 예외를 `repo-local-overrides.md`에 기록

### 단계 3. 첫 실행 기준 마련

- backend 첫 compile/smoke
- frontend 첫 build/smoke
- batch 첫 manual run smoke
- 통합 최소 시나리오 1개 확인

### 단계 4. 개발 착수

- 역할 경계 고정
- 공통 코드/공통 산출물 관리자 지정
- 체크리스트와 review prompt를 개발 중 반복 사용

## 11. 개발 착수 전에 최소한 남겨야 할 산출물

- `docs/ai/command-catalog.md`
- `docs/ai/architecture-map.md`
- `docs/ai/repo-local-overrides.md`
- 필요 시 `docs/ai/compatibility-matrix.md`
- 필요 시 `docs/ai/operations-manual.md`
- 필요 시 `docs/ai/parity-validation.md`

이 문서들이 비어 있으면, 생성은 끝났더라도 실무 착수 준비는 아직 덜 된 상태로 본다.

## 12. 바로 쓸 수 있는 간단 체크리스트

### Front-end

- KRDS/기관 UI 기준이 정리됐는가
- 검색/목록/상세/등록/첨부 패턴이 분류됐는가
- 접근성과 개인정보 노출 기준이 정해졌는가
- API 연결 기준이 고정됐는가

### Back-end

- controller/service/repository 경계가 정해졌는가
- profile/secret/log 정책이 정해졌는가
- DB ownership과 migration 책임이 정해졌는가
- 핵심 API smoke 기준이 정해졌는가

### Batch

- job/step/scheduler 구조가 정해졌는가
- 수동 실행과 재실행 기준이 있는가
- 검증 SQL와 결과 확인 방법이 있는가
- 실패 시 복구 절차가 정해졌는가

### 통합

- API 계약 기준 원본이 있는가
- 공통 자산 기준 원본이 있는가
- 반영 순서와 rollback 순서가 있는가
- 최소 통합 시나리오가 있는가

실행용 체크리스트가 필요하면 [`../../../checklists/egov-new-project-kickoff.md`](../../../checklists/egov-new-project-kickoff.md)를 그대로 사용하면 된다.
AI IDE에서 바로 시작하려면 [`../prompts/org-specific/egov-public-sector/egov-new-project-kickoff.md`](../prompts/org-specific/egov-public-sector/egov-new-project-kickoff.md)의 복붙용 질의를 먼저 쓰는 편이 좋다.
