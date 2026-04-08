# First Delivery Checklist

## 1. 문서

- [ ] `AGENTS.md`에서 핵심 상세 문서로 이동 가능하다
- [ ] `project-bootstrap`, `project-generation-spec`, `project-family-map`, `project-selection-mapping`, `stack-matrix`가 저장소 실정에 맞다
- [ ] build/test/배포/운영 관련 문서가 필요한 범위까지 준비되었다
- [ ] DB를 소유하는 저장소면 `database-rules`와 `database-change` 기준이 정리되었다

## 2. 기술 기준

- [ ] 프로젝트 패밀리와 런타임 역할이 명확하다
- [ ] 저장소 구성 방식과 generator v1 한계가 명확하다
- [ ] 언어, 프레임워크, 런타임 버전이 확정되었다
- [ ] 공통 권장값과 다른 항목은 repo-local 오버레이에 기록되었다
- [ ] high-priority refinement module은 해결되었거나 defer 이유가 기록되었다
- [ ] refinement-status가 최신 상태이고 pending/deferred가 설명 가능하다
- [ ] agent-workboard가 최신 상태이고 lane별 owner, scope, next handoff가 설명 가능하다
- [ ] planning -> execution 전환이 있었다면 current handoff packet이 최신 상태다
- [ ] current handoff packet이 있다면 freshness 검증 결과를 설명할 수 있다
- [ ] 첫 build, compile, test 명령이 실제로 동작한다
- [ ] pre-commit hook가 설치되었고 최소 1회 실행 확인이 있다
- [ ] pre-commit preset이 과검사나 누락 없이 저장소 실정과 맞는다

## 3. 검증

- [ ] 최소 1개 이상의 자동 검증이 수행되었다
- [ ] pre-commit local gate 결과를 보고할 수 있다
- [ ] 필요한 수동 smoke 절차가 문서화되었다
- [ ] schema/data change가 있으면 verification query 또는 영향 범위 확인이 준비되었다
- [ ] 미실행 검증과 이유가 명확하다

## 4. 전달 준비

- [ ] 첫 PR 설명에 범위, 검증, 미검증 항목, 운영 영향이 들어간다
- [ ] 배포가 필요한 저장소면 deployment-checklist 초안이 준비되었다
- [ ] 운영성 기능이면 operations-manual 또는 runbook 초안이 준비되었다
- [ ] DB change가 있으면 rollback 또는 backup 메모가 준비되었다
- [ ] 역할 분업이 있었다면 `docs/ai/agent-handoff-log.md`에 baton history가 남아 있다
