#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from generate_project import (
    TEMPLATE_BY_FAMILY,
    choose_scaffold,
    derive_agent_coordination,
    derive_coordination_mode,
    derive_refinement_manifest,
    derive_refinement_status,
    generate_project,
    normalize_spec,
    validate_spec,
)


PROJECT_FAMILIES = [
    "game",
    "web-app",
    "pwa",
    "mobile-app",
    "backend-service",
    "batch-worker",
    "receiver-integration",
    "mockup-local",
    "library-tooling",
]

PROJECT_NATURES = [
    "prototype",
    "production",
    "internal-tool",
    "demo",
    "local-only",
    "research",
]

REPOSITORY_MODES = [
    "single-repo",
    "monorepo",
    "multi-repo",
]

RUNTIME_ROLES = [
    "frontend",
    "api",
    "batch",
    "receiver",
    "client",
    "tooling",
    "worker",
]

TARGET_PLATFORMS = [
    "browser",
    "server",
    "Windows",
    "macOS",
    "Linux",
    "Android",
    "iOS",
    "CLI",
    "WebGL",
]

TARGET_OS = [
    "Linux",
    "Windows",
    "macOS",
    "Android",
    "iOS",
]

DATASTORES = [
    "없음",
    "MariaDB",
    "PostgreSQL",
    "MySQL",
    "SQLite",
    "MongoDB",
    "Firestore",
]

CACHES = [
    "없음",
    "Redis",
    "in-memory",
    "Memcached",
]

DEPLOYMENT_TYPES = [
    "local-only",
    "static-hosting",
    "container",
    "VM",
    "serverless",
    "store-release",
    "package-registry",
]

LOGGING_MODES = [
    "console",
    "file",
    "structured-json",
    "remote-collector",
    "mixed",
]

SECURITY_PROFILES = [
    "없음",
    "session",
    "JWT",
    "OAuth2/OIDC",
    "platform-auth",
    "basic-auth",
    "api-key",
    "internal-auth",
]

TARGET_ENVIRONMENTS = [
    "local",
    "dev",
    "stg",
    "prd",
]

DOCUMENT_SET_OPTIONS = [
    "README",
    "build-guide",
    "test-plan",
    "deployment-checklist",
    "operations-manual",
    "impact-analysis",
    "runbook",
]

SCHEMA_OWNERSHIP_OPTIONS = [
    "owned",
    "shared",
    "external",
]

DEFAULTS_BY_FAMILY = {
    "game": {
        "targetUsers": ["gamers"],
        "targetPlatforms": ["Windows", "macOS"],
        "runtimeRoles": ["client", "tooling"],
        "language": "C#",
        "runtimeVersion": "Unity LTS",
        "framework": "Unity",
        "buildTool": "Unity",
        "testTool": "Unity validation",
        "datastore": "없음",
        "cache": "없음",
        "deploymentType": "local-only",
        "startupMode": "Unity player",
        "loggingMode": "console",
        "targetOs": ["Windows", "macOS"],
        "securityProfile": "없음",
        "externalIntegrations": [],
    },
    "web-app": {
        "targetUsers": ["internal-users"],
        "targetPlatforms": ["browser"],
        "runtimeRoles": ["frontend"],
        "language": "TypeScript",
        "runtimeVersion": "18",
        "framework": "React",
        "buildTool": "npm",
        "testTool": "npm test",
        "datastore": "없음",
        "cache": "없음",
        "deploymentType": "static-hosting",
        "startupMode": "SPA",
        "loggingMode": "console",
        "targetOs": ["Windows", "macOS", "Linux"],
        "securityProfile": "없음",
        "externalIntegrations": ["backend-service"],
    },
    "pwa": {
        "targetUsers": ["external-users"],
        "targetPlatforms": ["browser"],
        "runtimeRoles": ["frontend"],
        "language": "TypeScript",
        "runtimeVersion": "18",
        "framework": "React",
        "buildTool": "npm",
        "testTool": "npm test",
        "datastore": "없음",
        "cache": "없음",
        "deploymentType": "static-hosting",
        "startupMode": "SPA",
        "loggingMode": "console",
        "targetOs": ["Windows", "macOS", "Linux"],
        "securityProfile": "없음",
        "externalIntegrations": ["backend-service"],
    },
    "mobile-app": {
        "targetUsers": ["mobile-users"],
        "targetPlatforms": ["Android", "iOS"],
        "runtimeRoles": ["client"],
        "language": "Dart",
        "runtimeVersion": "3",
        "framework": "Flutter",
        "buildTool": "Flutter CLI",
        "testTool": "flutter test",
        "datastore": "없음",
        "cache": "없음",
        "deploymentType": "store-release",
        "startupMode": "mobile-package",
        "loggingMode": "console",
        "targetOs": ["Android", "iOS"],
        "securityProfile": "platform-auth",
        "externalIntegrations": ["backend-service"],
    },
    "backend-service": {
        "targetUsers": ["internal-services"],
        "targetPlatforms": ["server"],
        "runtimeRoles": ["api"],
        "language": "Java",
        "runtimeVersion": "11",
        "framework": "Spring Boot 2.3.x",
        "buildTool": "Gradle",
        "testTool": "Gradle test",
        "datastore": "MariaDB",
        "cache": "Redis",
        "deploymentType": "container",
        "startupMode": "long-running-service",
        "loggingMode": "structured-json",
        "targetOs": ["Linux"],
        "securityProfile": "JWT",
        "externalIntegrations": ["internal-api"],
    },
    "batch-worker": {
        "targetUsers": ["operators"],
        "targetPlatforms": ["server"],
        "runtimeRoles": ["batch"],
        "language": "Java",
        "runtimeVersion": "11",
        "framework": "Spring Boot 2.7.x",
        "buildTool": "Gradle",
        "testTool": "Gradle test",
        "datastore": "MariaDB",
        "cache": "Redis",
        "deploymentType": "container",
        "startupMode": "scheduled-job",
        "loggingMode": "structured-json",
        "targetOs": ["Linux"],
        "securityProfile": "internal-auth",
        "externalIntegrations": ["scheduler", "database"],
    },
    "receiver-integration": {
        "targetUsers": ["integrations"],
        "targetPlatforms": ["server"],
        "runtimeRoles": ["receiver"],
        "language": "Java",
        "runtimeVersion": "11",
        "framework": "Spring Boot 2.7.x",
        "buildTool": "Gradle",
        "testTool": "Gradle test",
        "datastore": "MariaDB",
        "cache": "Redis",
        "deploymentType": "container",
        "startupMode": "event-driven-worker",
        "loggingMode": "structured-json",
        "targetOs": ["Linux"],
        "securityProfile": "internal-auth",
        "externalIntegrations": ["MQTT", "internal-api"],
    },
    "mockup-local": {
        "targetUsers": ["internal-reviewers"],
        "targetPlatforms": ["browser"],
        "runtimeRoles": ["frontend"],
        "language": "TypeScript",
        "runtimeVersion": "18",
        "framework": "Vite",
        "buildTool": "npm",
        "testTool": "npm run build.dev",
        "datastore": "없음",
        "cache": "없음",
        "deploymentType": "local-only",
        "startupMode": "local-preview",
        "loggingMode": "console",
        "targetOs": ["Windows", "macOS", "Linux"],
        "securityProfile": "없음",
        "externalIntegrations": [],
    },
    "library-tooling": {
        "targetUsers": ["developers"],
        "targetPlatforms": ["CLI"],
        "runtimeRoles": ["tooling"],
        "language": "TypeScript",
        "runtimeVersion": "18",
        "framework": "Node.js tooling",
        "buildTool": "npm",
        "testTool": "npm test",
        "datastore": "없음",
        "cache": "없음",
        "deploymentType": "package-registry",
        "startupMode": "CLI",
        "loggingMode": "console",
        "targetOs": ["Linux", "macOS", "Windows"],
        "securityProfile": "없음",
        "externalIntegrations": [],
    },
}

LANGUAGE_OPTIONS_BY_FAMILY = {
    "game": ["C#", "TypeScript"],
    "web-app": ["TypeScript", "JavaScript"],
    "pwa": ["TypeScript", "JavaScript"],
    "mobile-app": ["Dart", "TypeScript", "Kotlin", "Swift"],
    "backend-service": ["Java", "Kotlin"],
    "batch-worker": ["Java", "Kotlin"],
    "receiver-integration": ["Java", "Kotlin"],
    "mockup-local": ["TypeScript", "JavaScript", "HTML/CSS/JS"],
    "library-tooling": ["TypeScript", "Java"],
}

FRAMEWORK_OPTIONS_BY_FAMILY = {
    "game": ["Unity", "Godot", "custom"],
    "web-app": ["React", "Vue", "Svelte", "custom"],
    "pwa": ["React", "Vue", "Svelte", "custom"],
    "mobile-app": ["Flutter", "React Native", "Kotlin Android", "Swift iOS", "custom"],
    "backend-service": ["Spring Boot 2.3.x", "Spring Boot 3.x", "Micronaut", "Quarkus", "custom"],
    "batch-worker": ["Spring Boot 2.7.x", "Spring Batch", "custom"],
    "receiver-integration": ["Spring Boot 2.7.x", "custom"],
    "mockup-local": ["Vite", "Static HTML", "custom"],
    "library-tooling": ["Node.js tooling", "Spring Boot CLI", "custom"],
}

STARTUP_OPTIONS_BY_FAMILY = {
    "game": ["Unity player", "editor tooling"],
    "web-app": ["SPA", "SSR"],
    "pwa": ["SPA", "installable PWA"],
    "mobile-app": ["mobile-package"],
    "backend-service": ["long-running-service"],
    "batch-worker": ["scheduled-job", "manual batch trigger"],
    "receiver-integration": ["event-driven-worker", "long-running-service"],
    "mockup-local": ["local-preview", "CLI"],
    "library-tooling": ["CLI", "library package"],
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run an interactive bootstrap interview and generate a sample project.")
    parser.add_argument("--output-root", help="Directory where the generated sample repository will be created")
    parser.add_argument("--spec-path", help="Path where the generated project spec JSON will be saved")
    parser.add_argument("--skip-generate", action="store_true", help="Save the spec only and skip sample repository generation")
    parser.add_argument("--force", action="store_true", help="Overwrite the generated repository if it already exists")
    return parser.parse_args()


def slugify(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-").lower()
    return slug or "new-project"


def package_safe(value: str) -> str:
    cleaned = re.sub(r"[^a-z0-9]+", "", value.lower())
    return cleaned or "sample"


def default_package_name(repository_name: str) -> str:
    return f"com.example.{package_safe(repository_name)}"


def default_target_environments(project_nature: str) -> list[str]:
    if project_nature == "production":
        return ["local", "dev", "stg", "prd"]
    if project_nature == "local-only":
        return ["local"]
    return ["local", "dev"]


def default_db_engine(datastore: str) -> str:
    mapping = {
        "MariaDB": "MariaDB 10.x",
        "PostgreSQL": "PostgreSQL 14+",
        "MySQL": "MySQL 8.x",
        "SQLite": "SQLite 3.x",
        "MongoDB": "MongoDB 6.x",
        "Firestore": "Firestore managed",
    }
    return mapping.get(datastore, datastore)


def default_migration_path(project_family: str, language: str) -> str:
    if language.lower() in {"java", "kotlin"}:
        return "db/migration"
    if project_family in {"web-app", "pwa", "mobile-app"}:
        return "docs/sql"
    return "sql"


def unique(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item and item not in seen:
            seen.add(item)
            result.append(item)
    return result


def derive_base_document_set(spec: dict) -> list[str]:
    docs = ["README", "build-guide", "test-plan"]
    if spec["deploymentType"] != "local-only":
        docs.append("deployment-checklist")
    if spec["projectFamily"] in {"backend-service", "batch-worker", "receiver-integration"} or spec["projectNature"] == "production":
        docs.append("operations-manual")
    if spec["datastore"] != "없음":
        docs.append("impact-analysis")
    return unique(docs)


def detect_exceptions(spec: dict, family_defaults: dict) -> list[str]:
    exceptions: list[str] = []
    for key in ["language", "runtimeVersion", "framework", "buildTool", "testTool", "deploymentType", "startupMode"]:
        default = family_defaults.get(key)
        actual = spec.get(key)
        if default and actual and actual != default:
            exceptions.append(f"{key} uses `{actual}` instead of family default `{default}`")
    if spec["repositoryMode"] != "single-repo":
        exceptions.append(
            "repositoryMode is not `single-repo`; generator v1 still creates one sample repository and requires manual expansion."
        )
    return exceptions


def print_header(title: str) -> None:
    print()
    print("=" * len(title))
    print(title)
    print("=" * len(title))


def prompt_text(label: str, default: str | None = None, required: bool = True) -> str:
    while True:
        suffix = f" [{default}]" if default not in {None, ""} else ""
        value = input(f"{label}{suffix}: ").strip()
        if value:
            return value
        if default not in {None, ""}:
            return str(default)
        if not required:
            return ""
        print("값을 입력해주세요.")


def prompt_yes_no(label: str, default: bool = True) -> bool:
    default_label = "Y/n" if default else "y/N"
    while True:
        raw = input(f"{label} [{default_label}]: ").strip().lower()
        if not raw:
            return default
        if raw in {"y", "yes"}:
            return True
        if raw in {"n", "no"}:
            return False
        print("y 또는 n 으로 입력해주세요.")


def prompt_choice(label: str, options: list[str], default: str | None = None) -> str:
    print_header(label)
    for idx, option in enumerate(options, start=1):
        marker = " (default)" if option == default else ""
        print(f"{idx}. {option}{marker}")
    while True:
        raw = input("번호 또는 값을 입력하세요: ").strip()
        if not raw and default is not None:
            return default
        if raw.isdigit():
            index = int(raw) - 1
            if 0 <= index < len(options):
                return options[index]
        for option in options:
            if raw.lower() == option.lower():
                return option
        if raw:
            return raw
        print("유효한 값을 입력해주세요.")


def prompt_multi(label: str, options: list[str], default: list[str] | None = None) -> list[str]:
    default = default or []
    print_header(label)
    for idx, option in enumerate(options, start=1):
        marker = " (default)" if option in default else ""
        print(f"{idx}. {option}{marker}")
    print("여러 개를 고를 때는 쉼표로 구분하세요. 예: 1,3")
    while True:
        default_text = ", ".join(default)
        raw = input(f"선택 [{default_text}]: ").strip()
        if not raw:
            return default
        values: list[str] = []
        for part in raw.split(","):
            token = part.strip()
            if not token:
                continue
            if token.isdigit():
                index = int(token) - 1
                if 0 <= index < len(options):
                    values.append(options[index])
                    continue
            matched = next((option for option in options if token.lower() == option.lower()), None)
            values.append(matched or token)
        values = unique(values)
        if values:
            return values
        print("하나 이상 선택해주세요.")


def prompt_list(label: str, default: list[str] | None = None) -> list[str]:
    default = default or []
    default_text = ", ".join(default)
    raw = input(f"{label} [{default_text}]: ").strip()
    if not raw:
        return default
    return unique([item.strip() for item in raw.split(",") if item.strip()])


def family_defaults(project_family: str, project_nature: str) -> dict:
    defaults = dict(DEFAULTS_BY_FAMILY[project_family])
    defaults["targetEnvironments"] = default_target_environments(project_nature)
    return defaults


def build_interactive_spec(args: argparse.Namespace) -> tuple[dict, Path, Path]:
    print_header("프로젝트 bootstrap 인터뷰")
    project_name = prompt_text("프로젝트명")
    repository_name = prompt_text("저장소명", slugify(project_name))
    project_purpose = prompt_text("프로젝트 목적")
    project_family = prompt_choice("프로젝트 패밀리", PROJECT_FAMILIES)
    project_nature = prompt_choice("프로젝트 성격", PROJECT_NATURES, "prototype")
    repository_mode = prompt_choice("저장소 구성 방식", REPOSITORY_MODES, "single-repo")

    defaults = family_defaults(project_family, project_nature)

    target_users = prompt_list("대상 사용자 (쉼표 구분)", defaults["targetUsers"])
    target_platforms = prompt_multi("대상 플랫폼", TARGET_PLATFORMS, defaults["targetPlatforms"])
    runtime_roles = prompt_multi("런타임 역할", RUNTIME_ROLES, defaults["runtimeRoles"])
    language = prompt_choice("프로그램 언어", LANGUAGE_OPTIONS_BY_FAMILY[project_family], defaults["language"])
    framework = prompt_choice("프레임워크", FRAMEWORK_OPTIONS_BY_FAMILY[project_family], defaults["framework"])
    runtime_version = prompt_text("런타임 버전", defaults["runtimeVersion"])
    build_tool = prompt_text("빌드 도구", defaults["buildTool"])
    test_tool = prompt_text("테스트 도구", defaults["testTool"])
    datastore = prompt_choice("데이터 저장소", DATASTORES, defaults["datastore"])
    cache = prompt_choice("캐시", CACHES, defaults["cache"])
    deployment_type = prompt_choice("배포 유형", DEPLOYMENT_TYPES, defaults["deploymentType"])
    startup_mode = prompt_choice("서비스 기동 형태", STARTUP_OPTIONS_BY_FAMILY[project_family], defaults["startupMode"])
    logging_mode = prompt_choice("로깅 방식", LOGGING_MODES, defaults["loggingMode"])
    target_os = prompt_multi("동작 OS", TARGET_OS, defaults["targetOs"])
    security_profile = prompt_choice("보안/인증 방식", SECURITY_PROFILES, defaults["securityProfile"])
    target_environments = prompt_multi("대상 환경", TARGET_ENVIRONMENTS, defaults["targetEnvironments"])
    external_integrations = prompt_list("핵심 외부 연동 (쉼표 구분)", defaults["externalIntegrations"])

    spec: dict = {
        "repositoryName": repository_name,
        "projectName": project_name,
        "projectPurpose": project_purpose,
        "projectFamily": project_family,
        "projectNature": project_nature,
        "repositoryMode": repository_mode,
        "targetUsers": target_users,
        "targetPlatforms": target_platforms,
        "runtimeRoles": runtime_roles,
        "language": language,
        "runtimeVersion": runtime_version,
        "framework": framework,
        "buildTool": build_tool,
        "testTool": test_tool,
        "datastore": datastore,
        "cache": cache,
        "deploymentType": deployment_type,
        "startupMode": startup_mode,
        "loggingMode": logging_mode,
        "targetOs": target_os,
        "securityProfile": security_profile,
        "targetEnvironments": target_environments,
        "externalIntegrations": external_integrations,
    }

    if language.lower() == "java":
        spec["packageName"] = prompt_text("Java packageName", default_package_name(repository_name))

    if datastore != "없음":
        spec["dbEngine"] = prompt_text("DB 엔진/버전", default_db_engine(datastore))
        spec["schemaOwnership"] = prompt_choice("schema ownership", SCHEMA_OWNERSHIP_OPTIONS, "owned")
        spec["migrationPath"] = prompt_text("migration 경로", default_migration_path(project_family, language))

    suggested_docs = derive_base_document_set(spec)
    spec["baseDocumentSet"] = prompt_multi("기본 문서 세트", DOCUMENT_SET_OPTIONS, suggested_docs)
    exceptions = detect_exceptions(spec, defaults)
    extra_exceptions = prompt_list("추가 예외/메모 (쉼표 구분, 없으면 Enter)", [])
    spec["exceptions"] = unique(exceptions + extra_exceptions)
    spec.update(derive_agent_coordination(spec))

    output_root_default = args.output_root or str(Path.cwd() / "generated-projects")
    output_root = Path(prompt_text("샘플 저장소 output root", output_root_default)).expanduser().resolve()
    spec_path_default = args.spec_path or str(output_root / "_specs" / f"{repository_name}.json")
    spec_path = Path(prompt_text("spec 저장 경로", spec_path_default)).expanduser().resolve()

    spec = normalize_spec(spec)
    validate_spec(spec)
    return spec, output_root, spec_path


def refinement_path_for_spec(spec_path: Path) -> Path:
    return spec_path.with_name(f"{spec_path.stem}.refinement.json")


def refinement_status_path_for_spec(spec_path: Path) -> Path:
    return spec_path.with_name(f"{spec_path.stem}.refinement-status.json")


def print_summary(spec: dict, output_root: Path, spec_path: Path) -> None:
    print_header("확정된 project generation spec")
    print(json.dumps(spec, indent=2, ensure_ascii=False))
    template_name = TEMPLATE_BY_FAMILY[spec["projectFamily"]]
    scaffold_profile, support_level = choose_scaffold(spec)
    refinement_manifest = derive_refinement_manifest(spec, scaffold_profile, support_level)
    coordination_mode = derive_coordination_mode(spec)
    print()
    print("선택 결과")
    print(f"- template: {template_name}")
    print(f"- scaffold profile: {scaffold_profile or 'docs-only'}")
    print(f"- scaffold support level: {support_level}")
    print(f"- core agent roles: {', '.join(spec['requiredAgentRoles'])}")
    print(f"- extended agent roles: {', '.join(spec['optionalAgentRoles'])}")
    print(f"- role specializations: {', '.join(spec['roleSpecializations'])}")
    print(
        f"- recommended coordination mode: {coordination_mode['label']} ({coordination_mode['summary']})"
    )
    print(f"- output root: {output_root}")
    print(f"- spec path: {spec_path}")
    print(f"- refinement path: {refinement_path_for_spec(spec_path)}")
    print(f"- refinement status path: {refinement_status_path_for_spec(spec_path)}")
    print("- next context path: AGENTS.md -> context-profiles.md -> start-bootstrap.md")
    if spec["repositoryMode"] != "single-repo":
        print("- note: v1 generator는 샘플 저장소 1개만 만들고, monorepo/multi-repo 확장은 후속 수작업이 필요합니다.")
    if coordination_mode["reasons"]:
        print("- coordination reasons:")
        for reason in coordination_mode["reasons"]:
            print(f"  - {reason}")
    print()
    print("Refinement preview")
    print(f"- modules: {refinement_manifest['summary']['moduleCount']}")
    high_priority = refinement_manifest["summary"]["highPriorityModuleIds"]
    if high_priority:
        print(f"- high-priority modules: {', '.join(high_priority)}")
    print("- decision modes: decide-now, keep-default, defer-with-note")
    for module in refinement_manifest["modules"]:
        print(f"- {module['id']} [{module['priority']}]: {module['title']}")


def write_spec(spec: dict, spec_path: Path) -> None:
    spec_path.parent.mkdir(parents=True, exist_ok=True)
    spec_path.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_refinement_manifest(spec: dict, spec_path: Path) -> Path:
    scaffold_profile, support_level = choose_scaffold(spec)
    refinement_path = refinement_path_for_spec(spec_path)
    refinement_path.parent.mkdir(parents=True, exist_ok=True)
    refinement_manifest = derive_refinement_manifest(spec, scaffold_profile, support_level)
    refinement_path.write_text(
        json.dumps(refinement_manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return refinement_path


def write_refinement_status(spec: dict, spec_path: Path) -> Path:
    scaffold_profile, support_level = choose_scaffold(spec)
    refinement_manifest = derive_refinement_manifest(spec, scaffold_profile, support_level)
    refinement_status = derive_refinement_status(spec, refinement_manifest)
    refinement_status_path = refinement_status_path_for_spec(spec_path)
    refinement_status_path.parent.mkdir(parents=True, exist_ok=True)
    refinement_status_path.write_text(
        json.dumps(refinement_status, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return refinement_status_path


def main() -> int:
    args = parse_args()
    spec, output_root, spec_path = build_interactive_spec(args)
    coordination_mode = derive_coordination_mode(spec)
    print_summary(spec, output_root, spec_path)

    if not prompt_yes_no("이 spec을 저장할까요?", True):
        print(json.dumps({"cancelled": "spec-not-saved"}, ensure_ascii=False))
        return 0

    write_spec(spec, spec_path)
    refinement_path = write_refinement_manifest(spec, spec_path)
    refinement_status_path = write_refinement_status(spec, spec_path)

    if args.skip_generate:
        print(
            json.dumps(
                {
                    "savedSpec": str(spec_path),
                    "savedRefinementManifest": str(refinement_path),
                    "savedRefinementStatus": str(refinement_status_path),
                    "recommendedCoordinationMode": coordination_mode["mode"],
                    "generated": None,
                },
                ensure_ascii=False,
            )
        )
        return 0

    if not prompt_yes_no("이 spec으로 샘플 저장소를 생성할까요?", True):
        print(
            json.dumps(
                {
                    "savedSpec": str(spec_path),
                    "savedRefinementManifest": str(refinement_path),
                    "savedRefinementStatus": str(refinement_status_path),
                    "recommendedCoordinationMode": coordination_mode["mode"],
                    "generated": None,
                },
                ensure_ascii=False,
            )
        )
        return 0

    generated = generate_project(spec, output_root, args.force)
    print(
        json.dumps(
                {
                    "savedSpec": str(spec_path),
                    "savedRefinementManifest": str(refinement_path),
                    "savedRefinementStatus": str(refinement_status_path),
                    "recommendedCoordinationMode": coordination_mode["mode"],
                    "generated": str(generated),
                    "generatedContextManifest": str(generated / ".agent-base" / "context-manifest.json"),
                    "generatedRefinementManifest": str(generated / ".agent-base" / "refinement-manifest.json"),
                    "generatedRefinementStatus": str(generated / ".agent-base" / "refinement-status.json"),
                    "generatedAgentWorkboard": str(generated / ".agent-base" / "agent-workboard.json"),
                    "generatedHandoffLog": str(generated / "docs" / "ai" / "agent-handoff-log.md"),
                },
                ensure_ascii=False,
            )
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
