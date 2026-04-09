# Prompt Examples

이 디렉토리는 새 저장소 시작 시 바로 복사해 실행할 수 있는 예시 프롬프트를 제공한다.

## 권장 사용 순서

1. [`project-bootstrap.md`](./project-bootstrap.md)
2. 프로젝트 패밀리별 bootstrap 예시 중 하나
3. [`project-generator-run.md`](./project-generator-run.md)
4. [`test-plan.md`](./test-plan.md)
5. DB를 소유하는 저장소면 [`database-review.md`](./database-review.md)
6. 필요 시 [`deployment-checklist.md`](./deployment-checklist.md)
7. 필요 시 [`operations-manual.md`](./operations-manual.md)
8. 구조나 영향이 클 때 [`impact-analysis.md`](./impact-analysis.md)
9. 반복 실수나 규약 갭이 보이면 [`agent-failure-review.md`](./agent-failure-review.md)
10. 공공/전자정부 UI 검토가 필요하면 [`egov-public-ui-review.md`](./egov-public-ui-review.md)

## 주의사항

- 예시는 시작점이다. 실제 저장소명, 브랜치, 코드 경로, 설정 경로로 치환해서 사용한다.
- 실토큰, 실운영 URL, 실계정은 넣지 않는다.
- 산출물에는 항상 검증 기준과 미검증 항목을 포함하게 한다.
- schema, migration, seed, data correction이 있으면 naming과 risky SQL review를 빠뜨리지 않는다.
- 새 프로젝트는 반드시 `projectFamily`, `projectNature`, `runtimeRole[]`, `language`, `framework`, `deploymentType`가 결과물에 남아야 한다.
- 실패 케이스를 정리할 때는 재현 조건, root cause, 강화 위치, 재검증 계획까지 포함한다.
- 실패 기록을 남길 때는 먼저 `python3 scripts/record_agent_failure.py`로 기본 메타데이터를 남기고, 그 뒤 prompt로 강화 계획을 정리한다.
