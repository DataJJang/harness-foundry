# Example Prompt: eGov Public UI Review

다음 저장소는 공공기관 웹서비스 성격이고, JSP/Spring MVC 기반 화면을 일부 개선하려고 한다.

다음 순서로 진행하라.

1. `AGENTS.md`
2. `docs/ai/org-specific/egov-public-sector-guide.md`
3. `checklists/public-sector-ui-review.md`
4. `docs/ai/prompts/org-specific/egov-public-sector/egov-public-form-list-review.md`

그 다음 아래 작업을 수행하라.

- 현재 변경 범위에 해당하는 JSP, controller, service, 공통 JS/CSS, include/layout 파일을 확인한다.
- 검색조건, 결과 목록, 상세/등록/수정, 첨부파일 흐름을 기준으로 대표 패턴과 예외 화면을 구분한다.
- KRDS/접근성 기준에서 우선 수정할 문제를 찾는다.
- 공통 자산 변경으로 인해 다른 화면까지 영향이 갈 수 있는 지점을 표시한다.
- before/after parity가 깨질 수 있는 항목과 수동 검증 시나리오를 정리한다.

반드시 아래 형식으로 답하라.

1. 검토한 화면/파일 범위
2. 공통 패턴과 예외 패턴
3. 주요 문제와 영향 범위
4. 공공 UI/KRDS/접근성 관점 우선 수정 항목
5. parity 검증이 필요한 항목
6. 추천 수정 순서와 남은 리스크
