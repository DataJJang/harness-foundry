#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = REPO_ROOT / ".agent-base" / "pre-commit-config.json"
PROJECT_SPEC_PATH = REPO_ROOT / ".agent-base" / "project-generation-spec.json"

CODE_EXTENSIONS = {
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".css",
    ".scss",
    ".html",
    ".java",
    ".kt",
    ".kts",
    ".cs",
    ".dart",
    ".xml",
    ".sql",
    ".yml",
    ".yaml",
    ".properties",
    ".json",
}

DEFAULT_CONFIG = {
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run repository pre-commit checks.")
    parser.add_argument("--dry-run", action="store_true", help="Print selected commands without executing them")
    parser.add_argument(
        "--staged-file",
        action="append",
        default=[],
        help="Inject a staged file path for testing without reading git index",
    )
    return parser.parse_args()


def load_config() -> dict:
    if not CONFIG_PATH.exists():
        return dict(DEFAULT_CONFIG)
    with CONFIG_PATH.open("r", encoding="utf-8") as fp:
        loaded = json.load(fp)
    config = dict(DEFAULT_CONFIG)
    config.update(loaded)
    for key in ["customCommands", "additionalCommands", "unityValidationCommands"]:
        if not isinstance(config.get(key), list):
            config[key] = []
    return config


def load_project_spec() -> dict:
    if not PROJECT_SPEC_PATH.exists():
        return {}
    with PROJECT_SPEC_PATH.open("r", encoding="utf-8") as fp:
        return json.load(fp)


def get_staged_files(injected: list[str]) -> list[str]:
    if injected:
        return injected
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMRTUXB"],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def path_matches(staged_files: list[str], suffixes: set[str], prefixes: tuple[str, ...]) -> bool:
    for raw in staged_files:
        path = Path(raw)
        if path.suffix.lower() in suffixes:
            return True
        if raw.startswith(prefixes):
            return True
    return False


def first_available_package_script(scripts: dict[str, str], candidates: list[str]) -> str | None:
    for candidate in candidates:
        if candidate in scripts:
            return candidate
    return None


def infer_preset_profile(config: dict, spec: dict) -> str:
    preset = str(config.get("presetProfile", "auto")).strip() or "auto"
    if preset != "auto":
        return preset

    family = str(spec.get("projectFamily", "")).strip().lower()
    language = str(spec.get("language", "")).strip().lower()
    framework = str(spec.get("framework", "")).strip().lower()

    if family == "library-tooling":
        if language == "typescript":
            return "library-tooling-typescript"
        if language == "java":
            return "library-tooling-java"

    mapping = {
        "web-app": "web-app",
        "pwa": "pwa",
        "backend-service": "backend-service",
        "batch-worker": "batch-worker",
        "receiver-integration": "receiver-integration",
        "mockup-local": "mockup-local",
    }
    if family == "web-app" and language == "java":
        return "web-app-java"
    if family in mapping:
        return mapping[family]
    if family == "game":
        if "unity" in framework or language in {"c#", "csharp"}:
            return "unity-game"
        return "game"
    if family == "mobile-app":
        if "flutter" in framework or language == "dart":
            return "mobile-flutter"
        return "mobile-app"

    if (REPO_ROOT / "ProjectSettings" / "ProjectVersion.txt").exists():
        return "unity-game"
    if (REPO_ROOT / "pubspec.yaml").exists():
        return "mobile-flutter"
    if (REPO_ROOT / "gradlew").exists():
        return "java-service"
    if (REPO_ROOT / "package.json").exists():
        return "web-node"
    return "generic"


def read_package_scripts(package_json: Path) -> dict[str, str]:
    try:
        with package_json.open("r", encoding="utf-8") as fp:
            payload = json.load(fp)
    except FileNotFoundError:
        return {}
    return payload.get("scripts", {})


def command_exists(command: str) -> bool:
    return shutil_which(command) is not None


def shutil_which(command: str) -> str | None:
    result = subprocess.run(
        ["sh", "-lc", f"command -v {command} >/dev/null 2>&1 && command -v {command}"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def autodetect_commands(staged_files: list[str], config: dict, spec: dict) -> tuple[str, list[str]]:
    commands: list[str] = []
    preset = infer_preset_profile(config, spec)

    package_json = REPO_ROOT / "package.json"
    gradlew = REPO_ROOT / "gradlew"
    pom_xml = REPO_ROOT / "pom.xml"
    mvnw = REPO_ROOT / "mvnw"
    pubspec = REPO_ROOT / "pubspec.yaml"
    unity_version = REPO_ROOT / "ProjectSettings" / "ProjectVersion.txt"

    package_json_changed = path_matches(
        staged_files,
        {".js", ".jsx", ".ts", ".tsx", ".css", ".scss", ".html", ".json", ".mjs", ".cjs"},
        ("src/", "public/", "app/", "pages/", "components/", "package.json", "vite.config", "tsconfig", "lib/"),
    )
    java_changed = path_matches(
        staged_files,
        {".java", ".kt", ".kts", ".sql", ".xml", ".yml", ".yaml", ".properties"},
        (
            "src/main/",
            "src/test/",
            "build.gradle",
            "settings.gradle",
            "gradle/",
            "pom.xml",
            "mvnw",
            ".mvn/",
            "docs/sql/",
            "db/",
            "src/main/resources/",
        ),
    )
    unity_changed = path_matches(
        staged_files,
        {".cs", ".shader", ".json", ".asset", ".prefab", ".unity"},
        ("Assets/", "Packages/", "ProjectSettings/"),
    )
    flutter_changed = path_matches(
        staged_files,
        {".dart", ".yaml", ".yml"},
        ("lib/", "test/", "android/", "ios/", "pubspec.yaml"),
    )

    if package_json.exists() and preset in {
        "web-app",
        "pwa",
        "mockup-local",
        "library-tooling-typescript",
        "web-node",
    } and package_json_changed:
        scripts = read_package_scripts(package_json)
        if config.get("runLintOnHook"):
            lint_script = first_available_package_script(scripts, ["lint"])
            if lint_script:
                commands.append(f"npm run {lint_script}")
        if config.get("runTypecheckOnHook"):
            typecheck_script = first_available_package_script(scripts, ["typecheck"])
            if typecheck_script:
                commands.append(f"npm run {typecheck_script}")
        if config.get("runBuildOnHook"):
            build_script = first_available_package_script(scripts, ["build.dev", "build"])
            if build_script:
                commands.append(f"npm run {build_script}")
        if config.get("runTestOnHook"):
            test_script = first_available_package_script(scripts, ["test"])
            if test_script:
                commands.append(f"npm run {test_script}")

    java_presets = {
        "web-app-java",
        "backend-service",
        "batch-worker",
        "receiver-integration",
        "library-tooling-java",
        "java-service",
    }
    if preset in java_presets and java_changed:
        if gradlew.exists():
            commands.append("./gradlew compileJava")
            if config.get("runBuildOnHook"):
                commands.append("./gradlew build")
            if config.get("runTestOnHook") or path_matches(staged_files, {".java", ".kt", ".kts"}, ("src/test/",)):
                commands.append("./gradlew test")
        elif pom_xml.exists():
            maven_command = "./mvnw" if mvnw.exists() else "mvn"
            commands.append(f"{maven_command} -q -DskipTests compile")
            if config.get("runBuildOnHook"):
                commands.append(f"{maven_command} -q -DskipTests package")
            if config.get("runTestOnHook") or path_matches(staged_files, {".java", ".kt", ".kts"}, ("src/test/",)):
                commands.append(f"{maven_command} -q test")

    if pubspec.exists() and preset in {"mobile-flutter", "mobile-app"} and flutter_changed:
        if (config.get("runLintOnHook") or config.get("runTypecheckOnHook")) and command_exists("flutter"):
            commands.append("flutter analyze")
        elif (config.get("runLintOnHook") or config.get("runTypecheckOnHook")) and command_exists("dart"):
            commands.append("dart analyze")
        if config.get("runTestOnHook") and command_exists("flutter"):
            commands.append("flutter test")
        elif config.get("runTestOnHook") and command_exists("dart"):
            commands.append("dart test")

    if unity_version.exists() and preset in {"unity-game", "game"} and unity_changed:
        unity_commands = config.get("unityValidationCommands", [])
        if unity_commands:
            commands.extend(unity_commands)

    commands.extend(config.get("additionalCommands", []))

    deduped: list[str] = []
    seen: set[str] = set()
    for command in commands:
        if command and command not in seen:
            seen.add(command)
            deduped.append(command)
    return preset, deduped


def run_commands(commands: list[str], dry_run: bool) -> int:
    if not commands:
        print("[pre-commit] no commands selected")
        return 0

    print("[pre-commit] selected commands:")
    for command in commands:
        print(f"- {command}")

    if dry_run:
        return 0

    for command in commands:
        print(f"[pre-commit] running: {command}")
        result = subprocess.run(command, cwd=REPO_ROOT, shell=True)
        if result.returncode != 0:
            print(f"[pre-commit] failed: {command}", file=sys.stderr)
            return result.returncode
    return 0


def main() -> int:
    args = parse_args()
    config = load_config()
    spec = load_project_spec()
    staged_files = get_staged_files(args.staged_file)

    if not staged_files:
        print("[pre-commit] no staged files")
        return 0

    print("[pre-commit] staged files:")
    for staged in staged_files:
        print(f"- {staged}")

    if config.get("mode", "auto") == "custom":
        commands = list(config.get("customCommands", []))
        preset = infer_preset_profile(config, spec)
    else:
        preset, commands = autodetect_commands(staged_files, config, spec)
        if config.get("customCommands"):
            commands.extend(config["customCommands"])

    print(f"[pre-commit] preset profile: {preset}")

    if not commands:
        if config.get("failWhenNoChecksRun"):
            print("[pre-commit] no checks configured and failWhenNoChecksRun=true", file=sys.stderr)
            return 1
        print("[pre-commit] no matching checks; commit is allowed")
        return 0

    return run_commands(commands, args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
