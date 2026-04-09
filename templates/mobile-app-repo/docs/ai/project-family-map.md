# Project Family Map

## 1. 목적

이 문서는 상위 `프로젝트 패밀리`와 하위 `런타임 역할`의 관계를 정의한다.

## 2. 원칙

- 상위 분류는 항상 `프로젝트 패밀리`다.
- `frontend`, `api`, `batch`, `receiver`는 하위 역할이다.
- 하나의 프로젝트 패밀리가 여러 런타임 역할을 동시에 가질 수 있다.
- 새 저장소 생성 인터뷰에서는 패밀리를 먼저 확정하고, 그 다음 역할을 고른다.

## 3. 패밀리와 역할의 기본 관계

| 프로젝트 패밀리 | 기본 역할 | 조건부 역할 |
| --- | --- | --- |
| `game` | `client` | `tooling`, `api`, `backend`, `worker` |
| `web-app` | `frontend` | `api` |
| `pwa` | `frontend` | `api`, `worker` |
| `mobile-app` | `client` | `api` |
| `backend-service` | `api` | `worker`, `receiver` |
| `batch-worker` | `batch`, `worker` | `api` |
| `receiver-integration` | `receiver` | `worker`, `api` |
| `mockup-local` | `frontend` 또는 `client` | `tooling` |
| `library-tooling` | `tooling` | `worker` |

## 4. 선택 규칙

- `web-app`과 `pwa`는 브라우저 기반 UI가 핵심이면 먼저 고려한다.
- `pwa`는 installability, offline, cache 전략이 필요할 때만 선택한다.
- `mobile-app`은 앱스토어 또는 디바이스 실행이 핵심이면 선택한다.
- `backend-service`는 API 계약, 인증, DB, 비즈니스 로직이 중심이면 선택한다.
- `batch-worker`는 스케줄, 대량 처리, 집계, 동기화가 중심이면 선택한다.
- `receiver-integration`은 메시지 수신, 프로토콜 파싱, 이벤트 처리 중심이면 선택한다.
- `mockup-local`은 local-only, demo, click-through, low-risk prototype이면 선택한다.
- `library-tooling`은 SDK, CLI, editor tooling, reusable package 성격이면 선택한다.

## 5. 전자정부 / 공공 프로젝트에서 흔한 매핑

| 실무 형태 | 추천 패밀리 조합 | 메모 |
| --- | --- | --- |
| 대민 포털/민원 서비스 | `web-app` + `backend-service` | KRDS, 접근성, 인증, 첨부파일, 민원형 폼을 early refinement에 넣는다 |
| 내부 업무/행정 시스템 | `web-app` + `backend-service` + `batch-worker` | 권한, 상태 전이, 엑셀/대량 처리, 운영 로그를 먼저 본다 |
| 기관 간 연계/전문 수신 | `receiver-integration` + `backend-service` | 수신 포맷, 재처리, retry, 추적 가능성을 먼저 본다 |
| UI 선검토/제안 단계 | `mockup-local` 또는 `web-app` | KRDS component fit과 접근성 검토를 우선한다 |
| 공통 모듈/기관 공용 도구 | `library-tooling` | 기관 공통 배포 형식, 설치 경로, 운영 절차를 같이 문서화한다 |

전자정부 프로젝트라고 해서 별도 family를 강제로 만들 필요는 없다. 보통은 기존 family를 고르고, `constraintMode`, `legacy-exception-policy`, `compatibility-matrix`, `migration-strategy`로 공공 특유의 제약을 표현하는 편이 더 안정적이다.
