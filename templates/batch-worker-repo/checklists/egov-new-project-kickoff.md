# eGov New Project Kickoff Checklist

## 1. 공통 시작 조건

- [ ] `organizationProfile = egov-public-sector`로 시작한다
- [ ] 프로젝트 구성이 `web-app`, `backend-service`, `batch-worker` 조합인지 확인했다
- [ ] 신규 구축이라도 발주기관 운영 제약이 고정돼 있으면 `constraintMode`를 `fixed-target` 또는 `legacy-maintenance`로 잡았다
- [ ] `docs/ai/org-specific/egov-public-sector-guide.md`를 읽었다
- [ ] `docs/ai/org-specific/egov-new-project-playbook.md`를 읽었다
- [ ] `.agent-base/context-manifest.json`과 `.agent-base/refinement-manifest.json`을 확인했다

## 2. 공통 산출물 고정

- [ ] `docs/ai/command-catalog.md`에 실제 build/run/test/smoke 명령을 적었다
- [ ] `docs/ai/architecture-map.md`에 frontend/backend/batch 경계를 적었다
- [ ] `docs/ai/repo-local-overrides.md`에 기관/사업별 예외를 적었다
- [ ] 공통 자산 기준 원본을 정했다
  - 공통 코드
  - 공통 메시지
  - 공통 JS/CSS
  - 공통 코드 테이블
- [ ] 반영 순서와 rollback 순서를 대략이라도 정했다

## 3. Front-end 착수 전

- [ ] 화면 유형을 분류했다
  - 검색/목록
  - 상세
  - 등록/수정
  - 첨부파일
  - 팝업
- [ ] KRDS 또는 기관 UI 기준 적용 범위를 정했다
- [ ] 공통 레이아웃과 공통 include/template 범위를 정했다
- [ ] 접근성 최소 기준을 정했다
  - 키보드 접근
  - 포커스 이동
  - 제목 구조
  - 필수 입력 표시
- [ ] 개인정보/민감정보 표시 기준을 정했다
- [ ] API 연결 기준을 정했다
  - base URL
  - 인증 방식
  - 공통 오류 처리
  - 파일 업로드/다운로드 방식

## 4. Back-end 착수 전

- [ ] controller/service/repository/mapper 경계를 정했다
- [ ] 인증/인가 처리 위치를 정했다
- [ ] profile, 환경변수, 설정 파일의 source of truth를 정했다
- [ ] 로그 정책과 health/smoke 기준을 정했다
- [ ] DB ownership 여부를 정했다
- [ ] DB를 소유하면 아래를 같이 정했다
  - schema naming
  - migration 책임
  - 초기 기준데이터
  - 검증 SQL
  - rollback 가능 범위
- [ ] 외부 연계가 있으면 timeout/retry/error 계약을 정했다

## 5. Batch 착수 전

- [ ] job/step/service/mapper 경계를 정했다
- [ ] scheduler 사용 여부를 정했다
- [ ] 수동 실행 경로를 정했다
- [ ] 재실행 기준과 중복 실행 방지 기준을 정했다
- [ ] 읽는 테이블/쓰는 테이블을 정리했다
- [ ] cutoff 기준과 상태값 전이 규칙을 정했다
- [ ] 실패 시 복구 절차와 운영 확인 포인트를 정했다
- [ ] 결과 검증 SQL를 준비했다

## 6. 통합 착수 전

- [ ] API 계약 기준 원본이 있다
- [ ] 백엔드와 배치의 데이터 ownership 충돌이 없다
- [ ] 프런트, 백엔드, 배치 간 공통 코드/공통 자산 ownership이 있다
- [ ] 최소 통합 시나리오 1개를 적었다
- [ ] 반영 순서와 rollback 순서를 설명할 수 있다

## 7. 첫 검증 시작 조건

- [ ] frontend 첫 build/smoke 기준이 있다
- [ ] backend 첫 compile/API smoke 기준이 있다
- [ ] batch 첫 manual run/smoke 기준이 있다
- [ ] 미실행 검증과 이유를 적을 위치가 정해져 있다
- [ ] 필요 시 `checklists/public-sector-ui-review.md`로 UI review를 진행할 준비가 되어 있다

## 8. 개발 착수 조건

- [ ] high-priority refinement가 해결되었거나 defer 이유가 기록돼 있다
- [ ] 역할 분업이 있으면 execution owner와 validator가 정해져 있다
- [ ] 운영 영향이 있는 항목은 문서와 runbook에 반영할 준비가 되어 있다
- [ ] 지금부터 구현을 시작해도 설계가 뒤집히지 않을 정도로 기준이 고정돼 있다
