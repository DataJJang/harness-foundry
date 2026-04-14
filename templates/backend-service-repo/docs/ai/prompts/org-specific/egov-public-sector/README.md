# eGov Public-Sector Prompt Pack

이 디렉토리는 `전자정부프레임워크`, `공공기관 웹서비스`, `KRDS/UI·UX 기준`, `brownfield migration` 성격이 강한 프로젝트에서만 쓰는 선택형 prompt pack이다.

보통은 spec 또는 bootstrap 인터뷰에서 `organizationProfile = egov-public-sector`로 기록하고 이 pack을 활성화한다.

사용 기준:

- 공통 prompt만으로는 공공 프로젝트 특유의 질문 순서와 제약 확인이 부족할 때
- 전자정부프레임워크 기반 신규 구축, 유지보수, 고도화, 이관 작업일 때
- KRDS, 접근성, 운영 반영 절차, parity/rollback 문서를 먼저 맞춰야 할 때

포함 문서:

- `egov-bootstrap.md`
- `egov-adoption.md`
- `egov-new-project-kickoff.md`
- `egov-ui-accessibility-review.md`
- `egov-public-form-list-review.md`

기본 원칙:

- 먼저 공통 규칙인 `AGENTS.md`, `docs/ai/README.md`, `docs/ai/prompts/README.md`를 따른다.
- 이 디렉토리의 문서는 공통 규칙을 대체하지 않고, 공공 프로젝트용 overlay만 제공한다.
- 별도 family를 만들기보다 공통 family + `constraintMode` + migration/parity 문서 조합으로 푼다.

신규 공공 프로젝트에서 `web-app`, `backend-service`, `batch-worker`를 함께 시작한다면 `egov-new-project-kickoff.md`, `docs/ai/org-specific/egov-new-project-playbook.md`, `docs/ai/org-specific/egov-delivery-devops-scm-guide.md`를 같이 쓰는 편이 좋다.
