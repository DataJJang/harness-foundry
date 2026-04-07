# Role Prompt Templates

이 디렉토리는 역할별 specialist agent에게 바로 전달할 수 있는 프롬프트 템플릿을 담는다.

## 사용 원칙

- 먼저 `docs/ai/roles/README.md`와 해당 역할 문서를 읽는다.
- 프로젝트 패밀리와 runtime specialization을 prompt 안에 명시한다.
- 입력, 출력, handoff 대상, 완료 기준을 함께 적는다.
- multi-agent 작업이면 `orchestrator` prompt를 먼저 사용한다.

## Core Role Prompt Files

- [`orchestrator.md`](./orchestrator.md)
- [`bootstrap-planner.md`](./bootstrap-planner.md)
- [`runtime-engineer.md`](./runtime-engineer.md)
- [`data-steward.md`](./data-steward.md)
- [`security-reviewer.md`](./security-reviewer.md)
- [`qa-validator.md`](./qa-validator.md)
- [`docs-operator.md`](./docs-operator.md)

## Extended Role Prompt Files

- [`product-analyst.md`](./product-analyst.md)
- [`solution-architect.md`](./solution-architect.md)
- [`release-manager.md`](./release-manager.md)
- [`failure-curator.md`](./failure-curator.md)
- [`legacy-analyst.md`](./legacy-analyst.md)
- [`migration-planner.md`](./migration-planner.md)
- [`compatibility-reviewer.md`](./compatibility-reviewer.md)
- [`refactor-guardian.md`](./refactor-guardian.md)
- [`cutover-manager.md`](./cutover-manager.md)
