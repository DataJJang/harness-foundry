# Pre-Commit Hooks

## 1. 목적

이 문서는 저장 전 자동 검사를 위한 pre-commit hook 기준, 설치 방법, 기본 동작, 저장소 로컬 설정 규칙을 정의한다.

## 2. 기본 구성

기본 제공 파일은 아래와 같다.

- `.githooks/pre-commit`
- `.agent-base/pre-commit-config.json`
- `.agent-base/failure-cases/`
- `scripts/install_git_hooks.py`
- `scripts/precommit_check.py`

## 3. 설치 방법

저장소 루트에서 아래를 실행한다.

```bash
python3 scripts/install_git_hooks.py
```

이 스크립트는 아래를 수행한다.

- `.githooks/pre-commit` 실행 권한 부여
- `git config core.hooksPath .githooks` 설정

## 4. 기본 동작

기본 모드는 `auto`다.

- Web/app 저장소:
  - `package.json`과 staged file을 보고 preset profile에 맞는 `lint`, `typecheck`, `build`, `test` 중 가능한 명령을 고른다.
- Java 저장소:
  - `gradlew` 또는 `pom.xml`과 staged file을 보고 preset profile에 맞는 `./gradlew compileJava`, `./gradlew test`, `mvn compile`, `mvn test`를 고른다.
- Flutter 저장소:
  - `pubspec.yaml`과 staged file을 보고 `flutter analyze`, `flutter test` 또는 `dart analyze`, `dart test`를 고른다.
- Unity 저장소:
  - 기본 제공 자동 검사는 없다.
  - `unityValidationCommands`를 repo-local 설정으로 명시해야 한다.

## 5. 설정 파일

` .agent-base/pre-commit-config.json `은 아래를 제어한다.

- `mode`
  - `auto` 또는 `custom`
- `presetProfile`
  - `auto` 또는 명시적 preset 이름
- `customCommands`
  - 항상 실행할 명령 목록
- `additionalCommands`
  - 자동 감지 뒤에 추가 실행할 명령 목록
- `unityValidationCommands`
  - Unity 저장소 전용 수동 검증 명령
- `runLintOnHook`
  - lint 또는 analyze 계열을 hook에 포함할지 여부
- `runTypecheckOnHook`
  - typecheck 또는 analyze 계열을 hook에 포함할지 여부
- `runBuildOnHook`
  - build 계열을 hook에 포함할지 여부
- `runTestOnHook`
  - hook에서 test까지 수행할지 여부
- `failWhenNoChecksRun`
  - 선택된 검사가 없으면 commit 자체를 막을지 여부

## 6. preset profile

권장 preset은 아래와 같다.

- `web-app`
- `web-app-java`
- `pwa`
- `backend-service`
- `batch-worker`
- `receiver-integration`
- `mockup-local`
- `unity-game`
- `mobile-flutter`
- `library-tooling-typescript`
- `library-tooling-java`

`presetProfile`이 `auto`면 `.agent-base/project-generation-spec.json`의 `projectFamily`, `language`, `framework`를 보고 자동으로 고른다.

## 7. 저장소별 적용 규칙

- hook는 빠르고 반복 가능해야 한다.
- 운영 의존성이 큰 smoke나 stage 검증은 pre-commit에 넣지 않는다.
- pre-commit은 최소한의 local gate로 두고, 상세 검증은 `quality-gates.md`와 `command-catalog.md`를 따른다.
- 저장소별 실제 명령은 `command-catalog.md`와 hook config를 같이 맞춘다.
- Unity나 mobile처럼 무거운 검증은 경량 validation method만 걸고, 장시간 빌드는 CI나 수동 검증으로 분리한다.
- generator가 생성한 preset은 시작점일 뿐이다. 실제 저장소 명령과 다르면 repo-local config로 바로 보정한다.

## 8. 금지 사항

- destructive SQL 또는 운영 반영 명령을 pre-commit에 넣지 않는다.
- 네트워크, 외부 계정, 운영 토큰이 필요한 명령을 기본 hook에 넣지 않는다.
- 실행 시간이 과도한 end-to-end 전체 테스트를 기본 hook에 넣지 않는다.

## 9. 점검 기준

- hook 설치 여부
- hook 실행 여부
- preset profile이 저장소 실정과 맞는지
- 실패 시 commit 차단 여부
- 저장소 실정에 맞는 명령을 고르고 있는지
- `command-catalog.md`와 hook 설정이 일치하는지
