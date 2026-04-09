# eGov Bootstrap Prompt

전자정부프레임워크 또는 공공기관 프로젝트를 bootstrap하려고 한다.

다음 순서로 진행하라.

1. `AGENTS.md`
2. `docs/ai/start-bootstrap.md`
3. `docs/ai/org-specific/egov-public-sector-guide.md`
4. `docs/ai/project-generation-spec.md`
5. `docs/ai/project-selection-mapping.md`

이후 아래 원칙으로 질문하라.

- 질문은 좁고 현실적으로 한다.
- 작은 팀 기준으로, 과도한 multi-agent 절차를 먼저 늘리지 않는다.
- 신규 프로젝트라도 운영 환경, 발주 형식, 기존 공통컴포넌트/공통 템플릿 제약이 있으면 `fixed-target` 또는 `legacy-maintenance` 가능성을 먼저 확인한다.
- 전자정부 프로젝트라고 해서 별도 family를 만들지 말고, 기존 family 조합으로 분류한다.

반드시 먼저 확인할 것:

- 대민 서비스인지 내부 업무 시스템인지
- UI가 KRDS 또는 공공 UI/UX 기준을 따라야 하는지
- 전자정부프레임워크 버전 또는 고정 운영 환경이 있는지
- DB ownership과 운영 배치가 있는지
- 신규처럼 보여도 기존 공통 산출물/운영 절차를 따라야 하는지

출력 형식:

1. 추천 project family / runtime roles
2. `constraintMode` 추천과 이유
3. 먼저 확정할 항목 5개
4. 나중 refinement로 미뤄도 되는 항목
5. public-sector 특화 주의사항
