# Agent Handoff Packets

이 문서는 `docs/ai/handoff-packets/*.md` 아래에 남기는 deterministic current handoff packet을 설명한다.

## 왜 따로 두는가

- `.agent-base/agent-workboard.json`은 machine-readable 현재 상태다.
- `docs/ai/agent-handoff-log.md`는 chronological history다.
- `docs/ai/handoff-packets/*.md`는 다음 실행 에이전트가 바로 읽고 시작할 current contract다.

history와 current contract를 분리해야, 로그는 쌓이면서도 실행 기준은 한 경로에 고정된다.

## 언제 갱신하는가

- `design-freeze`가 끝나고 첫 execution lane으로 넘길 때
- 구현 중 설계 판단이 다시 열렸다가 재정리됐을 때
- 다음 역할이 기존 packet을 그대로 믿고 시작하기 어려운 범위 변경이 생겼을 때

## 기본 명령

```bash
python3 scripts/update_agent_workboard.py --finalize-design-freeze
python3 scripts/update_agent_workboard.py \
  --finalize-design-freeze \
  --target-lane runtime-implementation \
  --handoff-summary "runtime lane can start within the frozen API and validation boundary" \
  --activate-target
```

이 명령은 아래를 한 번에 처리한다.

- `design-freeze` lane을 `completed`로 갱신
- target lane의 `latestPacketPath` 갱신
- `docs/ai/handoff-packets/design-freeze-to-<lane>.md` 업데이트
- `docs/ai/agent-handoff-log.md`에 baton 기록 추가

## packet에 반드시 들어가야 하는 것

- frozen summary
- target lane objective / scope / owned path
- required inputs 와 expected outputs
- high-priority refinement snapshot
- verification starting point
- open question 과 blocker
- 다시 `design-freeze`로 되돌려야 하는 조건

## 운영 팁

- packet 경로는 timestamp 대신 deterministic path를 쓴다.
- history는 `agent-handoff-log.md`에 남기고, packet은 같은 파일을 덮어쓴다.
- target lane이 packet 경로를 잃지 않도록 `.agent-base/agent-workboard.json`의 `latestPacketPath`를 같이 갱신한다.
- blocker가 다시 생기면 packet만 수정하지 말고 먼저 `design-freeze` lane을 다시 열어라.
