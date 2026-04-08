#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT
TEMPLATES_DIR = ROOT.parent / "templates"
SCAFFOLDS_DIR = ROOT / "scaffolds"

TEMPLATE_BY_FAMILY = {
    "game": "game-repo",
    "web-app": "web-app-repo",
    "pwa": "pwa-repo",
    "mobile-app": "mobile-app-repo",
    "backend-service": "backend-service-repo",
    "batch-worker": "batch-worker-repo",
    "receiver-integration": "receiver-integration-repo",
    "mockup-local": "mockup-local-repo",
    "library-tooling": "library-tooling-repo",
}

TEXT_SUFFIXES = {
    ".md",
    ".txt",
    ".json",
    ".yml",
    ".yaml",
    ".gradle",
    ".kts",
    ".xml",
    ".ts",
    ".tsx",
    ".js",
    ".jsx",
    ".css",
    ".html",
    ".dart",
    ".java",
    ".cs",
    ".properties",
    ".webmanifest",
    ".gitignore",
}

DEFAULT_PRECOMMIT_CONFIG = {
    "mode": "auto",
    "presetProfile": "auto",
    "customCommands": [],
    "additionalCommands": [],
    "unityValidationCommands": [],
    "runLintOnHook": True,
    "runTypecheckOnHook": True,
    "runBuildOnHook": False,
    "runTestOnHook": False,
    "failWhenNoChecksRun": False,
}

ROLE_BASELINE_BY_FAMILY = {
    "game": {
        "required": ["orchestrator", "bootstrap-planner", "runtime-engineer", "qa-validator", "docs-operator"],
        "optional": ["product-analyst", "solution-architect", "release-manager", "failure-curator"],
        "specializations": ["runtime-engineer: game"],
    },
    "web-app": {
        "required": ["orchestrator", "bootstrap-planner", "runtime-engineer", "qa-validator", "docs-operator"],
        "optional": ["product-analyst", "solution-architect", "security-reviewer", "release-manager", "failure-curator"],
        "specializations": ["runtime-engineer: frontend"],
    },
    "pwa": {
        "required": ["orchestrator", "bootstrap-planner", "runtime-engineer", "security-reviewer", "qa-validator", "docs-operator"],
        "optional": ["product-analyst", "solution-architect", "release-manager", "failure-curator"],
        "specializations": ["runtime-engineer: frontend"],
    },
    "mobile-app": {
        "required": ["orchestrator", "runtime-engineer", "qa-validator", "docs-operator"],
        "optional": ["product-analyst", "security-reviewer", "release-manager", "failure-curator"],
        "specializations": ["runtime-engineer: mobile"],
    },
    "backend-service": {
        "required": [
            "orchestrator",
            "bootstrap-planner",
            "runtime-engineer",
            "data-steward",
            "security-reviewer",
            "qa-validator",
            "docs-operator",
        ],
        "optional": ["product-analyst", "solution-architect", "release-manager", "failure-curator"],
        "specializations": ["runtime-engineer: api"],
    },
    "batch-worker": {
        "required": ["orchestrator", "runtime-engineer", "data-steward", "qa-validator", "docs-operator"],
        "optional": ["solution-architect", "security-reviewer", "release-manager", "failure-curator"],
        "specializations": ["runtime-engineer: batch"],
    },
    "receiver-integration": {
        "required": [
            "orchestrator",
            "runtime-engineer",
            "data-steward",
            "security-reviewer",
            "qa-validator",
            "docs-operator",
        ],
        "optional": ["solution-architect", "release-manager", "failure-curator"],
        "specializations": ["runtime-engineer: receiver"],
    },
    "mockup-local": {
        "required": ["orchestrator", "bootstrap-planner", "runtime-engineer", "docs-operator"],
        "optional": ["qa-validator", "failure-curator"],
        "specializations": ["runtime-engineer: frontend"],
    },
    "library-tooling": {
        "required": ["orchestrator", "runtime-engineer", "qa-validator", "docs-operator"],
        "optional": ["solution-architect", "failure-curator"],
        "specializations": ["runtime-engineer: tooling"],
    },
}


CONTEXT_BUDGET = {
    "entryDocs": 3,
    "roleDocs": 3,
    "checklists": 2,
}

COORDINATION_MODE_LABELS = {
    "lite": "Lite",
    "coordinated": "Coordinated",
    "full": "Full",
}

COORDINATION_MODE_SUMMARIES = {
    "lite": "짧은 기본 경로로 시작하고, 실제 blocker가 생길 때만 coordination artifact를 넓힌다.",
    "coordinated": "핵심 refinement와 execution handoff만 고정하고, 나머지는 필요 시에만 확장한다.",
    "full": "DB, security, release, multi-lane handoff를 포함한 전체 coordination 흐름을 기본 절차로 쓴다.",
}

RUNTIME_REFINEMENT_BY_FAMILY = {
    "game": {
        "title": "Game Runtime Shape",
        "questions": [
            "core scene/bootstrap path를 어디까지 기본 구조로 둘지 정했는가?",
            "asset, content pipeline, editor automation 중 무엇을 먼저 문서화할지 정했는가?",
            "playmode/editmode 또는 validation method 중 첫 검증 기준은 무엇인가?",
        ],
        "recommendedOutputs": [
            "docs/ai/architecture-map.md",
            "docs/ai/command-catalog.md",
            "build-guide or validation guide",
        ],
        "recommendedPrompts": ["post-bootstrap-refinement", "build-guide", "test-plan"],
        "agentRoles": ["runtime-engineer", "qa-validator", "docs-operator"],
    },
    "web-app": {
        "title": "Frontend Runtime Shape",
        "questions": [
            "route, page, shared component, API binding 구조를 어떤 기준으로 둘지 정했는가?",
            "env 파일, API base URL, build target의 source of truth는 어디인가?",
            "UI smoke와 build 검증 중 첫 전달 기준은 무엇인가?",
        ],
        "recommendedOutputs": [
            "docs/ai/architecture-map.md",
            "docs/ai/command-catalog.md",
            "build-guide",
        ],
        "recommendedPrompts": ["post-bootstrap-refinement", "build-guide", "test-plan", "frontend"],
        "agentRoles": ["runtime-engineer", "qa-validator", "docs-operator"],
    },
    "pwa": {
        "title": "PWA Runtime Shape",
        "questions": [
            "offline/cache/installability 범위를 실제로 어디까지 지원할지 정했는가?",
            "route, API binding, env source of truth를 어디에 둘지 정했는가?",
            "installability/offline smoke 절차를 첫 검증에 포함할지 정했는가?",
        ],
        "recommendedOutputs": [
            "docs/ai/architecture-map.md",
            "docs/ai/command-catalog.md",
            "deployment-checklist or runbook note for cache behavior",
        ],
        "recommendedPrompts": ["post-bootstrap-refinement", "build-guide", "test-plan", "frontend"],
        "agentRoles": ["runtime-engineer", "qa-validator", "docs-operator"],
    },
    "mobile-app": {
        "title": "Mobile Runtime Shape",
        "questions": [
            "platform config, signing, release versioning의 source of truth는 어디인가?",
            "device/simulator smoke와 build 검증 중 첫 전달 기준은 무엇인가?",
            "backend binding과 runtime env 분기 기준을 어디에 기록할지 정했는가?",
        ],
        "recommendedOutputs": [
            "docs/ai/architecture-map.md",
            "docs/ai/command-catalog.md",
            "build-guide",
        ],
        "recommendedPrompts": ["post-bootstrap-refinement", "build-guide", "test-plan"],
        "agentRoles": ["runtime-engineer", "qa-validator", "docs-operator"],
    },
    "backend-service": {
        "title": "API Service Shape",
        "questions": [
            "controller/service/repository/query 책임 경계를 어디까지 분리할지 정했는가?",
            "profile, env, security, DB config의 source of truth를 어디에 둘지 정했는가?",
            "첫 compile/test/smoke와 health/auth 기준은 무엇인가?",
        ],
        "recommendedOutputs": [
            "docs/ai/architecture-map.md",
            "docs/ai/command-catalog.md",
            "operations-manual",
        ],
        "recommendedPrompts": ["post-bootstrap-refinement", "build-guide", "test-plan", "api"],
        "agentRoles": ["runtime-engineer", "security-reviewer", "qa-validator", "docs-operator"],
    },
    "batch-worker": {
        "title": "Batch Runtime Shape",
        "questions": [
            "job, service, mapper, model, scheduler 경계를 어디까지 문서화할지 정했는가?",
            "운영 SQL/runbook과 batch smoke 기준을 무엇으로 둘지 정했는가?",
            "scheduler enable flag와 수동 실행 경로를 어디에 기록할지 정했는가?",
        ],
        "recommendedOutputs": [
            "docs/ai/architecture-map.md",
            "docs/ai/command-catalog.md",
            "operations-manual",
        ],
        "recommendedPrompts": ["post-bootstrap-refinement", "build-guide", "test-plan", "batch"],
        "agentRoles": ["runtime-engineer", "data-steward", "qa-validator", "docs-operator"],
    },
    "receiver-integration": {
        "title": "Receiver Runtime Shape",
        "questions": [
            "ingress, parser, handler, publish 흐름을 어떤 파일 경계로 둘지 정했는가?",
            "sample payload, retry, diagnostics 기준을 어디에 남길지 정했는가?",
            "broker/port/topic/publish target 검증 절차를 무엇으로 둘지 정했는가?",
        ],
        "recommendedOutputs": [
            "docs/ai/architecture-map.md",
            "docs/ai/command-catalog.md",
            "operations-manual",
        ],
        "recommendedPrompts": ["post-bootstrap-refinement", "build-guide", "test-plan", "receiver"],
        "agentRoles": ["runtime-engineer", "security-reviewer", "qa-validator", "docs-operator"],
    },
    "mockup-local": {
        "title": "Mockup Runtime Shape",
        "questions": [
            "로컬 실행 범위와 데모 시나리오를 어디까지 포함할지 정했는가?",
            "실데이터/실연동 없이도 보여줄 핵심 흐름이 무엇인지 정했는가?",
            "preview 명령과 walkthrough 절차를 어디에 기록할지 정했는가?",
        ],
        "recommendedOutputs": [
            "docs/ai/architecture-map.md",
            "docs/ai/command-catalog.md",
            "build-guide",
        ],
        "recommendedPrompts": ["post-bootstrap-refinement", "build-guide", "test-plan"],
        "agentRoles": ["runtime-engineer", "docs-operator"],
    },
    "library-tooling": {
        "title": "Tooling Runtime Shape",
        "questions": [
            "library, CLI, helper script 중 무엇이 첫 public surface인지 정했는가?",
            "sample invocation과 package smoke 기준을 어디에 기록할지 정했는가?",
            "runtime dependency와 install path의 source of truth를 어디로 둘지 정했는가?",
        ],
        "recommendedOutputs": [
            "docs/ai/architecture-map.md",
            "docs/ai/command-catalog.md",
            "build-guide",
        ],
        "recommendedPrompts": ["post-bootstrap-refinement", "build-guide", "test-plan"],
        "agentRoles": ["runtime-engineer", "qa-validator", "docs-operator"],
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a sample project from harness-foundry.")
    parser.add_argument("--spec", required=True, help="Path to project generation spec JSON")
    parser.add_argument("--output-root", required=True, help="Directory where the project will be created")
    parser.add_argument("--force", action="store_true", help="Overwrite the target directory if it exists")
    return parser.parse_args()


def load_spec(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fp:
        spec = json.load(fp)
    spec = normalize_spec(spec)
    validate_spec(spec)
    return spec


def validate_spec(spec: dict) -> None:
    required = [
        "repositoryName",
        "projectName",
        "projectPurpose",
        "projectFamily",
        "projectNature",
        "repositoryMode",
        "targetUsers",
        "targetPlatforms",
        "runtimeRoles",
        "language",
        "runtimeVersion",
        "framework",
        "buildTool",
        "testTool",
        "datastore",
        "cache",
        "deploymentType",
        "startupMode",
        "loggingMode",
        "targetOs",
        "securityProfile",
        "targetEnvironments",
        "externalIntegrations",
        "baseDocumentSet",
    ]
    missing = [key for key in required if key not in spec]
    if missing:
        raise ValueError(f"Missing required spec keys: {', '.join(missing)}")

    if spec["projectFamily"] not in TEMPLATE_BY_FAMILY:
        raise ValueError(f"Unsupported projectFamily: {spec['projectFamily']}")

    if isinstance(spec["runtimeRoles"], list) and not spec["runtimeRoles"]:
        raise ValueError("runtimeRoles must contain at least one item")

    if spec["language"].lower() == "java" and not spec.get("packageName"):
        raise ValueError("packageName is required for Java-based scaffolds")

    coordination_keys = [
        "requiredAgentRoles",
        "optionalAgentRoles",
        "roleSpecializations",
        "agentWorkflowOrder",
        "agentRoleOverrides",
    ]
    missing_coordination = [key for key in coordination_keys if key not in spec]
    if missing_coordination:
        raise ValueError(f"Missing coordination spec keys: {', '.join(missing_coordination)}")


def slug_to_pascal(value: str) -> str:
    parts = re.split(r"[^A-Za-z0-9]+", value)
    return "".join(part[:1].upper() + part[1:] for part in parts if part)


def unique(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item and item not in seen:
            seen.add(item)
            result.append(item)
    return result


def runtime_specializations(spec: dict) -> list[str]:
    specializations: list[str] = []
    runtime_roles = set(spec.get("runtimeRoles", []))
    family = spec["projectFamily"]

    if "frontend" in runtime_roles:
        specializations.append("runtime-engineer: frontend")
    if "api" in runtime_roles:
        specializations.append("runtime-engineer: api")
    if "batch" in runtime_roles:
        specializations.append("runtime-engineer: batch")
    if "receiver" in runtime_roles:
        specializations.append("runtime-engineer: receiver")
    if "tooling" in runtime_roles:
        specializations.append("runtime-engineer: tooling")
    if "client" in runtime_roles and family == "game":
        specializations.append("runtime-engineer: game")
    if "client" in runtime_roles and family == "mobile-app":
        specializations.append("runtime-engineer: mobile")
    if not specializations and family in ROLE_BASELINE_BY_FAMILY:
        specializations.extend(ROLE_BASELINE_BY_FAMILY[family]["specializations"])
    return unique(specializations)


def derive_agent_coordination(spec: dict) -> dict[str, list[str]]:
    baseline = ROLE_BASELINE_BY_FAMILY[spec["projectFamily"]]
    required = list(baseline["required"])
    optional = list(baseline["optional"])
    specializations = runtime_specializations(spec)

    if spec.get("datastore") == "없음":
        required = [role for role in required if role != "data-steward"]
        optional = [role for role in optional if role != "data-steward"]
    elif spec.get("schemaOwnership") in {"owned", "shared"} and "data-steward" not in required:
        required.append("data-steward")

    security_needed = spec.get("securityProfile") != "없음" or spec.get("projectNature") == "production"
    if security_needed and "security-reviewer" not in required:
        required.append("security-reviewer")
    if not security_needed:
        optional = [role for role in optional if role != "security-reviewer"]

    release_needed = spec.get("deploymentType") != "local-only" or spec.get("projectNature") == "production"
    if release_needed and "release-manager" not in optional:
        optional.append("release-manager")

    workflow = [
        role
        for role in [
            "orchestrator",
            "bootstrap-planner",
            "runtime-engineer",
            "data-steward",
            "security-reviewer",
            "qa-validator",
            "docs-operator",
            "product-analyst",
            "solution-architect",
            "release-manager",
            "failure-curator",
        ]
        if role in required or role in optional
    ]

    return {
        "requiredAgentRoles": unique(required),
        "optionalAgentRoles": unique(optional),
        "roleSpecializations": specializations,
        "agentWorkflowOrder": workflow,
        "agentRoleOverrides": list(spec.get("agentRoleOverrides", [])),
    }


def derive_coordination_mode(spec: dict) -> dict[str, object]:
    coordinated_reasons: list[str] = []
    full_reasons: list[str] = []
    target_environments = spec.get("targetEnvironments", [])

    if spec.get("repositoryMode") != "single-repo":
        full_reasons.append(f"repositoryMode is `{spec['repositoryMode']}`.")
    if spec.get("projectNature") == "production":
        full_reasons.append("projectNature is `production`.")
    if spec.get("deploymentType") != "local-only" and len(target_environments) >= 3:
        full_reasons.append(
            "non-local deployment spans three or more target environments."
        )
    if spec.get("schemaOwnership") in {"owned", "shared"}:
        full_reasons.append(f"schemaOwnership is `{spec['schemaOwnership']}`.")
    if len(spec.get("runtimeRoles", [])) > 1 and spec.get("datastore") != "없음":
        full_reasons.append("multiple runtime roles share a datastore boundary.")

    if spec.get("datastore") != "없음":
        coordinated_reasons.append(f"datastore is `{spec['datastore']}`.")
    if spec.get("securityProfile") != "없음":
        coordinated_reasons.append(f"securityProfile is `{spec['securityProfile']}`.")
    if spec.get("deploymentType") != "local-only":
        coordinated_reasons.append(f"deploymentType is `{spec['deploymentType']}`.")
    if spec.get("externalIntegrations"):
        coordinated_reasons.append(
            "external integrations are declared: " + ", ".join(spec["externalIntegrations"]) + "."
        )

    if full_reasons:
        mode = "full"
        reasons = unique(full_reasons + coordinated_reasons)
    elif coordinated_reasons:
        mode = "coordinated"
        reasons = unique(coordinated_reasons)
    else:
        mode = "lite"
        reasons = [
            "single-repo, local-first bootstrap with no DB, security, deployment, or external-integration risk trigger was detected."
        ]

    return {
        "mode": mode,
        "label": COORDINATION_MODE_LABELS[mode],
        "summary": COORDINATION_MODE_SUMMARIES[mode],
        "reasons": reasons,
    }


def derive_context_manifest(spec: dict) -> dict:
    mode = "bootstrap"
    coordination_mode = derive_coordination_mode(spec)
    fast_path_docs = [
        "AGENTS.md",
        "docs/ai/context-profiles.md",
        "docs/ai/start-bootstrap.md",
        "docs/ai/project-selection-mapping.md",
        "docs/ai/roles/README.md",
        "docs/ai/governance/quality-gates.md",
    ]
    deep_path_docs = [
        "docs/ai/project-bootstrap.md",
        "docs/ai/project-bootstrap-cli.md",
        "docs/ai/project-generation-spec.md",
        "docs/ai/project-generator.md",
        "docs/ai/stack-matrix.md",
    ]
    if spec.get("datastore") != "없음" or spec.get("schemaOwnership") in {"owned", "shared"}:
        deep_path_docs.append("docs/ai/database-rules.md")
    if spec.get("projectNature") == "production" or spec.get("deploymentType") != "local-only":
        deep_path_docs.append("docs/ai/lifecycle.md")

    return {
        "mode": mode,
        "projectFamily": spec["projectFamily"],
        "runtimeRoles": spec.get("runtimeRoles", []),
        "fastPathDocs": fast_path_docs,
        "deepPathDocs": unique(deep_path_docs),
        "recommendedCoordinationMode": coordination_mode["mode"],
        "coordinationModeSummary": coordination_mode["summary"],
        "coordinationModeReasons": list(coordination_mode["reasons"]),
        "coreRoles": spec["requiredAgentRoles"],
        "extendedRoles": spec["optionalAgentRoles"],
        "roleSpecializations": spec["roleSpecializations"],
        "contextBudget": dict(CONTEXT_BUDGET),
    }


def derive_agent_role_plan(spec: dict) -> dict:
    return {
        "requiredAgentRoles": spec["requiredAgentRoles"],
        "optionalAgentRoles": spec["optionalAgentRoles"],
        "roleSpecializations": spec["roleSpecializations"],
        "agentWorkflowOrder": spec["agentWorkflowOrder"],
        "agentRoleOverrides": spec["agentRoleOverrides"],
    }


def make_refinement_module(
    module_id: str,
    title: str,
    priority: str,
    trigger_reason: str,
    questions: list[str],
    recommended_outputs: list[str],
    recommended_prompts: list[str],
    agent_roles: list[str],
    done_when: list[str],
) -> dict:
    return {
        "id": module_id,
        "title": title,
        "priority": priority,
        "triggerReason": trigger_reason,
        "questions": questions,
        "recommendedOutputs": recommended_outputs,
        "recommendedPrompts": recommended_prompts,
        "agentRoles": agent_roles,
        "doneWhen": done_when,
    }


def runtime_refinement_module(spec: dict) -> dict:
    family = spec["projectFamily"]
    baseline = RUNTIME_REFINEMENT_BY_FAMILY[family]
    return make_refinement_module(
        module_id="runtime-shape",
        title=baseline["title"],
        priority="medium",
        trigger_reason=f"projectFamily is `{family}` and runtime details still need repo-local shaping.",
        questions=list(baseline["questions"]),
        recommended_outputs=list(baseline["recommendedOutputs"]),
        recommended_prompts=list(baseline["recommendedPrompts"]),
        agent_roles=list(baseline["agentRoles"]),
        done_when=[
            "runtime-specific structure, commands, and validation boundary are written down",
            "repo-local source of truth files are named in architecture-map and command-catalog",
        ],
    )


def derive_refinement_manifest(spec: dict, scaffold_profile: str | None, support_level: str) -> dict:
    modules: list[dict] = []
    target_environments = spec.get("targetEnvironments", [])
    environment_labels = ", ".join(target_environments) or "local"

    modules.append(
        make_refinement_module(
            module_id="repository-alignment",
            title="Repository Alignment",
            priority="medium",
            trigger_reason="Every generated repository needs repo-local command, document, and pre-commit alignment.",
            questions=[
                "실제 첫 build, compile, test, smoke 명령은 무엇인가?",
                "환경설정과 secret의 source of truth 파일은 어디인가?",
                "생성된 문서 중 repo-local override가 필요한 파일은 무엇인가?",
                "pre-commit hook에 넣을 최소 검증은 무엇인가?",
            ],
            recommended_outputs=[
                "AGENTS.md",
                "docs/ai/command-catalog.md",
                "docs/ai/architecture-map.md",
                ".agent-base/pre-commit-config.json",
            ],
            recommended_prompts=["post-bootstrap-refinement", "build-guide", "test-plan"],
            agent_roles=["runtime-engineer", "qa-validator", "docs-operator"],
            done_when=[
                "first commands and source-of-truth files are documented",
                "pre-commit profile is aligned with the real repository command set",
                "repo-local overrides are named or intentionally deferred",
            ],
        )
    )
    modules.append(runtime_refinement_module(spec))

    if spec.get("exceptions"):
        modules.append(
            make_refinement_module(
                module_id="stack-exceptions",
                title="Non-Default Stack Exceptions",
                priority="medium",
                trigger_reason="The spec already contains exceptions that differ from family defaults.",
                questions=[
                    "예외로 남긴 언어, 프레임워크, 빌드/테스트 도구 차이를 유지할 근거는 무엇인가?",
                    "이 예외를 문서화할 repo-local overlay note는 어디에 남길 것인가?",
                    "기본 preset과 다른 명령 체계가 있다면 pre-commit과 command-catalog를 어떻게 수정할 것인가?",
                ],
                recommended_outputs=[
                    "repo-local overlay note for exceptions",
                    "docs/ai/command-catalog.md",
                    "docs/ai/architecture-map.md",
                ],
                recommended_prompts=["post-bootstrap-refinement", "scaffold-planning"],
                agent_roles=["bootstrap-planner", "runtime-engineer", "docs-operator"],
                done_when=[
                    "every non-default decision has a reason and an owning document",
                    "tooling presets and generated defaults no longer conflict with the chosen stack",
                ],
            )
        )

    if spec.get("datastore") != "없음":
        schema_ownership = spec.get("schemaOwnership", "unspecified")
        data_priority = "high" if schema_ownership in {"owned", "shared"} else "medium"
        modules.append(
            make_refinement_module(
                module_id="data-and-schema",
                title="Data Ownership And Schema Flow",
                priority=data_priority,
                trigger_reason=(
                    f"datastore is `{spec['datastore']}` and schemaOwnership is `{schema_ownership}`."
                ),
                questions=[
                    "schema, migration, seed, verification query 중 이 저장소가 실제로 소유하는 범위는 어디까지인가?",
                    "migration 경로와 naming, rollback, verification 기준을 어디에 남길 것인가?",
                    "seed, backfill, data correction이 생길 수 있다면 어떤 문서와 체크리스트를 기본으로 둘 것인가?",
                ],
                recommended_outputs=[
                    "docs/ai/database-rules.md",
                    "checklists/database-change.md",
                    "impact-analysis or database review note",
                ],
                recommended_prompts=["post-bootstrap-refinement", "impact-analysis"],
                agent_roles=["data-steward", "runtime-engineer", "qa-validator", "docs-operator"],
                done_when=[
                    "schema ownership and migration path are explicit",
                    "verification and rollback expectations are documented before the first DB-affecting change",
                ],
            )
        )

    if spec.get("cache") != "없음":
        modules.append(
            make_refinement_module(
                module_id="cache-policy",
                title="Cache And State Policy",
                priority="medium",
                trigger_reason=f"cache is `{spec['cache']}`.",
                questions=[
                    "cache key, TTL, invalidation 책임을 어느 계층에 둘지 정했는가?",
                    "cache miss/fallback과 local 개발 모드 동작을 어떻게 검증할 것인가?",
                    "cache 관련 설정과 운영 점검 포인트를 어디에 기록할 것인가?",
                ],
                recommended_outputs=[
                    "docs/ai/architecture-map.md",
                    "docs/ai/command-catalog.md",
                    "operations-manual or runbook note",
                ],
                recommended_prompts=["post-bootstrap-refinement", "operations-manual"],
                agent_roles=["runtime-engineer", "qa-validator", "docs-operator"],
                done_when=[
                    "cache behavior and ownership are visible in the repo-local docs",
                    "operators know where to check cache-related failures or toggles",
                ],
            )
        )

    if spec.get("externalIntegrations"):
        modules.append(
            make_refinement_module(
                module_id="integration-contracts",
                title="External Integration Contracts",
                priority="medium",
                trigger_reason=(
                    "externalIntegrations are declared in the spec: "
                    + ", ".join(spec["externalIntegrations"])
                    + "."
                ),
                questions=[
                    "각 외부 연동의 contract owner, timeout/retry, failure path를 어디에 기록할 것인가?",
                    "로컬 또는 test 환경에서 stub, mock, sandbox 중 무엇을 사용할 것인가?",
                    "smoke 검증에서 꼭 확인할 대표 연동 경로는 무엇인가?",
                ],
                recommended_outputs=[
                    "docs/ai/architecture-map.md",
                    "docs/ai/command-catalog.md",
                    "operations-manual or impact-analysis",
                ],
                recommended_prompts=["post-bootstrap-refinement", "impact-analysis", "operations-manual"],
                agent_roles=["runtime-engineer", "qa-validator", "docs-operator"],
                done_when=[
                    "integration boundaries and fallback expectations are documented",
                    "one representative validation path exists for critical integrations",
                ],
            )
        )

    security_needed = spec.get("securityProfile") != "없음" or spec.get("deploymentType") != "local-only" or len(target_environments) > 1
    if security_needed:
        security_priority = "high" if spec.get("securityProfile") != "없음" or spec.get("projectNature") == "production" else "medium"
        modules.append(
            make_refinement_module(
                module_id="security-and-environments",
                title="Security And Environment Policy",
                priority=security_priority,
                trigger_reason=(
                    f"securityProfile is `{spec['securityProfile']}` and target environments are `{environment_labels}`."
                ),
                questions=[
                    "secret, token, env override는 어디서 주입되고 어떤 파일이 source of truth인가?",
                    "인증/인가 경계와 민감 로그 금지 기준을 어디에 문서화할 것인가?",
                    "환경별 차이를 default, override, or defer 중 어떻게 처리할 것인가?",
                ],
                recommended_outputs=[
                    "docs/ai/architecture-map.md",
                    "docs/ai/command-catalog.md",
                    "repo-local env or security note",
                ],
                recommended_prompts=["post-bootstrap-refinement", "build-guide"],
                agent_roles=["security-reviewer", "runtime-engineer", "docs-operator"],
                done_when=[
                    "secret injection path and security boundaries are named",
                    "environment differences are documented or explicitly deferred with notes",
                ],
            )
        )

    delivery_needed = spec.get("deploymentType") != "local-only" or spec.get("projectNature") == "production" or any(env in {"stg", "prd"} for env in target_environments)
    if delivery_needed:
        delivery_priority = "high" if spec.get("projectNature") == "production" or spec.get("deploymentType") != "local-only" else "medium"
        modules.append(
            make_refinement_module(
                module_id="delivery-and-rollout",
                title="Delivery And Rollout",
                priority=delivery_priority,
                trigger_reason=(
                    f"deploymentType is `{spec['deploymentType']}` and target environments are `{environment_labels}`."
                ),
                questions=[
                    "배포 단위, 배포 순서, smoke owner를 어디까지 첫 문서에 넣을 것인가?",
                    "rollback trigger와 운영 점검 포인트를 무엇으로 둘 것인가?",
                    "deploy-check에서 반드시 확인할 env, secret, dependency 항목은 무엇인가?",
                ],
                recommended_outputs=[
                    "deployment-checklist",
                    "operations-manual",
                    "release and rollback note",
                ],
                recommended_prompts=["post-bootstrap-refinement", "deployment-checklist", "operations-manual"],
                agent_roles=["release-manager", "qa-validator", "docs-operator"],
                done_when=[
                    "deployment order and rollback trigger are explicit",
                    "deploy-check and smoke responsibilities are visible before first delivery",
                ],
            )
        )

    if spec.get("repositoryMode") != "single-repo":
        modules.append(
            make_refinement_module(
                module_id="repository-topology",
                title="Repository Topology Expansion",
                priority="high",
                trigger_reason=(
                    f"repositoryMode is `{spec['repositoryMode']}` but generator v1 creates only one sample repository."
                ),
                questions=[
                    "workspace, package boundary, shared config를 어떤 구조로 확장할 것인가?",
                    "root command와 package-local command를 어디에 나눠 기록할 것인가?",
                    "multi-repo 또는 monorepo handoff 기준과 문서 경계를 어떻게 둘 것인가?",
                ],
                recommended_outputs=[
                    "topology note or repo-local overlay plan",
                    "docs/ai/architecture-map.md",
                    "docs/ai/command-catalog.md",
                ],
                recommended_prompts=["post-bootstrap-refinement", "scaffold-planning"],
                agent_roles=["bootstrap-planner", "solution-architect", "docs-operator"],
                done_when=[
                    "the expansion path beyond the single generated sample repo is explicit",
                    "command ownership and document boundaries are clear for each repo or package",
                ],
            )
        )

    if support_level != "supported":
        scaffold_priority = "high" if support_level == "docs-only" else "medium"
        modules.append(
            make_refinement_module(
                module_id="scaffold-gap",
                title="Scaffold Completion Plan",
                priority=scaffold_priority,
                trigger_reason=(
                    f"scaffold support level is `{support_level}` with profile `{scaffold_profile or 'docs-only'}`."
                ),
                questions=[
                    "생성기가 채우지 못한 최소 실행 구조는 무엇인가?",
                    "repo-local scaffold를 어떤 파일과 디렉토리부터 직접 보완할 것인가?",
                    "지원되지 않는 영역을 TODO, overlay note, or custom script 중 어디에 남길 것인가?",
                ],
                recommended_outputs=[
                    "TODO_UNSUPPORTED_SCAFFOLD.md or repo-local scaffold plan",
                    "build-guide",
                    "test-plan",
                ],
                recommended_prompts=["post-bootstrap-refinement", "scaffold-planning", "project-generator-run"],
                agent_roles=["bootstrap-planner", "runtime-engineer", "docs-operator"],
                done_when=[
                    "manual scaffold completion scope is visible",
                    "the first executable or verifiable path is defined even when generation is partial",
                ],
            )
        )

    priority_order = {"high": 0, "medium": 1, "low": 2}
    suggested_execution_order = [
        module["id"]
        for module in sorted(modules, key=lambda module: priority_order.get(module["priority"], 9))
    ]
    high_priority_modules = [module["id"] for module in modules if module["priority"] == "high"]

    return {
        "version": 1,
        "projectFamily": spec["projectFamily"],
        "repositoryName": spec["repositoryName"],
        "scaffoldProfile": scaffold_profile,
        "supportLevel": support_level,
        "summary": {
            "needsRefinement": bool(modules),
            "moduleCount": len(modules),
            "highPriorityModuleIds": high_priority_modules,
            "suggestedExecutionOrder": suggested_execution_order,
            "decisionModes": ["decide-now", "keep-default", "defer-with-note"],
        },
        "modules": modules,
    }


def derive_refinement_status(spec: dict, refinement_manifest: dict) -> dict:
    module_entries = []
    for module in refinement_manifest["modules"]:
        module_entries.append(
            {
                "id": module["id"],
                "title": module["title"],
                "priority": module["priority"],
                "status": "pending",
                "decisionMode": "undecided",
                "ownerHints": list(module["agentRoles"]),
                "recommendedOutputs": list(module["recommendedOutputs"]),
                "recommendedPrompts": list(module["recommendedPrompts"]),
                "notes": "",
                "deferredReason": "",
                "resolver": "",
                "lastUpdated": None,
            }
        )

    return {
        "version": 1,
        "repositoryName": spec["repositoryName"],
        "projectFamily": spec["projectFamily"],
        "summary": {
            "pendingModuleIds": [module["id"] for module in refinement_manifest["modules"]],
            "highPriorityPendingModuleIds": list(refinement_manifest["summary"]["highPriorityModuleIds"]),
            "resolvedModuleIds": [],
            "deferredModuleIds": [],
            "nextRecommendedPrompt": "post-bootstrap-refinement",
            "decisionModes": ["decide-now", "keep-default", "defer-with-note"],
        },
        "modules": module_entries,
    }


def runtime_engineer_label(spec: dict) -> str:
    specializations = []
    for item in spec.get("roleSpecializations", []):
        if item.startswith("runtime-engineer:"):
            specializations.append(item.split(":", 1)[1].strip())
    if not specializations:
        return "runtime-engineer"
    return f"runtime-engineer[{', '.join(specializations)}]"


def default_runtime_owned_paths(spec: dict) -> list[str]:
    family = spec["projectFamily"]
    language = str(spec.get("language", "")).lower()
    framework = str(spec.get("framework", "")).lower()

    if family in {"web-app", "pwa", "mockup-local"}:
        return ["src/", "public/", "package.json", "docs/ai/architecture-map.md"]
    if family == "mobile-app":
        return ["lib/", "test/", "pubspec.yaml", "docs/ai/architecture-map.md"]
    if family == "game":
        return ["Assets/", "Packages/", "ProjectSettings/", "docs/ai/architecture-map.md"]
    if family in {"backend-service", "batch-worker", "receiver-integration"}:
        return ["src/main/", "src/test/", "build.gradle", "docs/ai/architecture-map.md"]
    if family == "library-tooling" and language == "java":
        return ["src/main/", "src/test/", "build.gradle", "docs/ai/architecture-map.md"]
    if family == "library-tooling" and language == "typescript":
        return ["src/", "test/", "package.json", "docs/ai/architecture-map.md"]
    if "spring" in framework:
        return ["src/main/", "src/test/", "build.gradle", "docs/ai/architecture-map.md"]
    return ["src/", "tests/", "docs/ai/architecture-map.md"]


def make_work_lane(
    lane_id: str,
    title: str,
    phase: str,
    role: str,
    status: str,
    objective: str,
    scope_summary: str,
    depends_on: list[str],
    owned_paths: list[str],
    required_inputs: list[str],
    expected_outputs: list[str],
    handoff_targets: list[str],
    done_when: list[str],
    notes: str = "",
    blockers: list[str] | None = None,
    verification_status: str = "not-started",
) -> dict:
    return {
        "id": lane_id,
        "title": title,
        "phase": phase,
        "role": role,
        "currentOwner": role,
        "status": status,
        "objective": objective,
        "scopeSummary": scope_summary,
        "dependsOn": depends_on,
        "ownedPaths": owned_paths,
        "requiredInputs": required_inputs,
        "expectedOutputs": expected_outputs,
        "handoffTargets": handoff_targets,
        "doneWhen": done_when,
        "latestSummary": "",
        "notes": notes,
        "verificationStatus": verification_status,
        "nextHandoffTarget": handoff_targets[0] if handoff_targets else "",
        "latestPacketPath": "",
        "blockers": list(blockers or []),
        "openQuestions": [],
        "lastUpdated": None,
    }


def recompute_agent_workboard_summary(workboard: dict) -> None:
    pending = [lane["id"] for lane in workboard["workLanes"] if lane["status"] == "pending"]
    in_progress = [lane["id"] for lane in workboard["workLanes"] if lane["status"] == "in-progress"]
    blocked = [lane["id"] for lane in workboard["workLanes"] if lane["status"] == "blocked"]
    completed = [lane["id"] for lane in workboard["workLanes"] if lane["status"] == "completed"]

    workboard["summary"]["pendingLaneIds"] = pending
    workboard["summary"]["inProgressLaneIds"] = in_progress
    workboard["summary"]["blockedLaneIds"] = blocked
    workboard["summary"]["completedLaneIds"] = completed

    completed_set = set(completed)
    next_lane = None
    for lane in workboard["workLanes"]:
        if lane["status"] != "pending":
            continue
        if all(dep in completed_set for dep in lane["dependsOn"]):
            next_lane = lane["id"]
            break
    workboard["summary"]["nextSuggestedLaneId"] = next_lane


def sync_agent_workboard_with_refinement(workboard: dict, refinement_status: dict) -> None:
    high_priority_pending = list(refinement_status["summary"]["highPriorityPendingModuleIds"])
    workboard["summary"]["blockingHighPriorityModuleIds"] = high_priority_pending
    workboard["summary"]["designReady"] = not high_priority_pending

    design_lane = next((lane for lane in workboard["workLanes"] if lane["id"] == "design-freeze"), None)
    if design_lane:
        design_lane["blockers"] = list(high_priority_pending)
        if high_priority_pending:
            design_lane["status"] = "blocked"
        elif design_lane["status"] == "blocked":
            design_lane["status"] = "pending"

    recompute_agent_workboard_summary(workboard)


def derive_agent_workboard(
    spec: dict,
    context_manifest: dict,
    refinement_manifest: dict,
    refinement_status: dict,
    path_map: dict[str, str],
) -> dict:
    high_priority_pending = list(refinement_status["summary"]["highPriorityPendingModuleIds"])
    design_ready = not high_priority_pending
    role_plan = derive_agent_role_plan(spec)
    active_roles = list(role_plan["requiredAgentRoles"])
    runtime_role = runtime_engineer_label(spec)
    refinement_modules = {module["id"] for module in refinement_manifest["modules"]}
    work_lanes = []

    work_lanes.append(
        make_work_lane(
            lane_id="design-freeze",
            title="Design Freeze And Task Framing",
            phase="planning",
            role="orchestrator" if "orchestrator" in active_roles else "bootstrap-planner",
            status="pending",
            objective="상위 설계와 refinement 결정을 실행 가능한 작업 범위와 handoff 기준으로 고정한다.",
            scope_summary="high-priority refinement, 역할별 owned path, 검증 경계, 다음 handoff 순서를 합의한다.",
            depends_on=[],
            owned_paths=[
                path_map["rolePlanPath"],
                path_map["refinementStatusPath"],
                path_map["repoLocalOverridesPath"],
                path_map["workboardPath"],
            ],
            required_inputs=[
                path_map["specPath"],
                path_map["refinementManifestPath"],
                path_map["refinementStatusPath"],
                path_map["commandCatalogPath"],
                path_map["architectureMapPath"],
            ],
            expected_outputs=[
                path_map["workboardPath"],
                path_map["handoffLogPath"],
                path_map["repoLocalOverridesPath"],
            ],
            handoff_targets=[
                runtime_role,
                "qa-validator" if "qa-validator" in active_roles else "docs-operator",
                "docs-operator" if "docs-operator" in active_roles else runtime_role,
            ],
            done_when=[
                "high-priority refinement module이 resolved 또는 deferred with owner 상태다",
                "각 실행 lane의 owned path와 next handoff target이 정리되었다",
                "첫 execution lane으로 넘길 deterministic handoff packet이 준비되었다",
                "작업을 막는 open question과 blocker가 workboard에 남아 있다",
            ],
            blockers=high_priority_pending,
            notes="설계가 끝난 뒤 runner에게 넘길 실행 기준선을 여기서 고정한다.",
        )
    )

    work_lanes.append(
        make_work_lane(
            lane_id="runtime-implementation",
            title="Runtime Implementation",
            phase="implementation",
            role=runtime_role,
            status="pending",
            objective="합의된 설계 기준 안에서 실제 코드와 설정을 구현한다.",
            scope_summary="코드 변경은 agreed scope 안에서 진행하고, 새로운 설계 판단이 생기면 먼저 design-freeze lane으로 되돌린다.",
            depends_on=["design-freeze"],
            owned_paths=default_runtime_owned_paths(spec),
            required_inputs=[
                path_map["specPath"],
                path_map["refinementStatusPath"],
                path_map["commandCatalogPath"],
                path_map["architectureMapPath"],
                path_map["repoLocalOverridesPath"],
            ],
            expected_outputs=[
                "code and config changes within owned paths",
                path_map["commandCatalogPath"],
                path_map["architectureMapPath"],
            ],
            handoff_targets=[
                "qa-validator" if "qa-validator" in active_roles else "docs-operator",
                "docs-operator" if "docs-operator" in active_roles else runtime_role,
            ],
            done_when=[
                "변경 범위가 owned path 안에서 설명 가능하다",
                "first build/test/smoke에 필요한 명령과 전제조건이 문서에 반영되었다",
                "미해결 위험이 handoff log와 workboard에 기록되었다",
            ],
        )
    )

    if "data-steward" in active_roles or "data-and-schema" in refinement_modules:
        work_lanes.append(
            make_work_lane(
                lane_id="data-contracts",
                title="Data Ownership And Verification",
                phase="implementation",
                role="data-steward" if "data-steward" in active_roles else runtime_role,
                status="pending",
                objective="schema, migration, verification query, rollback 기준을 구현 범위와 분리해 고정한다.",
                scope_summary="DB ownership이 있는 경우 코드보다 먼저 verification/rollback 기준을 분명히 한다.",
                depends_on=["design-freeze"],
                owned_paths=["docs/ai/database-rules.md", "checklists/database-change.md", "src/main/resources/"],
                required_inputs=[
                    path_map["refinementStatusPath"],
                    path_map["architectureMapPath"],
                    path_map["commandCatalogPath"],
                ],
                expected_outputs=[
                    "schema ownership note",
                    "migration and verification plan",
                    "rollback or data safety note",
                ],
                handoff_targets=[runtime_role, "qa-validator", "docs-operator"],
                done_when=[
                    "schema ownership과 migration 경로가 문서에 적혔다",
                    "verification query 또는 동등한 검증 기준이 준비되었다",
                    "DB 영향이 있는 handoff에서 놓친 사항이 없다",
                ],
            )
        )

    if "security-reviewer" in active_roles or "security-and-environments" in refinement_modules:
        work_lanes.append(
            make_work_lane(
                lane_id="security-review",
                title="Security And Environment Review",
                phase="governance",
                role="security-reviewer" if "security-reviewer" in active_roles else runtime_role,
                status="pending",
                objective="auth, secret, env override, 민감 로그 기준을 구현 전후로 점검한다.",
                scope_summary="보안 경계와 env source of truth를 확정하고 runtime lane과 validator lane에 공유한다.",
                depends_on=["design-freeze"],
                owned_paths=["docs/ai/architecture-map.md", "docs/ai/command-catalog.md", "docs/ai/repo-local-overrides.md"],
                required_inputs=[
                    path_map["refinementStatusPath"],
                    path_map["repoLocalOverridesPath"],
                    path_map["architectureMapPath"],
                ],
                expected_outputs=[
                    "security decision notes",
                    "env/source-of-truth update",
                    "blocked actions or safe defaults",
                ],
                handoff_targets=[runtime_role, "qa-validator", "docs-operator"],
                done_when=[
                    "secret/env injection source of truth가 명확하다",
                    "민감 로그와 권한 경계가 문서화되었다",
                    "보안 리뷰가 필요한 변경이 validator에게 공유되었다",
                ],
            )
        )

    if "qa-validator" in active_roles:
        validation_depends = ["runtime-implementation"]
        if any(lane["id"] == "data-contracts" for lane in work_lanes):
            validation_depends.append("data-contracts")
        if any(lane["id"] == "security-review" for lane in work_lanes):
            validation_depends.append("security-review")
        work_lanes.append(
            make_work_lane(
                lane_id="qa-validation",
                title="Validation And Smoke Review",
                phase="validation",
                role="qa-validator",
                status="pending",
                objective="실제 build/test/smoke 결과와 미검증 항목을 고정한다.",
                scope_summary="runtime 변경과 side review 결과를 받아 검증 경계와 미실행 항목을 정리한다.",
                depends_on=validation_depends,
                owned_paths=["docs/ai/command-catalog.md", "checklists/first-delivery.md", path_map["handoffLogPath"]],
                required_inputs=[
                    path_map["commandCatalogPath"],
                    path_map["workboardPath"],
                    path_map["handoffLogPath"],
                ],
                expected_outputs=[
                    "validation result summary",
                    "smoke notes",
                    "unverified items with reason",
                ],
                handoff_targets=["docs-operator", "release-manager" if "release-manager" in role_plan["optionalAgentRoles"] else "orchestrator"],
                done_when=[
                    "최소 1개 이상의 자동 검증 또는 동등 검증이 기록되었다",
                    "미실행 검증과 이유가 handoff에 남아 있다",
                    "final delivery가 설명 가능한 수준으로 정리되었다",
                ],
            )
        )

    if "docs-operator" in active_roles:
        docs_depends = ["runtime-implementation"]
        if "qa-validator" in active_roles:
            docs_depends.append("qa-validation")
        work_lanes.append(
            make_work_lane(
                lane_id="docs-alignment",
                title="Docs And Operator Alignment",
                phase="delivery",
                role="docs-operator",
                status="pending",
                objective="명령, 운영, handoff, 예외 정보를 사람이 바로 사용할 수 있게 정리한다.",
                scope_summary="repo-local overrides, command catalog, architecture map, handoff log를 최신 상태로 맞춘다.",
                depends_on=docs_depends,
                owned_paths=[
                    path_map["repoLocalOverridesPath"],
                    path_map["commandCatalogPath"],
                    path_map["architectureMapPath"],
                    path_map["handoffLogPath"],
                ],
                required_inputs=[
                    path_map["workboardPath"],
                    path_map["handoffLogPath"],
                    path_map["refinementStatusPath"],
                ],
                expected_outputs=[
                    path_map["repoLocalOverridesPath"],
                    path_map["commandCatalogPath"],
                    path_map["architectureMapPath"],
                    path_map["handoffLogPath"],
                ],
                handoff_targets=["orchestrator"],
                done_when=[
                    "실행 중 바뀐 기준이 docs에 반영되었다",
                    "handoff log만 봐도 누가 무엇을 넘겼는지 추적 가능하다",
                    "첫 전달 시 필요한 문서와 체크리스트가 최신 상태다",
                ],
            )
        )

    if spec.get("deploymentType") != "local-only" or "delivery-and-rollout" in refinement_modules:
        release_role = "release-manager" if "release-manager" in role_plan["optionalAgentRoles"] else "orchestrator"
        release_depends = ["docs-alignment"] if any(lane["id"] == "docs-alignment" for lane in work_lanes) else ["runtime-implementation"]
        if any(lane["id"] == "qa-validation" for lane in work_lanes):
            release_depends.append("qa-validation")
        work_lanes.append(
            make_work_lane(
                lane_id="release-readiness",
                title="Release And Rollout Readiness",
                phase="delivery",
                role=release_role,
                status="pending",
                objective="배포/롤아웃/rollback 기준이 필요한 저장소라면 첫 실행 기준선을 고정한다.",
                scope_summary="운영 영향이 있는 저장소에서 deploy-check와 rollback note가 없이 종료되지 않게 한다.",
                depends_on=release_depends,
                owned_paths=["deployment-checklist", "operations-manual", "docs/ai/repo-local-overrides.md"],
                required_inputs=[
                    path_map["handoffLogPath"],
                    path_map["refinementStatusPath"],
                    path_map["commandCatalogPath"],
                ],
                expected_outputs=[
                    "deployment checklist or equivalent note",
                    "rollback trigger memo",
                    "release blocker summary",
                ],
                handoff_targets=["orchestrator"],
                done_when=[
                    "배포 영향과 rollback 기준이 문서화되었다",
                    "release blocker가 있으면 명시적으로 defer 또는 block 처리되었다",
                    "운영 변경이 validator/docs output과 모순되지 않는다",
                ],
            )
        )

    workboard = {
        "version": 1,
        "repositoryName": spec["repositoryName"],
        "projectFamily": spec["projectFamily"],
        "summary": {
            "designReady": design_ready,
            "blockingHighPriorityModuleIds": high_priority_pending,
            "pendingLaneIds": [],
            "inProgressLaneIds": [],
            "blockedLaneIds": [],
            "completedLaneIds": [],
            "nextSuggestedLaneId": None,
        },
        "sharedContext": {
            **path_map,
            "fastPathDocs": list(context_manifest["fastPathDocs"]),
            "coreRoles": list(context_manifest["coreRoles"]),
            "extendedRoles": list(context_manifest["extendedRoles"]),
        },
        "coordinationRules": [
            "high-priority refinement module이 unresolved 상태면 implementation 범위를 넓히지 않는다.",
            "각 lane은 owned path를 먼저 선언하고, 다른 lane의 write scope를 덮어쓰지 않는다.",
            "새 설계 판단이 필요해지면 runtime lane이 혼자 결정하지 말고 design-freeze lane으로 되돌린다.",
            "handoff 때는 files, outputs, verification, open question을 docs/ai/agent-handoff-log.md에 남긴다.",
            "planning에서 execution으로 넘어갈 때는 docs/ai/handoff-packets/ 아래 current packet으로 실행 기준을 고정한다.",
            "qa-validator와 docs-operator 없이 작업을 최종 완료로 선언하지 않는다.",
        ],
        "workLanes": work_lanes,
    }
    sync_agent_workboard_with_refinement(workboard, refinement_status)
    return workboard


def normalize_spec(spec: dict) -> dict:
    normalized = dict(spec)
    derived = derive_agent_coordination(normalized)
    for key, value in derived.items():
        if key not in normalized or not normalized.get(key):
            normalized[key] = value
    return normalized


def choose_scaffold(spec: dict) -> tuple[str | None, str]:
    family = spec["projectFamily"]
    language = str(spec["language"]).lower()
    framework = str(spec["framework"]).lower()

    if family == "web-app" and language == "typescript" and "react" in framework:
        return "web-react-vite", "supported"
    if family == "pwa" and language == "typescript" and "react" in framework:
        return "pwa-react-vite", "supported"
    if family == "mockup-local":
        return "mockup-local-static", "supported"
    if family == "backend-service" and language == "java" and "spring" in framework:
        return "java-spring-service", "supported"
    if family == "batch-worker" and language == "java" and "spring" in framework:
        return "java-spring-batch", "supported"
    if family == "receiver-integration" and language == "java" and "spring" in framework:
        return "java-spring-receiver", "supported"
    if family == "game" and language in {"c#", "csharp"} and "unity" in framework:
        return "unity-game", "structure-only"
    if family == "mobile-app" and language == "dart" and "flutter" in framework:
        return "flutter-mobile", "structure-only"
    if family == "library-tooling" and language == "typescript":
        return "typescript-library-tooling", "supported"
    if family == "library-tooling" and language == "java":
        return "java-library-tooling", "supported"
    return None, "docs-only"


def derive_main_class_name(spec: dict) -> str:
    base = slug_to_pascal(spec.get("projectName") or spec["repositoryName"])
    family = spec["projectFamily"]
    if family == "batch-worker":
        return f"{base}BatchApplication"
    if family == "receiver-integration":
        return f"{base}ReceiverApplication"
    if family == "library-tooling":
        return f"{base}ToolingApplication"
    return f"{base}Application"


def build_token_map(spec: dict) -> dict[str, str]:
    package_name = spec.get("packageName", "")
    package_path = package_name.replace(".", "/")
    target_envs = ", ".join(spec.get("targetEnvironments", []))
    target_os = ", ".join(spec.get("targetOs", []))
    runtime_roles = ", ".join(spec.get("runtimeRoles", []))
    external_integrations = ", ".join(spec.get("externalIntegrations", []))

    return {
        "__REPOSITORY_NAME__": spec["repositoryName"],
        "__PROJECT_NAME__": spec["projectName"],
        "__PROJECT_FAMILY__": spec["projectFamily"],
        "__PROJECT_PURPOSE__": spec["projectPurpose"],
        "__PROJECT_NATURE__": spec["projectNature"],
        "__REPOSITORY_MODE__": spec["repositoryMode"],
        "__LANGUAGE__": spec["language"],
        "__FRAMEWORK__": spec["framework"],
        "__RUNTIME_VERSION__": str(spec["runtimeVersion"]),
        "__BUILD_TOOL__": spec["buildTool"],
        "__TEST_TOOL__": spec["testTool"],
        "__DATASTORE__": spec["datastore"],
        "__CACHE__": spec["cache"],
        "__DEPLOYMENT_TYPE__": spec["deploymentType"],
        "__STARTUP_MODE__": spec["startupMode"],
        "__LOGGING_MODE__": spec["loggingMode"],
        "__SECURITY_PROFILE__": spec["securityProfile"],
        "__PACKAGE_NAME__": package_name,
        "__PACKAGE_PATH__": package_path,
        "__MAIN_CLASS_NAME__": derive_main_class_name(spec),
        "__TARGET_ENVIRONMENTS__": target_envs,
        "__TARGET_OS__": target_os,
        "__RUNTIME_ROLES__": runtime_roles,
        "__EXTERNAL_INTEGRATIONS__": external_integrations,
    }


def build_precommit_config(spec: dict) -> dict:
    config = dict(DEFAULT_PRECOMMIT_CONFIG)
    family = spec["projectFamily"]
    language = str(spec.get("language", "")).lower()
    framework = str(spec.get("framework", "")).lower()

    if family == "web-app":
        config["presetProfile"] = "web-app"
    elif family == "pwa":
        config["presetProfile"] = "pwa"
    elif family == "backend-service":
        config["presetProfile"] = "backend-service"
        config["runLintOnHook"] = False
        config["runTypecheckOnHook"] = False
    elif family == "batch-worker":
        config["presetProfile"] = "batch-worker"
        config["runLintOnHook"] = False
        config["runTypecheckOnHook"] = False
    elif family == "receiver-integration":
        config["presetProfile"] = "receiver-integration"
        config["runLintOnHook"] = False
        config["runTypecheckOnHook"] = False
    elif family == "mockup-local":
        config["presetProfile"] = "mockup-local"
    elif family == "game":
        config["presetProfile"] = "unity-game" if "unity" in framework or language in {"c#", "csharp"} else "game"
        config["runLintOnHook"] = False
        config["runTypecheckOnHook"] = False
    elif family == "mobile-app":
        config["presetProfile"] = "mobile-flutter" if "flutter" in framework or language == "dart" else "mobile-app"
    elif family == "library-tooling":
        if language == "java":
            config["presetProfile"] = "library-tooling-java"
            config["runLintOnHook"] = False
            config["runTypecheckOnHook"] = False
        else:
            config["presetProfile"] = "library-tooling-typescript"
    return config


def safe_rmtree(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)


def copy_tree(src: Path, dest: Path) -> None:
    for item in src.iterdir():
        target = dest / item.name
        if item.is_dir():
            shutil.copytree(item, target, dirs_exist_ok=True)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, target)


def apply_tokens(root: Path, tokens: dict[str, str]) -> None:
    paths = sorted(root.rglob("*"), key=lambda p: len(p.parts), reverse=True)
    for path in paths:
        if path.name in {".git", "__pycache__"}:
            continue
        new_name = path.name
        for token, value in tokens.items():
            new_name = new_name.replace(token, value)
        if new_name != path.name:
            target_path = path.parent / new_name
            target_path.parent.mkdir(parents=True, exist_ok=True)
            path.rename(target_path)

    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES and path.name not in {".gitignore"}:
            continue
        text = path.read_text(encoding="utf-8")
        new_text = text
        for token, value in tokens.items():
            new_text = new_text.replace(token, value)
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")


def write_root_readme(target_dir: Path, spec: dict, scaffold_profile: str | None, support_level: str) -> None:
    coordination_mode = derive_coordination_mode(spec)
    starter_command = "python3 scripts/show_start_path.py"
    if coordination_mode["mode"] == "lite":
        next_steps = [
            "Review `AGENTS.md`, `.agent-base/context-manifest.json`, and `docs/ai/command-catalog.md` only.",
            "Review `.agent-base/refinement-manifest.json` and handle only the high-priority blockers for the first runnable path.",
            "Align `docs/ai/command-catalog.md` and `.agent-base/pre-commit-config.json` with the real repository commands.",
            "Run the first build, test, or smoke validation and record any gap in `docs/ai/repo-local-overrides.md`.",
            "Open `.agent-base/agent-workboard.json` only if more than one owner or DB/security/release risk appears.",
        ]
    elif coordination_mode["mode"] == "coordinated":
        next_steps = [
            "Review `AGENTS.md`, `.agent-base/context-manifest.json`, and `.agent-base/refinement-manifest.json` first.",
            "Update high-priority refinement decisions and record exceptions in `docs/ai/repo-local-overrides.md`.",
            "Review `.agent-base/agent-workboard.json`; once blockers clear, run `python3 scripts/update_agent_workboard.py --finalize-design-freeze`.",
            "Use handoff packets and baton history only at major role or scope transitions.",
            "Align command/pre-commit settings and run the first build, test, or smoke validation.",
        ]
    else:
        next_steps = [
            "Review `AGENTS.md`, `.agent-base/context-manifest.json`, `.agent-base/agent-role-plan.json`, and `.agent-base/agent-workboard.json` together.",
            "Resolve the high-priority refinement modules before widening implementation scope.",
            "Run `python3 scripts/update_agent_workboard.py --finalize-design-freeze` and keep packet freshness checks in the shared delivery path.",
            "Keep role owners, side lanes, and baton history current while implementation is in progress.",
            "Align command/pre-commit settings, prepare release or runbook notes, and run the first build, test, and smoke validation.",
        ]
    next_steps_lines = "\n".join(f"{index}. {step}" for index, step in enumerate(next_steps, start=1))
    coordination_reason_lines = "\n".join(f"- {reason}" for reason in coordination_mode["reasons"])
    readme = f"""# {spec['projectName']}

{spec['projectPurpose']}

## Bootstrap Summary

- Repository: `{spec['repositoryName']}`
- Project family: `{spec['projectFamily']}`
- Project nature: `{spec['projectNature']}`
- Repository mode: `{spec['repositoryMode']}`
- Runtime roles: `{', '.join(spec['runtimeRoles'])}`
- Language / framework: `{spec['language']} / {spec['framework']}`
- Build tool: `{spec['buildTool']}`
- Test tool: `{spec['testTool']}`
- Deployment type: `{spec['deploymentType']}`
- Startup mode: `{spec['startupMode']}`
- Logging mode: `{spec['loggingMode']}`
- Target environments: `{', '.join(spec['targetEnvironments'])}`
- Required agent roles: `{', '.join(spec['requiredAgentRoles'])}`
- Optional agent roles: `{', '.join(spec['optionalAgentRoles'])}`
- Scaffold profile: `{scaffold_profile or 'docs-only'}`
- Scaffold support level: `{support_level}`

## Recommended Coordination Mode

- Mode: `{coordination_mode['label']}`
- Summary: {coordination_mode['summary']}

Why this mode:
{coordination_reason_lines}

## Quick Start

```bash
{starter_command}
```

이 명령은 현재 저장소의 추천 mode, blocking refinement, workboard 상태를 읽고 지금 바로 할 3가지 액션만 보여준다.

## Mode Baseline

{next_steps_lines}
"""
    (target_dir / "README.md").write_text(readme, encoding="utf-8")


def write_repo_local_overrides(target_dir: Path, spec: dict, refinement_manifest: dict) -> None:
    exceptions = spec.get("exceptions", [])
    high_priority_modules = refinement_manifest["summary"]["highPriorityModuleIds"]
    lines = [
        "# Repo-Local Overrides",
        "",
        "이 문서는 공통 템플릿 기본값과 다른 선택, bootstrap 이후 refinement 결정, defer note를 저장소 로컬 기준으로 남긴다.",
        "",
        "## Bootstrap Snapshot",
        "",
        f"- Repository: `{spec['repositoryName']}`",
        f"- Project family: `{spec['projectFamily']}`",
        f"- Runtime roles: `{', '.join(spec['runtimeRoles'])}`",
        f"- Language / framework: `{spec['language']} / {spec['framework']}`",
        f"- Build tool: `{spec['buildTool']}`",
        f"- Test tool: `{spec['testTool']}`",
        f"- Deployment type: `{spec['deploymentType']}`",
        f"- Security profile: `{spec['securityProfile']}`",
        "",
        "## Decision Modes",
        "",
        "- `decide-now`: 지금 확정하고 관련 문서/설정까지 같이 반영한다.",
        "- `keep-default`: 공통 기본값을 의도적으로 유지한다.",
        "- `defer-with-note`: 지금은 미루되 이유와 나중에 결정할 주체를 남긴다.",
        "",
        "## Non-Default Choices",
        "",
    ]
    if exceptions:
        for exception in exceptions:
            lines.append(f"- {exception}")
    else:
        lines.append("- 없음")

    lines.extend(
        [
            "",
            "## High-Priority Refinement Modules",
            "",
        ]
    )
    if high_priority_modules:
        for module_id in high_priority_modules:
            lines.append(f"- `{module_id}`")
    else:
        lines.append("- 없음")

    for module in refinement_manifest["modules"]:
        lines.extend(
            [
                "",
                f"## {module['title']} `{module['id']}`",
                "",
                f"- Priority: `{module['priority']}`",
                f"- Trigger: {module['triggerReason']}",
                f"- Suggested owners: {', '.join(module['agentRoles'])}",
                "- Current decision: `pending`",
                "- Resolution mode: `undecided`",
                "- Deferred owner or next resolver: ",
                "",
                "Questions to answer:",
            ]
        )
        for question in module["questions"]:
            lines.append(f"- [ ] {question}")
        lines.extend(
            [
                "",
                "Recommended outputs:",
            ]
        )
        for output in module["recommendedOutputs"]:
            lines.append(f"- {output}")
        lines.extend(
            [
                "",
                "Recommended prompts:",
            ]
        )
        for prompt in module["recommendedPrompts"]:
            lines.append(f"- {prompt}")
        lines.extend(
            [
                "",
                "Notes:",
                "- ",
                "",
            ]
        )

    target_path = target_dir / "docs" / "ai" / "repo-local-overrides.md"
    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_agent_handoff_log(target_dir: Path, workboard: dict) -> None:
    shared = workboard["sharedContext"]
    blockers = workboard["summary"]["blockingHighPriorityModuleIds"]
    lines = [
        "# Agent Handoff Log",
        "",
        "이 문서는 상위 설계 이후 실행 에이전트 간 baton, 범위, 검증 상태를 시간순으로 남긴다.",
        "",
        "## Shared Baseline",
        "",
        f"- Workboard: `{shared['workboardPath']}`",
        f"- Role plan: `{shared['rolePlanPath']}`",
        f"- Refinement status: `{shared['refinementStatusPath']}`",
        f"- Repo-local overrides: `{shared['repoLocalOverridesPath']}`",
        f"- Command catalog: `{shared['commandCatalogPath']}`",
        f"- Architecture map: `{shared['architectureMapPath']}`",
        f"- Handoff packet directory: `{shared['handoffPacketDirectoryPath']}`",
        "",
        f"- Design ready: `{'yes' if workboard['summary']['designReady'] else 'no'}`",
        "- Blocking high-priority modules:",
    ]
    if blockers:
        for module_id in blockers:
            lines.append(f"- `{module_id}`")
    else:
        lines.append("- 없음")

    lines.extend(["", "## Initial Work Lane Snapshot", ""])
    for lane in workboard["workLanes"]:
        lines.extend(
            [
                f"### {lane['title']} `{lane['id']}`",
                "",
                f"- Phase: `{lane['phase']}`",
                f"- Role: `{lane['role']}`",
                f"- Status: `{lane['status']}`",
                f"- Next handoff target: `{lane['nextHandoffTarget'] or '-'}`",
                f"- Latest packet path: `{lane['latestPacketPath'] or '-'}`",
                f"- Objective: {lane['objective']}",
                f"- Scope: {lane['scopeSummary']}",
                "",
                "Owned paths:",
            ]
        )
        for path in lane["ownedPaths"]:
            lines.append(f"- {path}")
        lines.extend(["", "Expected outputs:"])
        for output in lane["expectedOutputs"]:
            lines.append(f"- {output}")
        lines.extend(["", "Done when:"])
        for criterion in lane["doneWhen"]:
            lines.append(f"- {criterion}")
        lines.extend(["", "Notes:", f"- {lane['notes'] or '-'}", ""])

    lines.extend(["## Chronological Handoffs", "", "- 아직 기록 없음"])

    target_path = target_dir / "docs" / "ai" / "agent-handoff-log.md"
    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_generation_artifacts(target_dir: Path, spec: dict, template_name: str, scaffold_profile: str | None, support_level: str) -> None:
    meta_dir = target_dir / ".agent-base"
    meta_dir.mkdir(parents=True, exist_ok=True)
    refinement_manifest = derive_refinement_manifest(spec, scaffold_profile, support_level)
    refinement_status = derive_refinement_status(spec, refinement_manifest)
    context_manifest = derive_context_manifest(spec)
    coordination_mode = derive_coordination_mode(spec)
    role_plan = derive_agent_role_plan(spec)
    path_map = {
        "specPath": ".agent-base/project-generation-spec.json",
        "rolePlanPath": ".agent-base/agent-role-plan.json",
        "contextManifestPath": ".agent-base/context-manifest.json",
        "refinementManifestPath": ".agent-base/refinement-manifest.json",
        "refinementStatusPath": ".agent-base/refinement-status.json",
        "workboardPath": ".agent-base/agent-workboard.json",
        "repoLocalOverridesPath": "docs/ai/repo-local-overrides.md",
        "handoffLogPath": "docs/ai/agent-handoff-log.md",
        "handoffPacketDirectoryPath": "docs/ai/handoff-packets",
        "commandCatalogPath": "docs/ai/command-catalog.md",
        "architectureMapPath": "docs/ai/architecture-map.md",
        "precommitConfigPath": ".agent-base/pre-commit-config.json",
    }
    agent_workboard = derive_agent_workboard(spec, context_manifest, refinement_manifest, refinement_status, path_map)
    (meta_dir / "project-generation-spec.json").write_text(
        json.dumps(spec, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    manifest = {
        "template": template_name,
        "scaffoldProfile": scaffold_profile,
        "supportLevel": support_level,
        "requiredAgentRoles": spec["requiredAgentRoles"],
        "optionalAgentRoles": spec["optionalAgentRoles"],
        "roleSpecializations": spec["roleSpecializations"],
        "agentWorkflowOrder": spec["agentWorkflowOrder"],
        "recommendedCoordinationMode": coordination_mode["mode"],
        "coordinationModeSummary": coordination_mode["summary"],
        "coordinationModeReasons": list(coordination_mode["reasons"]),
        "refinementManifestPath": ".agent-base/refinement-manifest.json",
        "refinementStatusPath": ".agent-base/refinement-status.json",
        "agentWorkboardPath": ".agent-base/agent-workboard.json",
        "repoLocalOverridesPath": "docs/ai/repo-local-overrides.md",
        "handoffLogPath": "docs/ai/agent-handoff-log.md",
        "handoffPacketDirectoryPath": "docs/ai/handoff-packets",
        "starterCommandPath": "scripts/show_start_path.py",
        "starterCommand": "python3 scripts/show_start_path.py",
        "refinementModuleIds": [module["id"] for module in refinement_manifest["modules"]],
        "highPriorityRefinementModuleIds": refinement_manifest["summary"]["highPriorityModuleIds"],
    }
    (meta_dir / "generation-manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (meta_dir / "agent-role-plan.json").write_text(
        json.dumps(role_plan, indent=2, ensure_ascii=False)
        + "\n",
        encoding="utf-8",
    )
    (meta_dir / "context-manifest.json").write_text(
        json.dumps(context_manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (meta_dir / "refinement-manifest.json").write_text(
        json.dumps(refinement_manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (meta_dir / "refinement-status.json").write_text(
        json.dumps(refinement_status, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (meta_dir / "agent-workboard.json").write_text(
        json.dumps(agent_workboard, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    write_agent_handoff_log(target_dir, agent_workboard)
    if support_level == "docs-only":
        (target_dir / "TODO_UNSUPPORTED_SCAFFOLD.md").write_text(
            "# Unsupported Scaffold\n\n"
            "This project family / language / framework combination is not scaffolded yet.\n"
            "The docs template was generated successfully. Add a repo-local scaffold and overlay docs next.\n",
            encoding="utf-8",
        )


def write_precommit_config(target_dir: Path, spec: dict) -> None:
    config_path = target_dir / ".agent-base" / "pre-commit-config.json"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(
        json.dumps(build_precommit_config(spec), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def generate_project(spec: dict, output_root: Path, force: bool) -> Path:
    spec = normalize_spec(spec)
    template_name = TEMPLATE_BY_FAMILY[spec["projectFamily"]]
    target_dir = output_root / spec["repositoryName"]
    if target_dir.exists():
        if not force:
            raise FileExistsError(f"Target directory already exists: {target_dir}")
        safe_rmtree(target_dir)

    output_root.mkdir(parents=True, exist_ok=True)
    template_dir = TEMPLATES_DIR / template_name
    shutil.copytree(template_dir, target_dir)

    scaffold_profile, support_level = choose_scaffold(spec)
    if scaffold_profile:
        scaffold_dir = SCAFFOLDS_DIR / scaffold_profile
        copy_tree(scaffold_dir, target_dir)

    tokens = build_token_map(spec)
    apply_tokens(target_dir, tokens)
    write_root_readme(target_dir, spec, scaffold_profile, support_level)
    write_generation_artifacts(target_dir, spec, template_name, scaffold_profile, support_level)
    write_repo_local_overrides(target_dir, spec, derive_refinement_manifest(spec, scaffold_profile, support_level))
    write_precommit_config(target_dir, spec)
    return target_dir


def main() -> int:
    args = parse_args()
    spec_path = Path(args.spec).resolve()
    output_root = Path(args.output_root).resolve()
    spec = load_spec(spec_path)
    generated = generate_project(spec, output_root, args.force)
    print(json.dumps({"generated": str(generated)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
