# Refinement Status

이 문서는 bootstrap 이후 follow-up 결정을 추적하는 `.agent-base/refinement-status.json` 또는 spec 옆 `*.refinement-status.json`의 의미를 정의한다.

## 목적

- refinement manifest가 제안한 모듈이 실제로 어떻게 처리됐는지 기록한다.
- `decide-now`, `keep-default`, `defer-with-note` 중 어떤 방식으로 정리됐는지 남긴다.
- 첫 전달 전 high-priority module이 해결되었는지 빠르게 확인한다.

## 언제 생기나

- `project_bootstrap_cli.py`가 spec 저장 시 spec 옆에 `*.refinement-status.json`을 같이 만든다.
- `generate_project.py`가 샘플 저장소를 생성할 때 `.agent-base/refinement-status.json`을 같이 만든다.

## 기본 항목

- `version`
- `repositoryName`
- `projectFamily`
- `summary`
  - `pendingModuleIds`
  - `highPriorityPendingModuleIds`
  - `resolvedModuleIds`
  - `deferredModuleIds`
  - `nextRecommendedPrompt`
  - `decisionModes`
- `modules[]`
  - `id`
  - `title`
  - `priority`
  - `status`
  - `decisionMode`
  - `ownerHints`
  - `recommendedOutputs`
  - `recommendedPrompts`
  - `notes`
  - `deferredReason`
  - `resolver`
  - `lastUpdated`

## 권장 status 값

- `pending`
- `resolved`
- `kept-default`
- `deferred`

## 기본 명령

```bash
python3 scripts/update_refinement_status.py --interactive
```

생성된 저장소 안에서 실행하면, 가능한 경우 `.agent-base/agent-workboard.json`의 `designReady`, `blockingHighPriorityModuleIds`, `design-freeze` lane 상태도 같이 동기화한다.
high-priority blocker가 모두 사라지면 `design-freeze`는 보통 `pending`으로 돌아오고, 실제 첫 execution packet은 `python3 scripts/update_agent_workboard.py --finalize-design-freeze`에서 만든다.
이 스크립트는 기본적으로 `.agent-base/coordination.lock`을 잡고 `refinement-status.json`, `agent-workboard.json`, `repo-local-overrides.md`를 atomic write로 갱신한다.
다른 updater가 이미 실행 중이면 잠금이 풀릴 때까지 기다리며, 필요하면 `--lock-timeout-seconds 0.1`처럼 fail-fast 설정을 줄 수 있다.

추가 예시:

```bash
python3 scripts/update_refinement_status.py --list
python3 scripts/update_refinement_status.py \
  --module delivery-and-rollout \
  --status deferred \
  --append-to-overrides \
  --resolver release-manager \
  --deferred-reason "stg pipeline가 아직 없어 rollout 기준을 다음 단계로 미룸" \
  --notes "first local build and smoke 이후 다시 확정"
```

## 사용 원칙

- refinement 질문을 진행할 때 manifest와 status를 같이 연다.
- 확정한 내용이 있으면 관련 module의 `status`, `decisionMode`, `notes`를 갱신한다.
- 미루는 경우 `deferredReason`과 `resolver`를 남긴다.
- 문서와 설정을 실제로 반영했다면 `resolved` 또는 `kept-default`로 올린다.
- 첫 공유 전달 전에는 `highPriorityPendingModuleIds`가 비었거나 defer 이유가 분명해야 한다.

## 연결 산출물

- 사람이 읽는 메모: `docs/ai/repo-local-overrides.md`
- follow-up 질문 기준: `.agent-base/refinement-manifest.json`
- 실행 lane 기준: `.agent-base/agent-workboard.json`
- 실제 반영 대상: `docs/ai/command-catalog.md`, `docs/ai/architecture-map.md`, `.agent-base/pre-commit-config.json`, `deployment-checklist`, `operations-manual`
