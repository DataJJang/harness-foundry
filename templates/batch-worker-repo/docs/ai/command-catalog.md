# Command Catalog

## 1. 목적

이 문서는 저장소에서 build, compile, test, smoke, deploy-check 명령을 어디서 찾고 어떻게 기록할지 정의한다.

## 2. 기본 원칙

- 명령은 실제 저장소의 manifest를 source of truth로 삼는다.
- Web/app 계열은 `package.json`, `pubspec.yaml`, repo-local scripts, or engine docs
- Java 계열은 `build.gradle`, `pom.xml`, wrapper script 중 실제 manifest를 본다
- Unity 계열은 Unity version docs, project settings, editor method, or repo-local scripts
- refinement 중에 기본값을 유지하거나 예외를 허용한 이유는 `docs/ai/repo-local-overrides.md`에 남긴다.
- commit 전 빠른 검사는 `.agent-base/pre-commit-config.json`과 `scripts/precommit_check.py`를 함께 본다.
- profile, env key, 외부 의존성은 `application.yml`과 운영 문서를 함께 본다.
- 새 저장소는 첫 공유 작업 전에 `build`, `compile`, `test`, `smoke`, `deploy-check` 기준을 문서화해야 한다.
- 공통 권장 명령과 실제 저장소 명령이 다르면 repo-local 오버레이에서 반드시 재정의한다.
- schema/data change가 있으면 pre-query, post-query, verification query 위치도 기록한다.

## 3. 명령 분류

### Build

- 패키지 또는 빌드 산출물을 만드는 명령

### Compile

- 컴파일 가능 여부를 확인하는 명령

### Test

- 자동화 테스트 실행 명령

### Pre-commit

- 저장 전 local gate로 실행하는 빠른 반복 검증 명령
- 일반적으로 lint, typecheck, compile, fast validation 중심으로 둔다

### Smoke

- 배포 후 최소 경로 검증 명령 또는 절차

### Deploy-check

- 환경, 설정, 외부 의존성, 헬스체크를 확인하는 절차
- schema/data change가 있으면 verification query 수행 절차도 포함한다.

## 4. 저장소 적용 시 기록 항목

- 빌드 명령
- 컴파일 명령
- 테스트 명령
- pre-commit 명령
- 대표 smoke 검증
- 운영 반영 전 확인 항목
- 명령 실행 시 필요한 환경 변수 또는 profile
- DB 변경 시 pre-query, post-query, verification query

## 5. 프로젝트 패밀리별 권장 기본값

| 프로젝트 패밀리 | Build | Compile | Test | Smoke | Deploy-check |
| --- | --- | --- | --- | --- | --- |
| `game` | repo-local engine build or export | editor or compile validation | editmode/playmode or validation method | boot scene, core loop, or main scene validation | engine version, platform target, asset pipeline check |
| `web-app` | `npm install`, `npm run build` 또는 `mvn package` | build가 compile 역할을 겸하거나 `mvn compile`을 별도로 둔다 | `npm test`, `mvn test`, 또는 repo-local test command | 핵심 라우트 렌더, 첫 JSP/화면 또는 API base URL 확인 | env 파일, 정적 자산, WAS 설정, API endpoint 연결 확인 |
| `pwa` | `npm install`, `npm run build` | build가 compile 역할을 겸할 수 있음 | `npm test` 또는 repo-local test command | offline, installability, 핵심 라우트 확인 | env 파일, manifest, service worker, API endpoint 확인 |
| `mobile-app` | repo-local app build | repo-local compile | repo-local test | simulator or device smoke | signing, target store, backend endpoint 확인 |
| `backend-service` | `./gradlew build`, `mvn package`, 또는 repo-local build | `./gradlew compileJava` 또는 `mvn compile` | `./gradlew test` 또는 `mvn test` | 핵심 API 1건 호출, health 또는 auth 경로 확인 | profile, DB, external API, security key, DB verification query 확인 |
| `batch-worker` | `./gradlew build`, `mvn package`, 또는 repo-local build | `./gradlew compileJava` 또는 `mvn compile` | `./gradlew test` 또는 `mvn test` | 핵심 job 진입 또는 validation method 확인 | scheduler enable flag, DB, SQL, 외부 토큰, DB verification query 확인 |
| `receiver-integration` | `./gradlew build`, `mvn package`, 또는 repo-local build | `./gradlew compileJava` 또는 `mvn compile` | `./gradlew test` 또는 `mvn test` | 샘플 payload 수신 또는 parser 흐름 확인 | ingress 설정, broker/port, publish 대상, retry 로그, DB verification query 확인 |
| `mockup-local` | local preview build or repo-local command | optional | repo-local smoke test | local route or screen flow 확인 | local env only 여부와 범위 확인 |
| `library-tooling` | package or build artifact command | compile command | unit test or package smoke | sample invocation or CLI smoke | runtime dependency and install path 확인 |

## 6. 프로젝트 생성 시 추가 기록 항목

- 첫 build/test 성공 시점
- 첫 pre-commit hook 설치 시점
- 첫 preset profile 확정 또는 repo-local override 적용 시점
- 명령 실행에 필요한 JDK, Node.js, package manager 또는 profile
- 수동 smoke 절차의 입력값과 기대 결과
- stage 또는 운영 반영 전 반드시 확인할 외부 의존성
- DB change가 있으면 count query와 verification query

## 7. 보고 규칙

- 실행한 명령은 그대로 적는다.
- 미실행 명령은 이유를 적는다.
- 수동 검증은 “명령 없음, 절차형 검증”으로 구분한다.
- DB verification query는 실행 전후 row count 또는 영향 범위를 함께 적는다.
- pre-commit에 포함된 명령과 실제 commit 전 운영 관례가 어긋나면 `pre-commit-hooks.md`와 설정 파일을 같이 갱신한다.
