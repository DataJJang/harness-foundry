# eGov Adoption Prompt

기존 전자정부프레임워크 또는 공공기관 저장소를 onboarding / migration 하려고 한다.

다음 순서로 진행하라.

1. `AGENTS.md`
2. `docs/ai/start-adoption.md`
3. `docs/ai/org-specific/egov-public-sector-guide.md`
4. `docs/ai/repository-inventory.md`
5. `docs/ai/migration-strategy.md`
6. `docs/ai/parity-validation.md`

이후 아래 원칙으로 inventory와 migration 초안을 만들어라.

- 최신화 제안보다 현재 운영 구조 파악을 먼저 한다.
- Spring MVC / Boot, JSP, MyBatis, scheduler, batch, 수신 연계, 공통 JS/CSS, 공통 태그를 먼저 찾는다.
- 화면/API/배치/연계 중 실제 변경 범위를 먼저 분리한다.
- 공공 프로젝트 특유의 검수, 반영, rollback, parity 요구를 별도 항목으로 남긴다.
- KRDS 또는 공공 UI/UX 기준 영향이 있으면 UI layer에 별도로 표시한다.

출력 형식:

1. 현재 구조 요약
2. 자동 파악된 legacy hotspot
3. fixed-target 또는 legacy-maintenance 필요 여부
4. migration 우선순위
5. parity validation이 꼭 필요한 영역
6. 공공 프로젝트 특화 리스크
