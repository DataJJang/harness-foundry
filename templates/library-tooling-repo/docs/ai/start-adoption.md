# Start Adoption

이 문서는 `기존 저장소`, `conversion`, `migration`, `brownfield onboarding`을 시작할 때 가장 먼저 읽는 짧은 진입 가이드다.

## 언제 쓰는가

- 이미 코드가 있는 저장소를 온보딩한다.
- framework, runtime, build, deployment 체계를 점진 전환한다.
- legacy 구조에 AI 규약과 품질 게이트를 이식한다.

## 빠른 시작 순서

1. [`project-adoption.md`](./project-adoption.md)
2. [`repository-inventory.md`](./repository-inventory.md)
3. [`adoption-spec.md`](./adoption-spec.md)
4. [`migration-strategy.md`](./migration-strategy.md)
5. [`project-selection-mapping.md`](./project-selection-mapping.md)
6. [`roles/README.md`](./roles/README.md)

## 바로 확인할 것

- 현재 build/test/run 명령
- 실제 배포 방식과 환경 목록
- config, secret, profile 위치
- DB ownership 여부
- 현재 문서 gap
- current stack과 target stack의 차이
- rollback 가능성
- parity requirement

## 처음에 필요한 역할

- 항상 시작:
  - `orchestrator`
  - `legacy-analyst`
  - `migration-planner`
  - `runtime-engineer`
  - `qa-validator`
  - `docs-operator`
- 조건부:
  - `data-steward`
  - `security-reviewer`
  - `compatibility-reviewer`
  - `refactor-guardian`
  - `cutover-manager`

## adoption 시작 체크

1. `scripts/analyze_repository.py` 실행 또는 동등 inventory 확보
2. `.agent-base/repository-inventory.json` 초안 생성
3. adoption spec 확정
4. migration strategy 확정
5. parity validation 계획 작성
6. `checklists/project-adoption.md`
7. `checklists/migration-readiness.md`
