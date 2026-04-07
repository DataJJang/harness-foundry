# Project Agent Entry

This file is the canonical AI entrypoint for a repository that uses this template pack.

## Start In The Right Mode

- New repository or new project: read [`docs/ai/start-bootstrap.md`](./docs/ai/start-bootstrap.md)
- Existing repository, conversion, migration, or onboarding: read [`docs/ai/start-adoption.md`](./docs/ai/start-adoption.md)
- Context-loading and light vs deep read paths: read [`docs/ai/context-profiles.md`](./docs/ai/context-profiles.md)

## Fast Path

Read only these first:

1. This `AGENTS.md`
2. [`docs/ai/context-profiles.md`](./docs/ai/context-profiles.md)
3. One of:
   - [`docs/ai/start-bootstrap.md`](./docs/ai/start-bootstrap.md)
   - [`docs/ai/start-adoption.md`](./docs/ai/start-adoption.md)
4. [`docs/ai/project-selection-mapping.md`](./docs/ai/project-selection-mapping.md)
5. [`docs/ai/roles/README.md`](./docs/ai/roles/README.md)
6. [`docs/ai/governance/quality-gates.md`](./docs/ai/governance/quality-gates.md)

## Core Concepts

- Project families:
  - `game`, `web-app`, `pwa`, `mobile-app`, `backend-service`, `batch-worker`, `receiver-integration`, `mockup-local`, `library-tooling`
- Runtime roles:
  - `frontend`, `api`, `batch`, `receiver`, `client`, `tooling`, `worker`
- Core agent roles:
  - `orchestrator`, `bootstrap-planner`, `runtime-engineer`, `qa-validator`, `docs-operator`
- Conditional core agent roles:
  - `data-steward` for schema/data/query ownership
  - `security-reviewer` for auth, secrets, production exposure, or public API changes
- Extended agent roles:
  - deeper planning, migration, compatibility, cutover, release, and failure-learning specialists

## What To Read Next

- Bootstrap flow:
  - [`docs/ai/project-bootstrap.md`](./docs/ai/project-bootstrap.md)
  - [`docs/ai/project-bootstrap-cli.md`](./docs/ai/project-bootstrap-cli.md)
  - [`docs/ai/project-generation-spec.md`](./docs/ai/project-generation-spec.md)
  - [`docs/ai/project-generator.md`](./docs/ai/project-generator.md)
- Adoption flow:
  - [`docs/ai/project-adoption.md`](./docs/ai/project-adoption.md)
  - [`docs/ai/adoption-spec.md`](./docs/ai/adoption-spec.md)
  - [`docs/ai/repository-inventory.md`](./docs/ai/repository-inventory.md)
  - [`docs/ai/migration-strategy.md`](./docs/ai/migration-strategy.md)
  - [`docs/ai/parity-validation.md`](./docs/ai/parity-validation.md)
- Technology and policy:
  - [`docs/ai/stack-matrix.md`](./docs/ai/stack-matrix.md)
  - [`docs/ai/database-rules.md`](./docs/ai/database-rules.md)
  - [`docs/ai/core-rules.md`](./docs/ai/core-rules.md)
  - [`docs/ai/lifecycle.md`](./docs/ai/lifecycle.md)
- Roles, prompts, and checklists:
  - [`docs/ai/roles/README.md`](./docs/ai/roles/README.md)
  - [`docs/ai/prompts/README.md`](./docs/ai/prompts/README.md)
  - [`checklists/agent-role-selection.md`](./checklists/agent-role-selection.md)
  - [`checklists/agent-handoff.md`](./checklists/agent-handoff.md)

## Non-Negotiables

- Follow the nearest existing code and directory pattern before inventing structure.
- Do not commit secrets, tokens, production credentials, or real personal identifiers.
- Prefer compatible changes over breaking changes.
- Do not run destructive DB commands without approval, rollback or backup notes, and verification queries.
- Do not push without at least one relevant verification step.
- Shared delivery must name an implementation owner, validator, and documentation owner.
- DB-owning changes must include `data-steward` responsibilities.
- Production-significant security changes must include `security-reviewer` output.
- Repeated failures must be recorded and fed back into the harness.

## Where Commands Live

- Web and app repos: `package.json`, `pubspec.yaml`, repo-local scripts
- Java repos: `build.gradle`
- Unity repos: Unity version docs, project settings, repo-local automation
- Environment keys: `application.yml`, `.env*`, platform config files
- Repo-local command truth: [`docs/ai/command-catalog.md`](./docs/ai/command-catalog.md)

## Tool Adapters

- Claude Code: [`CLAUDE.md`](./CLAUDE.md)
- Gemini CLI: [`GEMINI.md`](./GEMINI.md)
- GitHub Copilot: [`.github/copilot-instructions.md`](./.github/copilot-instructions.md)
- Cursor: [`.cursor/rules/00-base.mdc`](./.cursor/rules/00-base.mdc)

## Migration Pointers

- [`codex.md`](./codex.md) and [`codex-prompts.md`](./codex-prompts.md) are compatibility pointers only.
