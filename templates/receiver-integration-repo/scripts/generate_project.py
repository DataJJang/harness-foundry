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


def derive_context_manifest(spec: dict) -> dict:
    mode = "bootstrap"
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
        "coreRoles": spec["requiredAgentRoles"],
        "extendedRoles": spec["optionalAgentRoles"],
        "roleSpecializations": spec["roleSpecializations"],
        "contextBudget": dict(CONTEXT_BUDGET),
    }


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

## Next Steps

1. Review `AGENTS.md`, `docs/ai/project-bootstrap.md`, and `docs/ai/command-catalog.md`.
2. Install the local git hook pack with `python3 scripts/install_git_hooks.py`.
3. Review `.agent-base/pre-commit-config.json` and align the preset with the real repository commands.
4. Review `.agent-base/context-manifest.json` and load only the recommended fast-path docs first.
5. Update commands, package names, env files, and runtime assumptions to the real repository state.
6. Run the first build, compile, test, and smoke validation.
7. Complete `checklists/project-creation.md` and `checklists/first-delivery.md`.
"""
    (target_dir / "README.md").write_text(readme, encoding="utf-8")


def write_generation_artifacts(target_dir: Path, spec: dict, template_name: str, scaffold_profile: str | None, support_level: str) -> None:
    meta_dir = target_dir / ".agent-base"
    meta_dir.mkdir(parents=True, exist_ok=True)
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
    }
    (meta_dir / "generation-manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (meta_dir / "agent-role-plan.json").write_text(
        json.dumps(
            {
                "requiredAgentRoles": spec["requiredAgentRoles"],
                "optionalAgentRoles": spec["optionalAgentRoles"],
                "roleSpecializations": spec["roleSpecializations"],
                "agentWorkflowOrder": spec["agentWorkflowOrder"],
                "agentRoleOverrides": spec["agentRoleOverrides"],
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    (meta_dir / "context-manifest.json").write_text(
        json.dumps(derive_context_manifest(spec), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
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
