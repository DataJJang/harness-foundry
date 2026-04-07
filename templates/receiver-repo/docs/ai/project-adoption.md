# Project Adoption

짧은 진입 가이드가 필요하면 먼저 [`start-adoption.md`](./start-adoption.md)를 읽고, 이 문서는 adoption deep path에서 사용한다.

## 1. 목적

이 문서는 기존 저장소를 `agent_base` 하네스 안으로 편입할 때의 기본 순서를 정의한다.

## 2. 적용 대상

- 이미 운영 중인 저장소
- legacy 규칙과 새 규칙이 혼재한 저장소
- framework upgrade, 구조 개선, cutover를 동반한 전환 작업

## 3. 기본 순서

1. `scripts/analyze_repository.py`로 현재 저장소 inventory를 만든다.
2. [`repository-inventory.md`](./repository-inventory.md) 기준으로 누락된 사실을 보완한다.
3. [`adoption-spec.md`](./adoption-spec.md) 형태로 현재 상태와 목표 상태를 정리한다.
4. [`migration-strategy.md`](./migration-strategy.md)로 전환 전략을 고른다.
5. [`compatibility-matrix.md`](./compatibility-matrix.md)와 [`legacy-exception-policy.md`](./legacy-exception-policy.md)로 예외와 breaking point를 분류한다.
6. [`parity-validation.md`](./parity-validation.md)로 동등성 검증 기준을 정의한다.
7. [`checklists/project-adoption.md`](../../checklists/project-adoption.md)와 [`checklists/migration-readiness.md`](../../checklists/migration-readiness.md)를 완료한다.
8. 필요한 overlay 문서를 저장소에 주입하고 command catalog, architecture map, pre-commit gate를 보정한다.

## 4. 핵심 산출물

- `.agent-base/repository-inventory.json`
- `.agent-base/adoption-spec.json`
- migration plan 또는 impact analysis
- parity validation plan
- legacy exception note
- cutover / rollback note

## 5. 역할 기준

- `legacy-analyst`: 현재 구조와 명령, 제약 파악
- `migration-planner`: 단계별 전환 계획 작성
- `compatibility-reviewer`: 현재/목표 스택 호환성 검토
- `refactor-guardian`: 구조 정리 중 behavior drift 방지
- `cutover-manager`: cutover, rollback, 운영 점검 기준 관리

## 6. 완료 기준

- 현재 저장소 inventory가 정리되었다
- adoption spec가 확정되었다
- migration strategy와 parity requirement가 정의되었다
- 필요한 specialist role이 지정되었다
- 기존 저장소용 overlay와 checklists가 연결되었다
