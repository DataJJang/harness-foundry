# Agent Workboard

이 문서는 생성기와 실행용 updater가 남기는 `.agent-base/agent-workboard.json`과 `docs/ai/agent-handoff-log.md`를 설명한다.

## 목적

- 상위 설계가 끝난 뒤 실행 에이전트가 같은 기준선으로 움직이게 한다.
- 역할 배정표와 refinement 상태를 실제 구현 lane, owned path, handoff 순서로 연결한다.
- 작업이 흔들릴 때 어느 lane에서 다시 설계 판단을 열어야 하는지 분명히 한다.

## 왜 필요한가

- `agent-role-plan.json`은 누가 필요한지 보여준다.
- `refinement-status.json`은 무엇이 아직 남았는지 보여준다.
- `agent-workboard.json`은 누가 무엇을 어떤 범위로 언제 넘겨받는지 보여준다.

세 파일을 같이 써야 설계 단계와 실행 단계가 끊기지 않는다.

## 기본 구조

- `summary`
  - `designReady`
  - `blockingHighPriorityModuleIds`
  - `pendingLaneIds`
  - `inProgressLaneIds`
  - `blockedLaneIds`
  - `completedLaneIds`
  - `nextSuggestedLaneId`
- `sharedContext`
  - spec, role plan, refinement, overrides, command catalog, architecture map 경로
- `coordinationRules`
- `workLanes[]`
  - `id`
  - `phase`
  - `role`
  - `status`
  - `objective`
  - `scopeSummary`
  - `dependsOn`
  - `ownedPaths`
  - `requiredInputs`
  - `expectedOutputs`
  - `handoffTargets`
  - `doneWhen`
  - `latestSummary`
  - `notes`
  - `verificationStatus`
  - `nextHandoffTarget`
  - `blockers`
  - `openQuestions`
  - `lastUpdated`

## 권장 운영 방식

1. `update_refinement_status.py`로 high-priority refinement를 먼저 정리한다.
2. refinement 상태가 바뀌면 workboard의 `designReady`, blocker, `design-freeze` 상태가 자동 동기화되는지 확인한다.
3. `.agent-base/agent-workboard.json`에서 `nextSuggestedLaneId`를 보고 현재 lane을 잡는다.
4. 구현 중 설계 판단이 다시 열리면 runtime lane이 혼자 밀지 말고 `design-freeze` lane으로 되돌린다.
5. lane이 바뀌거나 다음 역할로 넘길 때 `python3 scripts/update_agent_workboard.py --append-handoff`로 baton을 남긴다.
6. 첫 전달 전에는 workboard, handoff log, overrides, command catalog가 서로 모순되지 않는지 확인한다.

## 기본 명령

```bash
python3 scripts/update_agent_workboard.py --list
python3 scripts/update_agent_workboard.py --interactive --append-handoff
python3 scripts/update_agent_workboard.py \
  --lane runtime-implementation \
  --status in-progress \
  --owner runtime-engineer[api] \
  --summary "controller/service boundary aligned with the frozen design" \
  --next-handoff qa-validator \
  --verification-status build-pending \
  --append-handoff \
  --handoff-to qa-validator
```

## 좋은 handoff 기준

- 한 lane은 한 번에 하나의 주요 write scope만 가진다.
- handoff 요약은 "무엇을 끝냈는가"보다 "다음 역할이 무엇을 믿고 시작해도 되는가"를 중심으로 쓴다.
- `files in scope`, `expected outputs`, `verification status`, `open questions`는 항상 같이 남긴다.
- data, security, release 같은 side lane은 runtime lane과 같은 문제를 다른 말로 다시 풀지 말고, 자신의 승인 조건과 blocker만 남긴다.

## 사람이 보는 로그

- `docs/ai/agent-handoff-log.md`는 시간순 baton 기록이다.
- 최신 상태의 single source는 `.agent-base/agent-workboard.json`이다.
- handoff log는 history를 남기고, workboard는 현재 상태를 남긴다.
