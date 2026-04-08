# Project Generator

## 1. 목적

이 문서는 `harness-foundry` 기반으로 실제 샘플 저장소를 별도 디렉토리에 생성하는 방법을 정의한다.

## 2. 생성 방식

- 권장 시작 방식은 `project_bootstrap_cli.py`로 인터뷰를 실행해 spec을 확정한 뒤 generator를 호출하는 것이다.
- 인터뷰 결과를 `project-generation-spec` JSON으로 확정한다.
- 생성기는 `projectFamily`에 맞는 템플릿을 복사한다.
- 지원되는 언어/프레임워크 조합이면 scaffold를 추가 생성한다.
- 토큰 치환 규칙에 따라 프로젝트 메타데이터를 실제 값으로 바꾼다.
- 결과 저장소에는 생성 당시 spec, manifest, context manifest, agent role plan을 같이 남긴다.

## 3. 권장 CLI 인터뷰 실행

```bash
python3 source/scripts/project_bootstrap_cli.py \
  --output-root /tmp/generated-projects \
  --force
```

이 CLI는 아래를 순서대로 수행한다.

- 프로젝트 인터뷰 질문
- 정규화된 spec 생성
- spec JSON 저장
- 확인 후 generator 호출

`--skip-generate`를 주면 spec만 저장하고 샘플 저장소 생성은 건너뛴다.

## 4. generator 직접 실행 명령

```bash
python3 source/scripts/generate_project.py \
  --spec /path/to/project-spec.json \
  --output-root /path/to/output-root
```

기본 동작:

- 출력 위치: `output-root/<repositoryName>`
- 이미 대상 디렉토리가 있으면 실패
- `--force`를 주면 기존 디렉토리를 삭제하고 다시 생성

## 5. 현재 지원 수준

### Runnable or near-runnable scaffold

- `web-app` + `TypeScript` + `React`
- `pwa` + `TypeScript` + `React`
- `mockup-local`
- `backend-service` + `Java` + `Spring Boot`
- `batch-worker` + `Java` + `Spring Boot`
- `receiver-integration` + `Java` + `Spring Boot`
- `library-tooling` + `TypeScript` 또는 `Java`

### Structure-first scaffold

- `game` + `Unity`
- `mobile-app` + `Flutter`

### Docs-only fallback

- 위 조합 외의 스택

## 5.1 scaffold profile 이름

- `web-react-vite`
- `pwa-react-vite`
- `mockup-local-static`
- `java-spring-service`
- `java-spring-batch`
- `java-spring-receiver`
- `typescript-library-tooling`
- `java-library-tooling`
- `unity-game`
- `flutter-mobile`

## 6. 생성 결과

생성기는 최소 아래를 만든다.

- project family template 기반 문서 세트
- scaffold profile 기반 기본 파일
- root `README.md`
- `.agent-base/project-generation-spec.json`
- `.agent-base/generation-manifest.json`
- `.agent-base/context-manifest.json`
- `.agent-base/agent-role-plan.json`
- `.agent-base/refinement-manifest.json`
- `.agent-base/refinement-status.json`
- `.agent-base/agent-workboard.json`
- `docs/ai/repo-local-overrides.md`
- `docs/ai/agent-handoff-log.md`
- 필요 시 `TODO_UNSUPPORTED_SCAFFOLD.md`

## 7. 후속 작업

- `python3 scripts/install_git_hooks.py`로 local pre-commit gate를 활성화한다.
- `.agent-base/context-manifest.json`을 보고 fast path 문서만 먼저 연다.
- `.agent-base/refinement-manifest.json`을 보고 high-priority follow-up module부터 정리한다.
- `python3 scripts/update_refinement_status.py --interactive --append-to-overrides`로 현재 pending module을 처리한다.
- `.agent-base/refinement-status.json`과 `docs/ai/repo-local-overrides.md`에 결정과 defer note를 남긴다.
- refinement 업데이트 후 `.agent-base/agent-workboard.json`의 blocker와 `design-freeze` 상태가 자동 동기화됐는지 확인한다.
- `.agent-base/agent-workboard.json`을 열어 execution lane, owned path, next handoff를 고정한다.
- `python3 scripts/update_agent_workboard.py --interactive --append-handoff`로 실행 중 baton을 갱신한다.
- `.agent-base/pre-commit-config.json`의 preset profile과 저장소 실제 명령을 맞춘다.
- `docs/ai/command-catalog.md`를 실제 명령으로 보정한다.
- `AGENTS.md`와 `architecture-map.md`를 저장소 실정에 맞게 보정한다.
- 첫 build/test/smoke를 실제로 수행한다.
- 첫 전달 전에 `checklists/project-creation.md`와 `checklists/first-delivery.md`를 다시 확인한다.

## 8. 예시

- 실제 인터뷰부터 생성까지 이어지는 예시는 [`examples/ai-test-bootstrap-sequence.md`](./examples/ai-test-bootstrap-sequence.md) 를 참고한다.

```bash
python3 source/scripts/generate_project.py \
  --spec source/examples/specs/backend-service.json \
  --output-root /tmp/generated-projects \
  --force
```

이 명령은 `/tmp/generated-projects/sample-backend-service`를 만든다.
