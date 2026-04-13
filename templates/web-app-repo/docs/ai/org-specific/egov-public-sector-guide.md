# eGov Public-Sector Guide

## 1. 목적

이 문서는 `대한민국 공공/준공공 프로젝트`, `전자정부프레임워크 기반 신규 구축`, `기존 전자정부 프로젝트 migration`을 `harness-foundry` 기준으로 다룰 때의 실무 기준을 정리한다.

이 가이드는 `everything harness`를 지향하지 않는다.  
작은 팀이 반복적으로 수행하는 `전자정부 + KRDS + brownfield migration` 업무를 더 빠르고 덜 흔들리게 만드는 것이 목적이다.

## 2. 이 가이드를 먼저 쓰는 경우

- 전자정부프레임워크 기반 신규 구축 또는 고도화
- 공공기관 또는 정부/지자체 발주 사업
- KRDS 또는 정부 UI/UX 가이드라인을 따라야 하는 웹/모바일 서비스
- Spring MVC, JSP, MyBatis, 공통컴포넌트, 운영 배치가 섞인 legacy brownfield
- 최신 baseline보다 실제 운영 환경 제약이 더 강한 공공 유지보수 프로젝트

신규 구축을 실제로 시작할 때는 [`egov-new-project-playbook.md`](./egov-new-project-playbook.md)를 같이 보는 편이 좋다.

## 3. 기본 원칙

- `프로젝트 패밀리`는 그대로 사용한다.
  - `web-app`, `backend-service`, `batch-worker`, `receiver-integration`, `mockup-local`
- 전자정부 프로젝트라고 해서 별도 family를 억지로 만들지 않는다.
- 대신 아래 3가지를 우선 적용한다.
  - `organizationProfile = egov-public-sector`
  - `frontendArchitecturePolicy`
  - `constraintMode`
  - `legacy-exception-policy`
  - `compatibility / parity / migration` 문서 세트
- 신규 구축보다 `brownfield first`로 생각한다.
  - 실제론 신규처럼 보여도 기존 운영 환경, 공통컴포넌트, 산출물 형식, 발주 기준에 묶인 경우가 많기 때문이다.

## 4. 자주 나오는 프로젝트 형태

### 대민 웹 서비스

- 보통 `web-app` + `backend-service`
- 설치형/offline 요구가 있으면 `pwa`
- KRDS, 접근성, 본인인증/간편인증, 파일 업로드, 민원형 폼 검토를 early refinement에 넣는다

### 내부 업무/행정 시스템

- 보통 `web-app` + `backend-service` + `batch-worker`
- 권한, 결재/상태 전이, 엑셀 다운로드, 대량 배치, 운영 로그 요구를 early refinement에 넣는다
- 실제 착수용 후속 작업은 [`egov-new-project-playbook.md`](./egov-new-project-playbook.md) 기준으로 `frontend / backend / batch / 통합` 순서로 정리하는 편이 좋다

### 기관 간 연계/수신 시스템

- 보통 `receiver-integration` + `backend-service`
- 전문 파싱, 재처리, 재전송, 장애 복구, 운영 추적을 먼저 본다

### UI/UX 선검토 또는 제안 단계

- 보통 `mockup-local` 또는 `web-app`
- KRDS component fit, 정보구조, 접근성, 문안/레이블 일관성을 먼저 본다

## 5. bootstrap 권장값

- `repositoryMode`
  - 기본은 `single-repo`
- `organizationProfile`
  - 기본은 `egov-public-sector`
- `constraintMode`
  - 신규지만 발주/운영 기준이 강하게 고정돼 있으면 `fixed-target`
  - 기존 전자정부 유지보수/고도화면 `legacy-maintenance`
- `runtimeRoles`
  - UI가 있으면 `frontend`
  - 업무/민원 처리면 `api`
  - 야간/정기 처리면 `batch`
  - 외부 전문/수신이면 `receiver`
- `coordination mode`
  - 작은 PoC가 아니면 보통 `Coordinated`부터 시작

## 6. adoption 권장값

기존 전자정부 저장소는 아래 순서로 시작하는 편이 안전하다.

1. 현재 build/run/deploy 명령 확인
2. Spring MVC / Boot / JSP / Tiles / MyBatis / scheduler / batch 존재 여부 확인
3. 공통컴포넌트, 공통 태그, 공통 JS/CSS, 기관 공통 템플릿 확인
4. 화면/배치/API/연계 중 어디가 실제 변경 범위인지 구분
5. `compatibility-matrix`, `migration-strategy`, `parity-validation` 초안 생성
6. DB ownership, 운영 배치, 반영 절차, rollback 가능성 확인

`analyze_repository.py`를 먼저 돌리면 eGovFrame, JSP/Spring MVC, MyBatis mapper, batch/receiver, deployment/CI 흔적과 함께 docs gap, role recommendation까지 같이 확보할 수 있다.

## 7. 공공 프로젝트에서 먼저 보는 refinement

- `repository-alignment`
  - 실제 반입 산출물, 명령, 환경 분리 기준
- `runtime-shape`
  - 화면/API/배치/연계 경계
- `security-and-environments`
  - 인증, 권한, 개인정보/민감정보 로그 금지, 환경 분리
- `delivery-and-rollout`
  - 반영 절차, 검수, 운영 이관, rollback
- `stack-exceptions`
  - 전자정부 버전, 구형 WAS/JDK, 기관 표준 제약
- `data-and-schema`
  - 기관 DB naming, COMMENT, migration ownership, 검증 SQL

## 8. KRDS / UI·UX / 접근성 기준

- UI 프로젝트는 공통 frontend 규칙 외에 `KRDS 적합성`을 별도로 확인한다.
- 최소한 아래를 early review에 넣는 편이 좋다.
  - 컴포넌트 선택이 KRDS와 크게 어긋나지 않는가
  - 필수 입력, 에러 메시지, 도움말, 단계 흐름이 공공서비스 UX에 맞는가
  - 키보드 접근성, 명도 대비, 제목 구조, 폼 레이블이 기본 기준을 만족하는가
  - 공공기관 특유의 첨부파일, 표, 검색조건, 결과 목록 패턴을 안정적으로 다루는가

실제 점검은 `checklists/public-sector-ui-review.md`와 `prompts/org-specific/egov-public-sector/egov-ui-accessibility-review.md`를 같이 쓰는 편이 좋다.
검색조건/목록/상세/등록/첨부파일 같은 반복 화면을 집중 검토할 때는 `prompts/org-specific/egov-public-sector/egov-public-form-list-review.md`를 추가로 쓰면 좋다.

## 9. 역할 권장

- 거의 항상 시작:
  - `orchestrator`
  - `runtime-engineer`
  - `qa-validator`
  - `docs-operator`
- 자주 추가:
  - `legacy-analyst`
  - `migration-planner`
  - `compatibility-reviewer`
  - `security-reviewer`
  - `data-steward`

## 10. 과하게 하지 말 것

- 소규모 팀인데 multi-agent 절차를 과도하게 늘리지 않는다.
- skill marketplace 같은 범용 확장보다, 자주 하는 업무의 문서/질문/체크리스트를 더 정교하게 만든다.
- 최신 스택 강박보다 실제 운영 환경과 발주 기준 적합성을 우선한다.
- 신규 프로젝트라도 기관 공통 산출물, 반입 형식, 운영 절차를 무시하고 일반 스타트업식 flow로 밀지 않는다.
