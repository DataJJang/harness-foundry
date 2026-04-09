#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path


IGNORED_PARTS = {
    ".git",
    ".gradle",
    ".idea",
    ".next",
    ".venv",
    "__pycache__",
    "build",
    "coverage",
    "dist",
    "node_modules",
    "out",
    "target",
}

BUILD_PATTERNS = [
    "package.json",
    "pnpm-workspace.yaml",
    "yarn.lock",
    "package-lock.json",
    "build.gradle",
    "build.gradle.kts",
    "settings.gradle",
    "settings.gradle.kts",
    "pom.xml",
    "mvnw",
    "gradlew",
    "pubspec.yaml",
    "Packages/manifest.json",
]

CONFIG_PATTERNS = [
    ".env",
    ".env.local",
    ".env.dev",
    ".env.prod",
    "**/application.yml",
    "**/application.yaml",
    "**/application.properties",
    "**/bootstrap.yml",
    "**/bootstrap.yaml",
    "**/bootstrap.properties",
    "**/web.xml",
    "**/dispatcher-servlet.xml",
    "**/servlet-context.xml",
    "**/context-*.xml",
    "**/globals.properties",
    "**/tiles*.xml",
    "**/*tiles*.xml",
    "**/logback.xml",
    "**/logback-spring.xml",
]

DOC_PATTERNS = [
    "README.md",
    "AGENTS.md",
    "docs/**/*.md",
    "docs/ai/**/*.md",
]

CI_PATTERNS = [
    ".github/workflows/*.yml",
    ".github/workflows/*.yaml",
    ".gitlab-ci.yml",
    "Jenkinsfile",
    "azure-pipelines.yml",
]

DEPLOYMENT_PATTERNS = [
    "Dockerfile",
    "Dockerfile.*",
    "docker-compose.yml",
    "docker-compose.yaml",
    "docker-compose.*.yml",
    "docker-compose.*.yaml",
    "compose.yml",
    "compose.yaml",
    "k8s/**/*.yml",
    "k8s/**/*.yaml",
    "helm/**/*.yml",
    "helm/**/*.yaml",
    "charts/**/*.yml",
    "charts/**/*.yaml",
]

MIGRATION_PATTERNS = [
    "db/migration/**",
    "sql/**",
    "database/**",
    "src/main/resources/db/migration/**",
    "src/main/resources/mapper/**",
    "src/main/resources/mappers/**",
    "src/main/webapp/WEB-INF/jsp/**",
    "src/main/webapp/WEB-INF/tlds/**",
]

ENTRYPOINT_PATTERNS = [
    "src/main/java/**/*Application.java",
    "src/main/kotlin/**/*Application.kt",
    "src/main/webapp/WEB-INF/web.xml",
    "server.js",
    "app.js",
    "src/main.ts",
    "src/main.js",
    "lib/main.dart",
]

CODE_PATTERNS = [
    "src/main/java/**/*.java",
    "src/main/kotlin/**/*.kt",
    "src/main/resources/**/*.xml",
    "src/main/resources/**/*.properties",
    "src/main/resources/**/*.yml",
    "src/main/resources/**/*.yaml",
    "src/main/webapp/WEB-INF/**/*.xml",
    "src/main/webapp/WEB-INF/**/*.jsp",
    "src/main/webapp/**/*.css",
    "src/main/webapp/**/*.js",
    "src/main/resources/static/**/*.css",
    "src/main/resources/static/**/*.js",
    "src/main/resources/templates/**/*.html",
    "src/**/*.ts",
    "src/**/*.js",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze an existing repository and emit an adoption inventory bundle.")
    parser.add_argument("--repo", default=".", help="Target repository root")
    parser.add_argument("--output", help="Output path for repository inventory JSON")
    parser.add_argument("--docs-gap-output", help="Output path for docs gap markdown")
    parser.add_argument("--role-output", help="Output path for role recommendation JSON")
    return parser.parse_args()


def is_ignored(root: Path, path: Path) -> bool:
    try:
        parts = path.relative_to(root).parts
    except ValueError:
        return True
    return any(part in IGNORED_PARTS for part in parts)


def glob_files(root: Path, patterns: list[str]) -> list[Path]:
    results: list[Path] = []
    seen: set[str] = set()
    for pattern in patterns:
        for path in root.glob(pattern):
            if not path.is_file():
                continue
            if is_ignored(root, path):
                continue
            rel = path.relative_to(root).as_posix()
            if rel in seen:
                continue
            seen.add(rel)
            results.append(path)
    return sorted(results, key=lambda path: path.relative_to(root).as_posix())


def to_rel(root: Path, paths: list[Path]) -> list[str]:
    return [path.relative_to(root).as_posix() for path in paths]


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def unique(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item and item not in seen:
            seen.add(item)
            result.append(item)
    return result


def add_evidence(bucket: dict[str, list[str]], key: str, evidence: str) -> None:
    bucket.setdefault(key, [])
    if evidence not in bucket[key]:
        bucket[key].append(evidence)


def confidence_from_count(count: int) -> str:
    if count >= 3:
        return "high"
    if count >= 2:
        return "medium"
    return "low"


def parse_package_scripts(root: Path, build_files: list[Path]) -> tuple[list[dict], list[str], list[str], list[str], list[str]]:
    package_scripts: list[dict] = []
    frameworks: list[str] = []
    build_hints: list[str] = []
    test_hints: list[str] = []
    run_hints: list[str] = []

    for path in build_files:
        if path.name != "package.json":
            continue
        try:
            payload = json.loads(read_text(path))
        except json.JSONDecodeError:
            continue
        scripts = payload.get("scripts", {})
        if isinstance(scripts, dict):
            package_scripts.append(
                {
                    "file": path.relative_to(root).as_posix(),
                    "scripts": sorted(str(key) for key in scripts.keys()),
                }
            )
            for name in scripts.keys():
                if name in {"build", "compile"}:
                    build_hints.append(f"npm run {name}")
                if "test" in name:
                    test_hints.append(f"npm run {name}")
                if name in {"start", "dev", "serve", "preview"}:
                    run_hints.append(f"npm run {name}")

        dependencies = payload.get("dependencies", {})
        dev_dependencies = payload.get("devDependencies", {})
        combined = {}
        if isinstance(dependencies, dict):
            combined.update(dependencies)
        if isinstance(dev_dependencies, dict):
            combined.update(dev_dependencies)
        dependency_names = set(combined.keys())
        if "react" in dependency_names:
            frameworks.append("react")
        if "vite" in dependency_names:
            frameworks.append("vite")
        if "vue" in dependency_names:
            frameworks.append("vue")
        if "next" in dependency_names:
            frameworks.append("nextjs")
        if "nuxt" in dependency_names:
            frameworks.append("nuxt")
        if "@govuk-frontend/govuk" in dependency_names or "krds" in " ".join(dependency_names).lower():
            frameworks.append("public-ui-library")

    return package_scripts, unique(frameworks), unique(build_hints), unique(test_hints), unique(run_hints)


def detect_file_path_signals(root: Path, paths: list[Path]) -> dict[str, list[str]]:
    evidence: dict[str, list[str]] = {}
    for path in paths:
        rel = path.relative_to(root).as_posix()
        lowered = rel.lower()
        if "src/main/webapp/web-inf/jsp" in lowered or lowered.endswith(".jsp"):
            add_evidence(evidence, "jsp-webapp", rel)
            add_evidence(evidence, "frontend", rel)
            add_evidence(evidence, "legacy-webmvc", rel)
        if "dispatcher-servlet.xml" in lowered or "servlet-context.xml" in lowered or lowered.endswith("web.xml"):
            add_evidence(evidence, "spring-webmvc", rel)
            add_evidence(evidence, "legacy-webmvc", rel)
            add_evidence(evidence, "api", rel)
        if lowered.endswith("globals.properties"):
            add_evidence(evidence, "egov-globals", rel)
            add_evidence(evidence, "egov-common-component", rel)
        if "tiles" in lowered and lowered.endswith(".xml"):
            add_evidence(evidence, "tiles-layout", rel)
            add_evidence(evidence, "legacy-webmvc", rel)
        if "db/migration" in lowered:
            add_evidence(evidence, "flyway-migration", rel)
            add_evidence(evidence, "data-layer", rel)
        if "/mapper/" in lowered or "/mappers/" in lowered:
            add_evidence(evidence, "mybatis-mapper", rel)
            add_evidence(evidence, "data-layer", rel)
        if "scheduler" in lowered or "schedule" in lowered or "quartz" in lowered:
            add_evidence(evidence, "scheduler", rel)
            add_evidence(evidence, "batch", rel)
        if "src/main/webapp" in lowered and ("/js/" in lowered or "/css/" in lowered or "/images/" in lowered):
            add_evidence(evidence, "shared-asset", rel)
        if any(marker in lowered for marker in ("/common/", "/shared/", "/include/", "/includes/")) and lowered.endswith(
            (".jsp", ".js", ".css", ".tag", ".tagx", ".html")
        ):
            add_evidence(evidence, "shared-asset", rel)
        if any(marker in lowered for marker in ("/com/", "/cmm/", "/cop/", "/uss/", "/sym/")):
            add_evidence(evidence, "egov-common-component", rel)
        if "docker" in lowered or lowered.startswith("k8s/") or lowered.startswith("helm/") or lowered.startswith("charts/"):
            add_evidence(evidence, "deployment", rel)
        if lowered.endswith("jenkinsfile") or ".github/workflows/" in lowered or lowered.endswith(".gitlab-ci.yml"):
            add_evidence(evidence, "ci", rel)
        if "src/main/java" in lowered or "src/main/kotlin" in lowered:
            add_evidence(evidence, "java-source", rel)
        if lowered.endswith("application.yml") or lowered.endswith("application.yaml") or lowered.endswith("application.properties"):
            add_evidence(evidence, "spring-config", rel)
        if lowered.endswith((".jsp", ".html", ".tsx", ".jsx")):
            name = Path(lowered).stem
            if any(token in name for token in ("list", "lst", "grid", "table")):
                add_evidence(evidence, "ui-pattern-list", rel)
            if any(token in name for token in ("detail", "view", "read")):
                add_evidence(evidence, "ui-pattern-detail", rel)
            if any(token in name for token in ("form", "edit", "write", "regist", "register", "modify", "update")):
                add_evidence(evidence, "ui-pattern-form", rel)
            if any(token in name for token in ("upload", "attach", "file")):
                add_evidence(evidence, "ui-pattern-upload", rel)
            if any(token in name for token in ("popup", "modal", "dialog")):
                add_evidence(evidence, "ui-pattern-popup", rel)
            if any(token in name for token in ("search", "find", "filter")):
                add_evidence(evidence, "ui-pattern-search", rel)
    return evidence


def analyze_text_signals(root: Path, paths: list[Path]) -> dict[str, list[str]]:
    evidence: dict[str, list[str]] = {}
    for path in paths[:200]:
        rel = path.relative_to(root).as_posix()
        text = read_text(path)
        lowered = text.lower()
        if not lowered:
            continue

        if "org.egovframe" in lowered or "egovframework" in lowered or "egovabstractserviceimpl" in lowered:
            add_evidence(evidence, "egovframe", rel)
            add_evidence(evidence, "legacy-webmvc", rel)
        if "egovcomabstractdao" in lowered or "egovuserdetailshelper" in lowered or "egovpropertyservice" in lowered:
            add_evidence(evidence, "egov-common-component", rel)
        if "egovfilemngutil" in lowered or "atchfileid" in lowered or "atchmnfl" in lowered:
            add_evidence(evidence, "egov-common-component", rel)
            add_evidence(evidence, "ui-pattern-upload", rel)
        if "globals." in lowered or "globals.properties" in lowered:
            add_evidence(evidence, "egov-globals", rel)
        if "mybatis" in lowered or "sqlsessionfactory" in lowered or "mapperlocations" in lowered:
            add_evidence(evidence, "mybatis", rel)
            add_evidence(evidence, "data-layer", rel)
        if "spring-boot" in lowered:
            add_evidence(evidence, "spring-boot", rel)
            add_evidence(evidence, "api", rel)
        if "@restcontroller" in lowered or "requestmapping" in lowered or "dispatcherServlet".lower() in lowered:
            add_evidence(evidence, "api", rel)
        if "@scheduled" in lowered or "spring batch" in lowered or "jobbuilder" in lowered or "quartz" in lowered:
            add_evidence(evidence, "batch", rel)
            add_evidence(evidence, "scheduler", rel)
        if "kafkalistener" in lowered or "rabbitlistener" in lowered or "mqtt" in lowered or "webhook" in lowered:
            add_evidence(evidence, "receiver", rel)
            add_evidence(evidence, "integration", rel)
        if "resttemplate" in lowered or "webclient" in lowered or "@feignclient" in lowered or "openfeign" in lowered:
            add_evidence(evidence, "integration", rel)
        if "spring-security" in lowered or "securityfilterchain" in lowered or "oauth2" in lowered or "jwt" in lowered:
            add_evidence(evidence, "security", rel)
        if "/actuator/health" in lowered or ("management:" in lowered and "health" in lowered):
            add_evidence(evidence, "health-actuator", rel)
        if "readinessprobe" in lowered or "livenessprobe" in lowered:
            add_evidence(evidence, "health-k8s", rel)
        if "krds" in lowered:
            add_evidence(evidence, "krds", rel)
            add_evidence(evidence, "frontend", rel)
        if "접근성" in lowered or "aria-" in lowered or "role=" in lowered:
            add_evidence(evidence, "accessibility", rel)
        if "tiles" in lowered:
            add_evidence(evidence, "tiles", rel)
            add_evidence(evidence, "tiles-layout", rel)
            add_evidence(evidence, "legacy-webmvc", rel)
        if "paginationinfo" in lowered or "searchcondition" in lowered or "searchkeyword" in lowered:
            add_evidence(evidence, "ui-pattern-search", rel)
            add_evidence(evidence, "ui-pattern-list", rel)
        if "common.js" in lowered or "common.css" in lowered or "layout.jsp" in lowered or "include/header.jsp" in lowered:
            add_evidence(evidence, "shared-asset", rel)
        if "fn_egov_" in lowered or "egovcmmuse" in lowered or "egovframework.com." in lowered:
            add_evidence(evidence, "egov-common-component", rel)
    return evidence


def merge_evidence(*groups: dict[str, list[str]]) -> dict[str, list[str]]:
    merged: dict[str, list[str]] = {}
    for group in groups:
        for key, values in group.items():
            for value in values:
                add_evidence(merged, key, value)
    return merged


def family_candidates(evidence: dict[str, list[str]], frameworks: list[str]) -> list[dict]:
    scores: dict[str, int] = defaultdict(int)
    reasons: dict[str, list[str]] = defaultdict(list)

    def bump(family: str, amount: int, reason: str) -> None:
        scores[family] += amount
        if reason not in reasons[family]:
            reasons[family].append(reason)

    if evidence.get("frontend") or evidence.get("jsp-webapp") or any(name in frameworks for name in {"react", "vue", "nextjs", "vite"}):
        bump("web-app", 2, "UI layer, JSP, or frontend framework hints were detected.")
    if "pwa" in " ".join(frameworks).lower():
        bump("pwa", 2, "PWA-specific framework hints were detected.")
    if evidence.get("api") or evidence.get("spring-boot") or evidence.get("spring-webmvc"):
        bump("backend-service", 3, "API or Spring server hints were detected.")
    if evidence.get("batch"):
        bump("batch-worker", 3, "Batch or scheduler hints were detected.")
    if evidence.get("receiver") or evidence.get("integration"):
        bump("receiver-integration", 2, "Integration receiver or broker hints were detected.")
    if not scores and any(name in frameworks for name in {"react", "vue", "vite"}):
        bump("mockup-local", 1, "Only lightweight frontend signals were detected.")

    ranked = sorted(scores.items(), key=lambda item: (-item[1], item[0]))
    return [
        {
            "id": family,
            "confidence": confidence_from_count(score),
            "reasons": reasons[family],
        }
        for family, score in ranked
    ]


def runtime_role_candidates(evidence: dict[str, list[str]]) -> list[dict]:
    candidates: list[tuple[str, int, list[str]]] = []
    if evidence.get("frontend") or evidence.get("jsp-webapp"):
        candidates.append(("frontend", max(2, len(evidence.get("frontend", []))), ["UI/JSP/frontend signals were detected."]))
    if evidence.get("api"):
        candidates.append(("api", max(2, len(evidence.get("api", []))), ["Spring MVC/Boot API signals were detected."]))
    if evidence.get("batch"):
        candidates.append(("batch", max(2, len(evidence.get("batch", []))), ["Batch or scheduler signals were detected."]))
    if evidence.get("receiver"):
        candidates.append(("receiver", max(2, len(evidence.get("receiver", []))), ["Broker, webhook, or receiver signals were detected."]))
    if not candidates and evidence.get("java-source"):
        candidates.append(("tooling", 1, ["Generic source code was detected but runtime shape is still unclear."]))
    return [
        {"id": role, "confidence": confidence_from_count(score), "reasons": reasons}
        for role, score, reasons in candidates
    ]


def detect_health_hints(evidence: dict[str, list[str]]) -> list[str]:
    hints: list[str] = []
    if evidence.get("health-actuator"):
        hints.append("/actuator/health")
    if evidence.get("health-k8s"):
        hints.append("k8s readiness/liveness probe path requires manual extraction")
    return unique(hints)


def detect_external_integrations(evidence: dict[str, list[str]]) -> list[str]:
    hints: list[str] = []
    if evidence.get("integration"):
        hints.append("HTTP client or external API integration")
    if evidence.get("receiver"):
        hints.append("message broker / webhook / receiver integration")
    return unique(hints)


def detect_scheduler_hints(evidence: dict[str, list[str]]) -> list[str]:
    hints: list[str] = []
    if evidence.get("scheduler"):
        hints.append("scheduler or Quartz-style cadence/ownership review required")
    if evidence.get("batch"):
        hints.append("batch trigger, retry, and re-run path need manual confirmation")
    return unique(hints)


def detect_shared_asset_hints(evidence: dict[str, list[str]]) -> list[str]:
    hints: list[str] = []
    if evidence.get("shared-asset"):
        hints.append("shared JS/CSS/layout/include assets likely affect multiple screens")
    if evidence.get("tiles-layout"):
        hints.append("Tiles/layout template dependency likely affects cross-screen parity")
    return unique(hints)


def detect_public_sector_component_hints(evidence: dict[str, list[str]]) -> list[str]:
    hints: list[str] = []
    if evidence.get("egov-common-component"):
        hints.append("eGovFrame common component or shared module usage requires compatibility review")
    if evidence.get("egov-globals"):
        hints.append("Globals properties/config conventions require environment ownership review")
    if evidence.get("tiles-layout"):
        hints.append("Tiles/layout template structure should be mapped before screen changes")
    return unique(hints)


def detect_ui_pattern_hints(evidence: dict[str, list[str]]) -> list[str]:
    hints: list[str] = []
    mapping = {
        "ui-pattern-search": "search/filter condition pattern",
        "ui-pattern-list": "result list/table pattern",
        "ui-pattern-detail": "detail/read view pattern",
        "ui-pattern-form": "create/edit form pattern",
        "ui-pattern-upload": "attachment/upload pattern",
        "ui-pattern-popup": "popup/modal/dialog pattern",
    }
    for key, label in mapping.items():
        if evidence.get(key):
            hints.append(label)
    return unique(hints)


def detect_build_command_hints(build_files: list[Path], evidence: dict[str, list[str]], package_builds: list[str], package_tests: list[str], package_runs: list[str]) -> tuple[list[str], list[str], list[str]]:
    build_hints = list(package_builds)
    test_hints = list(package_tests)
    run_hints = list(package_runs)

    rel_files = {path.name for path in build_files}
    rel_paths = {path.as_posix() for path in build_files}

    if {"build.gradle", "build.gradle.kts", "settings.gradle", "settings.gradle.kts", "gradlew"} & rel_files:
        build_hints.append("./gradlew build")
        test_hints.append("./gradlew test")
        if evidence.get("spring-boot"):
            run_hints.append("./gradlew bootRun")
    if {"pom.xml", "mvnw"} & rel_files:
        build_hints.append("mvn package")
        test_hints.append("mvn test")
        if evidence.get("spring-boot"):
            run_hints.append("mvn spring-boot:run")
    if "pubspec.yaml" in rel_files:
        build_hints.append("flutter build <target>")
        test_hints.append("flutter test")
        run_hints.append("flutter run")
    if "manifest.json" in rel_files and any("Packages/manifest.json" in path for path in rel_paths):
        run_hints.append("Unity editor or batchmode validation")

    return unique(build_hints), unique(test_hints), unique(run_hints)


def public_sector_signals(evidence: dict[str, list[str]]) -> dict:
    egov_evidence = unique(evidence.get("egovframe", []) + evidence.get("legacy-webmvc", []))
    krds_evidence = unique(evidence.get("krds", []) + evidence.get("accessibility", []))
    return {
        "eGovFrameLikely": {
            "value": bool(egov_evidence),
            "confidence": confidence_from_count(len(egov_evidence)) if egov_evidence else "low",
            "evidence": egov_evidence,
        },
        "krdsOrPublicUiLikely": {
            "value": bool(krds_evidence),
            "confidence": confidence_from_count(len(krds_evidence)) if krds_evidence else "low",
            "evidence": krds_evidence,
        },
        "legacyWebMvcLikely": {
            "value": bool(evidence.get("legacy-webmvc")),
            "confidence": confidence_from_count(len(evidence.get("legacy-webmvc", []))) if evidence.get("legacy-webmvc") else "low",
            "evidence": evidence.get("legacy-webmvc", []),
        },
    }


def suggested_constraint_mode(signals: dict) -> str:
    if signals["eGovFrameLikely"]["value"] or signals["legacyWebMvcLikely"]["value"]:
        return "legacy-maintenance"
    return "recommended-baseline"


def recommended_roles(inventory: dict) -> dict:
    required = [
        "orchestrator",
        "legacy-analyst",
        "migration-planner",
        "runtime-engineer",
        "qa-validator",
        "docs-operator",
    ]
    optional = [
        "release-manager",
        "failure-curator",
    ]
    reasons: list[str] = []

    if inventory["migrationPaths"] or inventory["dataLayerHints"]:
        required.append("data-steward")
        reasons.append("DB, migration, or mapper ownership signals were detected.")
    if inventory["securityHints"] or inventory["publicSectorSignals"]["eGovFrameLikely"]["value"]:
        required.append("security-reviewer")
        reasons.append("Security or public-sector auth/compliance signals were detected.")
    if inventory["publicSectorSignals"]["eGovFrameLikely"]["value"] or inventory["publicSectorSignals"]["legacyWebMvcLikely"]["value"]:
        optional.append("compatibility-reviewer")
        optional.append("refactor-guardian")
        reasons.append("Legacy eGovFrame / Spring MVC compatibility risk is likely.")
    if inventory["sharedAssetHints"] or inventory["publicSectorComponentHints"] or inventory["uiPatternHints"]:
        optional.append("compatibility-reviewer")
        optional.append("refactor-guardian")
        reasons.append("Shared public-sector assets/components suggest wide screen-level blast radius.")
    if inventory["deploymentFiles"] or inventory["ciFiles"]:
        optional.append("cutover-manager")
        reasons.append("Deployment or CI artifacts suggest rollout/cutover coordination.")
    if inventory["externalIntegrationHints"]:
        optional.append("solution-architect")
        reasons.append("External integration hints suggest contract and boundary review.")

    required = unique(required)
    optional = [role for role in unique(optional) if role not in required]

    coordination_mode = "coordinated"
    if "cutover-manager" in optional and ("release-manager" in optional or "data-steward" in required):
        coordination_mode = "full"

    return {
        "sourceProjectFamilyCandidates": inventory["projectFamilyCandidates"],
        "runtimeRoleCandidates": inventory["runtimeRoleCandidates"],
        "requiredAgentRoles": required,
        "optionalAgentRoles": optional,
        "suggestedConstraintMode": inventory["suggestedConstraintMode"],
        "recommendedCoordinationMode": coordination_mode,
        "reasons": unique(reasons),
    }


def build_docs_gap_report(inventory: dict) -> str:
    existing_docs = set(inventory["docFiles"])
    gaps: list[str] = []
    public_sector_gaps: list[str] = []

    if "README.md" not in existing_docs:
        gaps.append("루트 README가 없거나 충분히 확인되지 않았다.")
    if not any(path.endswith("build-guide.md") for path in existing_docs):
        gaps.append("실제 build/run/test 명령을 정리한 build guide가 보이지 않는다.")
    if inventory["deploymentFiles"] and not any(path.endswith("deployment-checklist.md") for path in existing_docs):
        gaps.append("배포 산출물이 있지만 deployment checklist가 보이지 않는다.")
    if (inventory["deploymentFiles"] or "batch" in {role["id"] for role in inventory["runtimeRoleCandidates"]}) and not any(
        path.endswith("operations-manual.md") or path.endswith("runbook.md") for path in existing_docs
    ):
        gaps.append("운영/장애 대응 문서가 부족해 보인다.")
    if inventory["migrationPaths"] and not any(path.endswith("impact-analysis.md") for path in existing_docs):
        gaps.append("DB 또는 migration 흔적이 있지만 impact-analysis 문서가 보이지 않는다.")
    if inventory["publicSectorSignals"]["eGovFrameLikely"]["value"]:
        public_sector_gaps.append("eGovFrame/legacy 유지 제약을 정리한 compatibility matrix 또는 legacy exception note가 필요하다.")
        public_sector_gaps.append("parity validation과 rollback 기준을 일반 프로젝트보다 먼저 적는 편이 안전하다.")
    if inventory["publicSectorSignals"]["krdsOrPublicUiLikely"]["value"] or any(role["id"] == "frontend" for role in inventory["runtimeRoleCandidates"]):
        public_sector_gaps.append("KRDS 적합성, 접근성, 공공형 폼/목록/첨부파일 패턴 점검 문서를 별도로 두는 편이 좋다.")
    if inventory["sharedAssetHints"] or inventory["publicSectorComponentHints"]:
        public_sector_gaps.append("공통 JS/CSS, layout, include, 공통컴포넌트 의존 지도를 먼저 남기면 화면 영향 범위 파악이 빨라진다.")
    if inventory["uiPatternHints"]:
        public_sector_gaps.append("검색조건/목록/상세/등록/첨부파일 같은 대표 화면 패턴 catalog를 먼저 정리하면 migration 검토가 쉬워진다.")

    lines = [
        "# Docs Gap Report",
        "",
        f"- Repository root: `{inventory['repositoryRoot']}`",
        f"- Suggested constraint mode: `{inventory['suggestedConstraintMode']}`",
        f"- Project family candidates: {', '.join(candidate['id'] for candidate in inventory['projectFamilyCandidates']) or '-'}",
        "",
        "## Existing Docs",
        "",
    ]
    if inventory["docFiles"]:
        lines.extend(f"- `{path}`" for path in inventory["docFiles"])
    else:
        lines.append("- 없음")

    lines.extend(["", "## Likely Missing Or Incomplete Docs", ""])
    if gaps:
        lines.extend(f"- {gap}" for gap in gaps)
    else:
        lines.append("- 기본 문서 gap은 적어 보인다. 그래도 실제 명령과 운영 절차는 수동 확인이 필요하다.")

    lines.extend(["", "## Public-Sector / eGov Notes", ""])
    if public_sector_gaps:
        lines.extend(f"- {gap}" for gap in public_sector_gaps)
    else:
        lines.append("- 별도 공공 특화 문서 gap은 강하게 감지되지 않았다.")

    lines.extend(["", "## Manual Follow-Up", ""])
    lines.extend(f"- {item}" for item in inventory["needsManualReview"])
    return "\n".join(lines) + "\n"


def analyze(root: Path) -> tuple[dict, str, dict]:
    build_files = glob_files(root, BUILD_PATTERNS)
    config_files = glob_files(root, CONFIG_PATTERNS)
    doc_files = glob_files(root, DOC_PATTERNS)
    ci_files = glob_files(root, CI_PATTERNS)
    deployment_files = glob_files(root, DEPLOYMENT_PATTERNS)
    migration_paths = glob_files(root, MIGRATION_PATTERNS)
    entrypoint_files = glob_files(root, ENTRYPOINT_PATTERNS)
    code_files = glob_files(root, CODE_PATTERNS)

    path_evidence = detect_file_path_signals(
        root,
        unique(build_files + config_files + ci_files + deployment_files + migration_paths + entrypoint_files + code_files),
    )
    text_evidence = analyze_text_signals(root, unique(build_files + config_files + ci_files + deployment_files + code_files))
    evidence = merge_evidence(path_evidence, text_evidence)

    languages: list[str] = []
    if any(path.name == "package.json" for path in build_files):
        languages.append("TypeScript/JavaScript")
    if any(path.name in {"build.gradle", "build.gradle.kts", "pom.xml"} for path in build_files):
        languages.append("Java/Kotlin")
    if any(path.name == "pubspec.yaml" for path in build_files):
        languages.append("Dart")
    if any(path.as_posix().endswith("Packages/manifest.json") for path in build_files):
        languages.append("C#")
    if evidence.get("jsp-webapp"):
        languages.append("JSP/Servlet")

    package_scripts, package_frameworks, package_builds, package_tests, package_runs = parse_package_scripts(root, build_files)

    frameworks: list[str] = []
    if any(path.name in {"build.gradle", "build.gradle.kts", "pom.xml"} for path in build_files):
        frameworks.append("java-app")
    if any(path.name == "package.json" for path in build_files):
        frameworks.append("node-app")
    frameworks.extend(package_frameworks)
    if evidence.get("spring-boot"):
        frameworks.append("spring-boot")
    if evidence.get("spring-webmvc"):
        frameworks.append("spring-webmvc")
    if evidence.get("egovframe"):
        frameworks.append("egovframe")
    if evidence.get("mybatis"):
        frameworks.append("mybatis")
    if evidence.get("tiles"):
        frameworks.append("tiles")
    if evidence.get("jsp-webapp"):
        frameworks.append("jsp-webapp")

    build_command_hints, test_command_hints, run_command_hints = detect_build_command_hints(
        build_files,
        evidence,
        package_builds,
        package_tests,
        package_runs,
    )

    inventory = {
        "repositoryRoot": str(root.resolve()),
        "repositoryName": root.name,
        "buildFiles": to_rel(root, build_files),
        "configFiles": to_rel(root, config_files),
        "docFiles": to_rel(root, doc_files),
        "ciFiles": to_rel(root, ci_files),
        "deploymentFiles": to_rel(root, deployment_files),
        "migrationPaths": to_rel(root, migration_paths),
        "entrypointHints": to_rel(root, entrypoint_files),
        "detectedLanguages": unique(languages),
        "detectedFrameworkHints": unique(frameworks),
        "projectFamilyCandidates": family_candidates(evidence, unique(frameworks)),
        "runtimeRoleCandidates": runtime_role_candidates(evidence),
        "packageScripts": package_scripts,
        "buildCommandHints": build_command_hints,
        "testCommandHints": test_command_hints,
        "runCommandHints": run_command_hints,
        "healthEndpointHints": detect_health_hints(evidence),
        "externalIntegrationHints": detect_external_integrations(evidence),
        "schedulerHints": detect_scheduler_hints(evidence),
        "sharedAssetHints": detect_shared_asset_hints(evidence),
        "publicSectorComponentHints": detect_public_sector_component_hints(evidence),
        "uiPatternHints": detect_ui_pattern_hints(evidence),
        "dataLayerHints": unique(
            [
                "mybatis" if evidence.get("mybatis") else "",
                "mapper-xml" if evidence.get("mybatis-mapper") else "",
                "flyway-style migration" if evidence.get("flyway-migration") else "",
            ]
        ),
        "securityHints": unique(
            [
                "spring-security or auth configuration" if evidence.get("security") else "",
                "legacy auth/security layer needs manual review" if evidence.get("egovframe") else "",
            ]
        ),
        "publicSectorSignals": public_sector_signals(evidence),
        "suggestedConstraintMode": suggested_constraint_mode(public_sector_signals(evidence)),
        "needsManualReview": [
            "real build/test/smoke commands and required parameters",
            "deployment order, rollback step, and environment approvals",
            "DB ownership, migration ownership, and verification SQL",
            "secret injection, profile split, and 운영 config source of truth",
            "public-sector parity scope, accessibility baseline, and KRDS/UI-UX fit when relevant",
        ],
    }

    docs_gap_report = build_docs_gap_report(inventory)
    role_recommendation = recommended_roles(inventory)
    return inventory, docs_gap_report, role_recommendation


def main() -> int:
    args = parse_args()
    root = Path(args.repo).resolve()
    inventory, docs_gap_report, role_recommendation = analyze(root)

    inventory_output = Path(args.output).resolve() if args.output else root / ".agent-base" / "repository-inventory.json"
    docs_gap_output = (
        Path(args.docs_gap_output).resolve() if args.docs_gap_output else root / ".agent-base" / "docs-gap-report.md"
    )
    role_output = (
        Path(args.role_output).resolve() if args.role_output else root / ".agent-base" / "role-recommendation.json"
    )

    inventory_output.parent.mkdir(parents=True, exist_ok=True)
    docs_gap_output.parent.mkdir(parents=True, exist_ok=True)
    role_output.parent.mkdir(parents=True, exist_ok=True)

    inventory_output.write_text(json.dumps(inventory, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    docs_gap_output.write_text(docs_gap_report, encoding="utf-8")
    role_output.write_text(json.dumps(role_recommendation, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(
        json.dumps(
            {
                "inventory": str(inventory_output),
                "docsGapReport": str(docs_gap_output),
                "roleRecommendation": str(role_output),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
