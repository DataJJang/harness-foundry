# Post-Bootstrap Refinement Prompt

이 프롬프트는 bootstrap 이후 생성된 spec과 refinement manifest를 바탕으로, 꼭 필요한 심화 질문만 골라 사용자와 이어서 확정하게 한다.

```text
You are continuing a project bootstrap after the initial spec has already been created.

Read these sources in order:
1. AGENTS.md
2. docs/ai/context-profiles.md
3. docs/ai/project-bootstrap.md
4. docs/ai/refinement-manifest.md
5. docs/ai/refinement-status.md
6. docs/ai/repo-local-overrides.md
7. .agent-base/project-generation-spec.json or the saved spec JSON
8. .agent-base/refinement-manifest.json or the saved *.refinement.json
9. .agent-base/refinement-status.json or the saved *.refinement-status.json when available
10. .agent-base/context-manifest.json when available
11. docs/ai/command-catalog.md
12. docs/ai/architecture-map.md
13. docs/ai/database-rules.md when a data module is triggered
14. docs/ai/governance/release-and-rollback.md when a delivery module is triggered

Your job is to continue the bootstrap in a lightweight way.
Do not restart the whole interview.
Only ask follow-up questions for the modules listed in the refinement manifest.

Rules:
- Ask high-priority modules first.
- Keep questions decision-oriented and bounded.
- For each question, allow one of three outcomes:
  - decide now
  - keep default
  - defer with note
- Do not force the user to over-specify implementation details too early.
- Translate answers into concrete repo-local outputs such as command-catalog, architecture-map, pre-commit-config, overlay notes, deployment-checklist, or operations-manual.
- If a module can be satisfied by explicitly keeping the default, record that and move on.
- If something is deferred, record who or what should resolve it later.
- Update refinement-status and repo-local-overrides as part of the output, not as an optional afterthought.
- When possible, align the result with `python3 scripts/update_refinement_status.py --interactive`.

Required outputs:
- module-by-module decision summary
- decisions made now
- defaults kept intentionally
- deferred items with reasons
- refinement-status fields to update
- docs or config files to update next
- prompts to run next
- verification steps that became possible after the refinement
```
