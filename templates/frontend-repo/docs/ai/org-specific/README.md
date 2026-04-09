# Organization Profiles

이 디렉토리는 `projectFamily`를 대체하지 않는 조직/도메인 overlay를 담는다.

핵심 원칙:

- family는 서비스 구조를 고른다.
- organization profile은 문서, prompt, refinement, checklist overlay를 고른다.
- 즉, `web-app`, `backend-service` 같은 공통 family는 유지하고 조직/도메인 규칙만 profile로 덧씌운다.

현재 profile:

| profile | 용도 | 비고 |
| --- | --- | --- |
| `none` | 공통 baseline만 사용 | 기본값 |
| `egov-public-sector` | 전자정부프레임워크, KRDS, 공공 SI, legacy brownfield | 별도 family를 만들지 않고 overlay만 활성화 |

`organizationProfile = egov-public-sector`을 쓰면 아래를 같이 읽는 편이 좋다.

- `docs/ai/org-specific/egov-public-sector-guide.md`
- `docs/ai/org-specific/egov-new-project-playbook.md`
- `docs/ai/prompts/org-specific/egov-public-sector/README.md`
- `checklists/public-sector-ui-review.md`

생성기와 bootstrap CLI는 `organizationProfile` 값을 spec, context manifest, generation manifest에 함께 남긴다.
