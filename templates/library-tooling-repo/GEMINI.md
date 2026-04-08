# Project Gemini Adapter

This repository uses `AGENTS.md` as the canonical AI rules entrypoint.

## Start Here

- Read [`AGENTS.md`](./AGENTS.md) first.
- Then use [`docs/ai/README.md`](./docs/ai/README.md) as the detailed system of record.

## Core Guidance

- Follow existing repository patterns before inventing new ones.
- Treat `docs/ai/` as the source of detailed coding, lifecycle, service, and quality rules.
- Do not expose secrets, tokens, or production identifiers.
- Keep changes backward-compatible where possible.
- Run at least one relevant verification step before concluding work.

## Quick Map

- Frontend rules: [`docs/ai/services/frontend.md`](./docs/ai/services/frontend.md)
- API rules: [`docs/ai/services/api.md`](./docs/ai/services/api.md)
- Batch rules: [`docs/ai/services/batch.md`](./docs/ai/services/batch.md)
- Receiver rules: [`docs/ai/services/receiver.md`](./docs/ai/services/receiver.md)
- Prompt templates: [`docs/ai/prompts/README.md`](./docs/ai/prompts/README.md)
- Model tier policy: [`docs/ai/governance/model-routing.md`](./docs/ai/governance/model-routing.md)
- Model name mapping fallback: [`docs/ai/tools/model-tier-mapping.md`](./docs/ai/tools/model-tier-mapping.md)
