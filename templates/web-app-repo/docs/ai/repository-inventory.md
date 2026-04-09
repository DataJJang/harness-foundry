# Repository Inventory

## 1. 목적

기존 저장소를 adoption하기 전에 먼저 추출해야 하는 사실 목록을 정의한다.

## 2. 최소 inventory 항목

- 언어, 프레임워크, 런타임 버전
- build/test 명령
- 실행/기동 방식
- 환경설정 위치
- DB/cache/queue/broker 의존성
- 외부 연동
- 문서 위치
- 배포 방식
- 운영성 로그/모니터링 포인트
- 위험 구간
  - legacy auth
  - custom build
  - manual SQL
  - undocumented deploy step

## 3. 산출물

- `.agent-base/repository-inventory.json`
- `.agent-base/docs-gap-report.md`
- `.agent-base/role-recommendation.json`

`analyze_repository.py`는 기본적으로 이 3가지를 함께 만든다.

- `repository-inventory.json`
  - 실제 파일, 명령 힌트, family/runtime 후보, deployment/migration 흔적
- `docs-gap-report.md`
  - 현재 문서 상태와 adoption 시 먼저 보강할 문서 gap
- `role-recommendation.json`
  - required/optional 역할, suggested constraint mode, coordination mode

전자정부/공공 프로젝트에서는 아래 같은 흔적을 초기에 자동 감지하는 것이 중요하다.

- `egovframe`, `org.egovframe`
- Spring MVC XML, `web.xml`, JSP
- MyBatis mapper XML
- `Globals.properties`, Tiles layout, 공통 include/layout
- 공통 JS/CSS/static asset와 기관 공통 템플릿 흔적
- batch, scheduler, receiver, external integration 힌트
- KRDS 또는 접근성 관련 문자열/구조
- 검색조건, 목록, 상세, 등록/수정, 첨부파일, 팝업 같은 공공형 화면 패턴

## 4. inventory 질문

- 실제 build/test 명령은 어디에 있는가
- 환경별 profile과 secret은 어디에서 주입되는가
- DB schema와 migration은 누가 소유하는가
- 운영자가 실제로 보는 로그와 health point는 무엇인가
- 배포/롤백 문서는 있는가
- parity가 깨지면 큰 문제가 나는 기능은 무엇인가
- 공통 JS/CSS, include, Tiles/layout, 공통컴포넌트가 영향 범위를 얼마나 넓히는가
- 검색조건, 결과 목록, 상세/수정, 첨부파일 중 어디가 반복 패턴이고 어디가 예외 화면인가
