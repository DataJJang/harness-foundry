# Project AI Docs

이 디렉토리는 프로젝트 생성, 기존 저장소 온보딩, 역할 분업, 품질 게이트를 위한 상세 system of record다.

루트 진입점은 [`AGENTS.md`](../../AGENTS.md)다.

## 먼저 읽을 것

- 공통 진입:
  - [`context-profiles.md`](./context-profiles.md)
- 새 프로젝트:
  - [`start-bootstrap.md`](./start-bootstrap.md)
- 기존 저장소:
  - [`start-adoption.md`](./start-adoption.md)

## 문서 구조

### Entry Paths

- [`project-bootstrap.md`](./project-bootstrap.md)
- [`project-bootstrap-cli.md`](./project-bootstrap-cli.md)
- [`project-generation-spec.md`](./project-generation-spec.md)
- [`project-adoption.md`](./project-adoption.md)
- [`adoption-spec.md`](./adoption-spec.md)
- [`project-family-map.md`](./project-family-map.md)
- [`project-selection-mapping.md`](./project-selection-mapping.md)

### Core Rules

- [`core-rules.md`](./core-rules.md)
- [`stack-matrix.md`](./stack-matrix.md)
- [`database-rules.md`](./database-rules.md)
- [`lifecycle.md`](./lifecycle.md)
- [`document-routing.md`](./document-routing.md)
- [`architecture-map.md`](./architecture-map.md)
- [`command-catalog.md`](./command-catalog.md)

### Brownfield / Migration

- [`repository-inventory.md`](./repository-inventory.md)
- [`migration-strategy.md`](./migration-strategy.md)
- [`compatibility-matrix.md`](./compatibility-matrix.md)
- [`legacy-exception-policy.md`](./legacy-exception-policy.md)
- [`parity-validation.md`](./parity-validation.md)

### Roles And Prompts

- [`roles/README.md`](./roles/README.md)
  - core roles와 extended roles를 구분해 읽는 기준 포함
- [`prompts/README.md`](./prompts/README.md)
- [`prompts/roles/README.md`](./prompts/roles/README.md)

### Runtime Guides

- [`services/frontend.md`](./services/frontend.md)
- [`services/api.md`](./services/api.md)
- [`services/batch.md`](./services/batch.md)
- [`services/receiver.md`](./services/receiver.md)

### Governance

- [`governance/quality-gates.md`](./governance/quality-gates.md)
- [`governance/git-workflow.md`](./governance/git-workflow.md)
- [`governance/pre-commit-hooks.md`](./governance/pre-commit-hooks.md)
- [`governance/agent-failure-learning.md`](./governance/agent-failure-learning.md)
- [`governance/release-and-rollback.md`](./governance/release-and-rollback.md)
- [`governance/evaluation-and-drift.md`](./governance/evaluation-and-drift.md)

### Tools / Examples

- [`project-generator.md`](./project-generator.md)
- [`context-manifest.md`](./context-manifest.md)
- [`refinement-manifest.md`](./refinement-manifest.md)
- [`refinement-status.md`](./refinement-status.md)
- [`agent-workboard.md`](./agent-workboard.md)
- [`agent-handoff-packets.md`](./agent-handoff-packets.md)
- [`repo-local-overrides.md`](./repo-local-overrides.md)
- [`token-substitution.md`](./token-substitution.md)
- [`tools/compatibility.md`](./tools/compatibility.md)
- [`tools/windsurf.md`](./tools/windsurf.md)
- [`examples/`](./examples/)

## 기본 사용 순서

### Bootstrap

1. `AGENTS.md`
2. `docs/ai/context-profiles.md`
3. `docs/ai/start-bootstrap.md`
4. `docs/ai/project-selection-mapping.md`
5. `docs/ai/roles/README.md`
6. 관련 체크리스트

### Adoption

1. `AGENTS.md`
2. `docs/ai/context-profiles.md`
3. `docs/ai/start-adoption.md`
4. `docs/ai/repository-inventory.md`
5. `docs/ai/project-selection-mapping.md`
6. `docs/ai/roles/README.md`
7. 관련 체크리스트

## 설계 원칙

- entry layer는 가볍게 유지한다.
- bootstrap과 adoption은 시작 경로를 분리한다.
- context depth와 coordination depth는 별도 축으로 설명한다.
- 역할 문서는 `core roles`와 `extended roles`를 구분해 읽는다.
- simple 작업은 필요한 문맥만 먼저 읽고, migration/production/DB-owning 작업일 때만 deep path로 확장한다.
- 템플릿과 생성 스크립트는 이 문서 구조를 기준으로 동기화한다.
