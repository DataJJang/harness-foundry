# eGov New Project Kickoff Prompt

전자정부프레임워크 기반 신규 프로젝트를 시작하려고 한다.
전제는 `web-app`, `backend-service`, `batch-worker`를 함께 구성하는 형태다.

먼저 아래 문서를 읽고 진행하라.

1. `AGENTS.md`
2. `docs/ai/start-bootstrap.md`
3. `docs/ai/org-specific/egov-public-sector-guide.md`
4. `docs/ai/org-specific/egov-new-project-playbook.md`
5. `checklists/egov-new-project-kickoff.md`

이후 아래 원칙으로 진행하라.

- 질문은 적게 하고 좁게 한다.
- 작은 팀 기준으로 과도한 multi-agent 절차를 먼저 늘리지 않는다.
- 최신 baseline보다 기관 운영 환경, 발주 형식, 기존 공통 산출물 제약을 우선한다.
- frontend, backend, batch를 따로 보되 공통 산출물과 반영 순서는 함께 정리한다.
- 구현부터 들어가지 말고, 먼저 착수 전 기준을 고정한다.

반드시 먼저 확인할 것:

- 대민 서비스인지 내부 업무 시스템인지
- KRDS 또는 기관 UI/UX 기준 적용 여부
- 전자정부프레임워크 버전, WAS, JDK, OS 같은 고정 운영 제약 여부
- DB ownership과 batch 운영 여부
- 공통 코드, 공통 JS/CSS, 공통 메시지, 공통 코드 테이블 같은 공통 자산 존재 여부
- 신규처럼 보여도 기존 기관 산출물/운영 절차를 따라야 하는지

출력 형식:

1. 추천 project family / runtime roles
2. `constraintMode` 추천과 이유
3. 지금 바로 확정해야 할 공통 항목
4. frontend에서 먼저 고정할 항목
5. backend에서 먼저 고정할 항목
6. batch에서 먼저 고정할 항목
7. 세 프로젝트를 묶어 맞춰야 할 통합 항목
8. 생성 직후부터 개발 착수 전까지의 실행 순서
9. 아직 미확정이라 refinement로 넘겨도 되는 항목

## Copy-Paste Quick Prompt

```text
`source/AGENTS.md`, `source/docs/ai/start-bootstrap.md`,
`source/docs/ai/org-specific/egov-public-sector-guide.md`,
`source/docs/ai/org-specific/egov-new-project-playbook.md`,
`source/checklists/egov-new-project-kickoff.md`
를 읽고,
전자정부프레임워크 기반 신규 프로젝트 bootstrap을 도와줘.

전제는 `web-app`, `backend-service`, `batch-worker`를 함께 구성하는 형태야.
작은 팀 기준으로 질문은 꼭 필요한 것만 좁혀서 해주고,
먼저 확정해야 할 공통 항목과
frontend / backend / batch별 착수 전 작업,
그리고 세 프로젝트를 함께 맞춰야 할 통합 기준을 정리해줘.

최신 baseline보다 기관 운영 제약이 우선이면 그 기준을 먼저 잠그고,
필요하면 `constraintMode = fixed-target` 또는 `legacy-maintenance`도 제안해줘.
```

## Post-Generation Prompt

생성 후 각 저장소에서 바로 이어갈 때는 아래처럼 요청하면 된다.

```text
`AGENTS.md`, `.agent-base/context-manifest.json`,
`.agent-base/refinement-manifest.json`,
`docs/ai/org-specific/egov-new-project-playbook.md`,
`checklists/egov-new-project-kickoff.md`
를 읽고,
이 저장소가 frontend / backend / batch 중 어디에 해당하는지 기준으로
지금 먼저 고정해야 할 항목 5개와
첫 build/test/smoke 전에 해야 할 작업만 정리해줘.
```
