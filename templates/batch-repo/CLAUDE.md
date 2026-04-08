@AGENTS.md

## Claude Code Adapter

- Treat `AGENTS.md` as the canonical entry file for this repository.
- Use `docs/ai/` as the system of record for detailed rules.
- If this file and `AGENTS.md` ever conflict, follow `AGENTS.md` and the referenced detailed docs.
- Keep Claude-specific notes short and tool-specific.

## Claude-Specific Notes

- For large or multi-layer changes, prefer planning before implementation.
- When a change spans code, config, DB, docs, and rollout, consult `docs/ai/lifecycle.md`.
- When generating new documentation, use `docs/ai/prompts/README.md`.
- If Claude can expose the current model tier, compare it with `.agent-base/model-routing.json`.
- If Claude only exposes the model name, resolve it with `.agent-base/model-tier-map.json` before trusting automated tier warnings.
