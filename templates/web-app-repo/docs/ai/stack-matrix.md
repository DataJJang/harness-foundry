# Stack Matrix

## 1. 목적

이 문서는 새 프로젝트를 시작할 때 프로젝트 패밀리별 권장 언어, 프레임워크, 런타임, 버전 기준을 정의한다.

## 2. 기본 원칙

- 아래 값은 `강한 권장 기본값`이다.
- 실제 저장소가 이 기준을 벗어나면 repo-local 오버레이 문서에 근거를 남긴다.
- 빌드 파일과 설정 파일이 최종 source of truth다.

## 3. 권장 기준표

| 프로젝트 패밀리 | 권장 언어/런타임 | 권장 프레임워크 | 권장 빌드 도구 | 권장 테스트 기준 | 예외 시 문서화 |
| --- | --- | --- | --- | --- | --- |
| `game` | C# + Unity LTS | Unity LTS | Unity Hub + repo-local scripts | playmode/editmode 또는 validation method | engine version doc, overlay, command-catalog |
| `web-app` | TypeScript + Node.js 22 LTS 또는 Java 17 | React 19.2, Vite 8.x 또는 eGovFrame 4.3 JSP/Spring MVC | npm 또는 Maven | `npm run build`, `npm test`, `mvn compile`, `mvn test` | `package.json`, `pom.xml`, overlay, command-catalog |
| `pwa` | TypeScript + Node.js 22 LTS | React 19.2, Vite 8.x, PWA plugin | npm | `npm run build`, `npm test` 또는 repo-local test | `package.json`, overlay, command-catalog |
| `mobile-app` | Dart 3.x 또는 TypeScript + Node.js 22 LTS | Flutter 기본, React Native 허용 | Flutter CLI 또는 npm | repo-local build and test command | manifest, overlay, command-catalog |
| `backend-service` | Java 17 | Spring Boot 3.5.x, JPA, Querydsl 중심 또는 eGovFrame 4.3 REST + MyBatis | Gradle 또는 Maven | `./gradlew compileJava`, `./gradlew test`, `mvn compile`, `mvn test` | `build.gradle`, `pom.xml`, overlay, command-catalog |
| `batch-worker` | Java 17 | Spring Boot 3.5.x, Spring Batch 5, MyBatis 또는 eGovFrame 4.3 Batch + MyBatis | Gradle 또는 Maven | `./gradlew compileJava`, `./gradlew test`, `mvn compile`, `mvn test` | `build.gradle`, `pom.xml`, overlay, command-catalog |
| `receiver-integration` | Java 17 | Spring Boot 3.5.x, protocol adapter + handler/service/publish 패턴 | Gradle | `./gradlew compileJava`, `./gradlew test` | `build.gradle`, overlay, command-catalog |
| `mockup-local` | TypeScript + Node.js 22 LTS 또는 repo-local lightweight stack | Vite 8.x, lightweight UI tool, static mockup | npm 또는 repo-local tool | build or local preview smoke | manifest, overlay, command-catalog |
| `library-tooling` | Java 17, TypeScript + Node.js 22 LTS, or repo-local language | library or CLI-friendly minimal framework | Gradle, npm, or repo-local tool | compile and package smoke | manifest, overlay, command-catalog |

## 4. 허용 범위

### Game

- Unity LTS를 기본으로 본다.
- C#을 기본 언어로 본다.
- custom engine 또는 다른 game framework를 쓰면 overlay가 필수다.

### Web App / PWA

- React는 `19.2` 계열을 기본으로 본다.
- TypeScript는 `5.x` 계열을 기본으로 본다.
- Node.js는 `22 LTS`를 기본으로 보고, current Vite 지원선인 `20.19+ / 22.12+`도 호환 범위로 본다.
- Vite는 current docs line인 `8.x`를 기본으로 본다.
- `Node.js 18`, `React 18`, `Vite 4/5`는 legacy baseline으로 간주한다.
- 공공/전자정부 프로젝트에서 `organizationProfile = egov-public-sector`면 `Java 17 + Maven + eGovFrame 4.3 JSP/Spring MVC` 조합을 `공식 reference lane`으로 허용한다.
- 다만 공공 `web-app`의 기본 선택은 `frontendArchitecturePolicy`로 결정한다.
- `frontendArchitecturePolicy = separated-frontend-api`면 `TypeScript + React`도 공식 지원 경로로 남기고, SEO/MPA/AJAX/크로스브라우징 제약은 `publicWebConstraints`에 기록한다.
- `pwa`는 offline, cache, installability가 필요 없으면 `web-app`로 낮춘다.

### Mobile App

- Flutter를 기본으로 본다.
- `React Native`, `Kotlin`, `Swift`는 팀 숙련도나 배포 제약이 있을 때 허용한다.
- store release가 필요한 경우 signing, package naming, release flow overlay가 필요하다.

### Backend Service

- JDK는 `17`을 기본으로 본다.
- Spring Boot는 보수안으로 `3.5.x` 계열을 기본으로 본다.
- 전자정부프레임워크 baseline이 필요한 경우 `eGovFrame 4.3 REST + MyBatis + Maven`도 공식 선택지로 본다.
- 공격안은 `4.0.x` 계열이며, 더 빠른 baseline adoption이 필요할 때만 repo-local overlay와 함께 선택한다.
- `Java 11`, `Spring Boot 2.x`는 legacy baseline으로 간주한다.
- JPA + Querydsl 패턴을 우선하고, 복잡 조회는 query repository 또는 native query로 분리한다.

### Batch Worker

- JDK는 `17`을 기본으로 본다.
- Spring Boot는 `3.5.x` 계열을 기본으로 본다.
- 전자정부프레임워크 baseline이 필요한 경우 `eGovFrame 4.3 Batch + MyBatis + Maven`도 공식 선택지로 본다.
- Spring Batch 5 기준으로 `JobBuilderFactory`, `StepBuilderFactory` 없는 구성을 우선한다.
- `Java 11`, `Spring Boot 2.7.x`는 legacy baseline으로 간주한다.
- mapper XML과 운영 SQL 문서가 필요한 구조를 기본으로 본다.

### Receiver Integration

- JDK는 `17`을 기본으로 본다.
- Spring Boot는 `3.5.x` 계열을 기본으로 본다.
- validation과 servlet API는 `jakarta.*` namespace 기준을 우선한다.
- `Java 11`, `Spring Boot 2.7.x`는 legacy baseline으로 간주한다.
- 수신 프로토콜 차이는 repo-local 오버레이에서 정의한다.

### Mockup Local / Library Tooling

- 가장 가벼운 도구를 우선한다.
- local-only 목업은 DB, cache, 배포를 비워 둘 수 있다.
- reusable library나 CLI는 불필요한 web/server dependency를 넣지 않는다.

## 5. 문서화 의무

다음 중 하나라도 해당되면 저장소 로컬 오버레이가 필요하다.

- 다른 언어를 사용한다.
- 권장 런타임 버전과 다르다.
- 다른 프레임워크 계열을 쓴다.
- package manager, 빌드 도구, 테스트 도구가 다르다.
- 배포 환경이나 외부 연동 때문에 별도 제약이 있다.
- 프로젝트 패밀리 기본값과 다른 엔진, mobile stack, 배포 유형을 택한다.
