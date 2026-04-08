# aitelecom-admin Prompt Pack

기준 문서:

- [`AGENTS.md`](../../../../../AGENTS.md)
- [`docs/ai/services/frontend.md`](../../../services/frontend.md)
- [`docs/ai/governance/quality-gates.md`](../../../governance/quality-gates.md)

## 대표 경로

- `package.json`
- `.prettierrc`
- `src/App.tsx`
- `src/i18n.ts`
- `src/types/CommonTypes.ts`
- `src/elements/pages`
- `src/elements/components`
- `docs/telegram-operations-admin-manual.md`

## Repo-Specific Prompt Template

```text
Create a repository-specific deliverable for aitelecom-admin.

Repository: aitelecom-admin
Branch: {{BRANCH}}
Goal: {{GOAL}}
Scope: {{SCOPE}}
Target environments: {{ENVIRONMENTS}}
Relevant frontend paths:
- src/elements/pages/{{DOMAIN}}
- src/elements/components
- src/hooks
- src/types/CommonTypes.ts
- src/i18n.ts
Relevant docs:
- docs/telegram-operations-admin-manual.md
- {{DOC_PATH_1}}
Out of scope:
- {{OUT_OF_SCOPE}}

Requirements:
- Follow AGENTS.md and docs/ai/services/frontend.md.
- Use current page naming patterns such as ListPage, DetailPage, RegistrationPage, ModifyPage, Shared, and Api.
- Call out route, menu, i18n, type, and API normalization changes together.
- Include `npm run build` in the validation plan unless a different command is confirmed by source.
- Explicitly note any manual UI verification that still remains.

Output format:
- Purpose
- Scope
- Impacted screens and shared modules
- Detailed tasks
- Validation plan
- Risks and follow-ups
```
