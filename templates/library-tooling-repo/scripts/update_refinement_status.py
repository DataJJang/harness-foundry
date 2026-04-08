#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path

from generate_project import derive_refinement_status, sync_agent_workboard_with_refinement
from state_io import coordination_lock, default_lock_path, load_json, save_json, write_text_atomic


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST_PATH = REPO_ROOT / ".agent-base" / "refinement-manifest.json"
DEFAULT_STATUS_PATH = REPO_ROOT / ".agent-base" / "refinement-status.json"
DEFAULT_OVERRIDES_PATH = REPO_ROOT / "docs" / "ai" / "repo-local-overrides.md"
DEFAULT_WORKBOARD_PATH = REPO_ROOT / ".agent-base" / "agent-workboard.json"
DEFAULT_LOCK_PATH = default_lock_path(DEFAULT_STATUS_PATH)

STATUS_CHOICES = ["pending", "resolved", "kept-default", "deferred"]
DECISION_MODE_BY_STATUS = {
    "pending": "undecided",
    "resolved": "decide-now",
    "kept-default": "keep-default",
    "deferred": "defer-with-note",
}
PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Update refinement follow-up status for a generated repository.")
    parser.add_argument("--manifest-path", default=str(DEFAULT_MANIFEST_PATH), help="Path to refinement-manifest.json")
    parser.add_argument("--status-path", default=str(DEFAULT_STATUS_PATH), help="Path to refinement-status.json")
    parser.add_argument("--overrides-path", default=str(DEFAULT_OVERRIDES_PATH), help="Path to repo-local-overrides.md")
    parser.add_argument("--workboard-path", default=str(DEFAULT_WORKBOARD_PATH), help="Path to agent-workboard.json")
    parser.add_argument("--lock-path", default=str(DEFAULT_LOCK_PATH), help="Path to the shared coordination lock file")
    parser.add_argument("--lock-timeout-seconds", type=float, default=10.0, help="How long to wait for the coordination lock")
    parser.add_argument("--module", help="Module id to update")
    parser.add_argument("--status", choices=STATUS_CHOICES, help="New status value")
    parser.add_argument("--decision-mode", help="Override decision mode")
    parser.add_argument("--notes", help="Decision or implementation notes")
    parser.add_argument("--deferred-reason", help="Reason for deferring the module")
    parser.add_argument("--resolver", help="Owner or future resolver")
    parser.add_argument("--list", action="store_true", help="List current refinement modules and exit")
    parser.add_argument("--show-snippet", action="store_true", help="Print a repo-local-overrides snippet after updating")
    parser.add_argument(
        "--append-to-overrides",
        action="store_true",
        help="Append or update the decision snippet inside repo-local-overrides.md",
    )
    parser.add_argument("--interactive", action="store_true", help="Prompt for the next pending module interactively")
    return parser.parse_args()


def maybe_sync_workboard(workboard_path: Path, status: dict) -> bool:
    if not workboard_path.exists():
        return False
    workboard = load_json(workboard_path)
    sync_agent_workboard_with_refinement(workboard, status)
    save_json(workboard_path, workboard)
    return True


def status_from_manifest(manifest: dict) -> dict:
    spec_stub = {
        "repositoryName": manifest["repositoryName"],
        "projectFamily": manifest["projectFamily"],
    }
    return derive_refinement_status(spec_stub, manifest)


def ensure_status(manifest: dict, status_path: Path) -> dict:
    if status_path.exists():
        return load_json(status_path)
    status = status_from_manifest(manifest)
    save_json(status_path, status)
    return status


def sorted_modules(modules: list[dict]) -> list[dict]:
    return sorted(modules, key=lambda module: (PRIORITY_ORDER.get(module["priority"], 9), module["id"]))


def list_modules(manifest: dict, status: dict) -> None:
    manifest_by_id = {module["id"]: module for module in manifest["modules"]}
    print("Refinement modules:")
    for module in sorted_modules(status["modules"]):
        manifest_module = manifest_by_id[module["id"]]
        print(
            f"- {module['id']} [{module['priority']}] "
            f"status={module['status']} decision={module['decisionMode']} "
            f"title={module['title']}"
        )
        print(f"  trigger: {manifest_module['triggerReason']}")
        print(f"  outputs: {', '.join(module['recommendedOutputs'])}")


def find_status_module(status: dict, module_id: str) -> dict:
    for module in status["modules"]:
        if module["id"] == module_id:
            return module
    raise SystemExit(f"Unknown module id: {module_id}")


def next_pending_module(status: dict) -> dict | None:
    pending = [module for module in status["modules"] if module["status"] == "pending"]
    if not pending:
        return None
    return sorted_modules(pending)[0]


def ask(prompt: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    raw = input(f"{prompt}{suffix}: ").strip()
    return raw or default


def prompt_status(current: str) -> str:
    print("Select module outcome:")
    print("1. resolved")
    print("2. kept-default")
    print("3. deferred")
    print("4. pending")
    mapping = {
        "1": "resolved",
        "2": "kept-default",
        "3": "deferred",
        "4": "pending",
        "resolved": "resolved",
        "kept-default": "kept-default",
        "deferred": "deferred",
        "pending": "pending",
    }
    while True:
        choice = ask("Outcome", current or "pending").lower()
        if choice in mapping:
            return mapping[choice]
        print("Choose one of: resolved, kept-default, deferred, pending")


def update_module(
    module: dict,
    new_status: str,
    decision_mode: str | None,
    notes: str,
    deferred_reason: str,
    resolver: str,
) -> None:
    module["status"] = new_status
    module["decisionMode"] = decision_mode or DECISION_MODE_BY_STATUS[new_status]
    module["notes"] = notes
    module["resolver"] = resolver
    module["lastUpdated"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    if new_status == "deferred":
        module["deferredReason"] = deferred_reason
    else:
        module["deferredReason"] = ""


def recompute_summary(status: dict) -> None:
    pending = [module["id"] for module in status["modules"] if module["status"] == "pending"]
    resolved = [module["id"] for module in status["modules"] if module["status"] in {"resolved", "kept-default"}]
    deferred = [module["id"] for module in status["modules"] if module["status"] == "deferred"]
    high_priority_pending = [
        module["id"] for module in status["modules"] if module["priority"] == "high" and module["status"] == "pending"
    ]
    status["summary"]["pendingModuleIds"] = pending
    status["summary"]["highPriorityPendingModuleIds"] = high_priority_pending
    status["summary"]["resolvedModuleIds"] = resolved
    status["summary"]["deferredModuleIds"] = deferred


def render_snippet(manifest_module: dict, status_module: dict) -> str:
    lines = [
        f"## Decision Log: {status_module['title']} `{status_module['id']}`",
        "",
        f"- Status: `{status_module['status']}`",
        f"- Decision mode: `{status_module['decisionMode']}`",
        f"- Updated: `{status_module['lastUpdated'] or '-'}`",
        f"- Owner or resolver: `{status_module['resolver'] or '-'}`",
        "",
        "Notes:",
        f"- {status_module['notes'] or '-'}",
    ]
    if status_module["status"] == "deferred":
        lines.extend(
            [
                "",
                "Deferred reason:",
                f"- {status_module['deferredReason'] or '-'}",
            ]
        )
    lines.extend(
        [
            "",
            "Recommended outputs to update next:",
        ]
    )
    for output in manifest_module["recommendedOutputs"]:
        lines.append(f"- {output}")
    return "\n".join(lines)


def upsert_overrides_snippet(path: Path, module_id: str, snippet: str) -> None:
    start_marker = f"<!-- refinement-log:{module_id}:start -->"
    end_marker = f"<!-- refinement-log:{module_id}:end -->"
    wrapped_snippet = f"{start_marker}\n{snippet}\n{end_marker}"

    if path.exists():
        text = path.read_text(encoding="utf-8")
    else:
        text = (
            "# Repo-Local Overrides\n\n"
            "## Automated Decision Logs\n\n"
        )

    pattern = re.compile(
        re.escape(start_marker) + r".*?" + re.escape(end_marker),
        re.DOTALL,
    )
    if pattern.search(text):
        updated = pattern.sub(wrapped_snippet, text)
    else:
        suffix = "" if text.endswith("\n") else "\n"
        updated = text + suffix + "\n" + wrapped_snippet + "\n"

    write_text_atomic(path, updated)


def interactive_update(manifest: dict, status: dict) -> dict | None:
    module = next_pending_module(status)
    if not module:
        print("No pending refinement modules remain.")
        return None

    manifest_module = next(item for item in manifest["modules"] if item["id"] == module["id"])
    print(f"Next module: {module['id']} [{module['priority']}] {module['title']}")
    print(f"Trigger: {manifest_module['triggerReason']}")
    print("Questions:")
    for question in manifest_module["questions"]:
        print(f"- {question}")
    print("Recommended outputs:")
    for output in module["recommendedOutputs"]:
        print(f"- {output}")

    new_status = prompt_status(module["status"])
    notes = ask("Notes", module["notes"])
    resolver = ask("Owner or resolver", module["resolver"])
    deferred_reason = ""
    if new_status == "deferred":
        deferred_reason = ask("Deferred reason", module["deferredReason"])

    update_module(
        module=module,
        new_status=new_status,
        decision_mode=None,
        notes=notes,
        deferred_reason=deferred_reason,
        resolver=resolver,
    )
    recompute_summary(status)
    return module


def main() -> int:
    args = parse_args()
    manifest_path = Path(args.manifest_path).expanduser().resolve()
    status_path = Path(args.status_path).expanduser().resolve()
    overrides_path = Path(args.overrides_path).expanduser().resolve()
    workboard_path = Path(args.workboard_path).expanduser().resolve()
    lock_path = Path(args.lock_path).expanduser().resolve()

    with coordination_lock(lock_path, timeout_seconds=args.lock_timeout_seconds):
        manifest = load_json(manifest_path)
        status = ensure_status(manifest, status_path)
        manifest_by_id = {module["id"]: module for module in manifest["modules"]}

        if args.list:
            list_modules(manifest, status)
            return 0

        updated_module: dict | None = None
        if args.interactive:
            updated_module = interactive_update(manifest, status)
            if updated_module is None:
                return 0
        else:
            if not args.module or not args.status:
                raise SystemExit("Use --interactive or provide both --module and --status.")
            status_module = find_status_module(status, args.module)
            update_module(
                module=status_module,
                new_status=args.status,
                decision_mode=args.decision_mode,
                notes=args.notes or status_module["notes"],
                deferred_reason=args.deferred_reason or status_module["deferredReason"],
                resolver=args.resolver or status_module["resolver"],
            )
            recompute_summary(status)
            updated_module = status_module

        save_json(status_path, status)
        workboard_updated = maybe_sync_workboard(workboard_path, status)
        next_module = next_pending_module(status)
        snippet = render_snippet(manifest_by_id[updated_module["id"]], updated_module)
        overrides_written = False
        if args.append_to_overrides:
            upsert_overrides_snippet(overrides_path, updated_module["id"], snippet)
            overrides_written = True

    response = {
        "updatedModule": updated_module["id"],
        "statusPath": str(status_path),
        "overridesPath": str(overrides_path),
        "workboardPath": str(workboard_path),
        "lockPath": str(lock_path),
        "overridesUpdated": overrides_written,
        "workboardUpdated": workboard_updated,
        "moduleStatus": updated_module["status"],
        "decisionMode": updated_module["decisionMode"],
        "nextPendingModule": next_module["id"] if next_module else None,
        "highPriorityPendingModuleIds": status["summary"]["highPriorityPendingModuleIds"],
    }
    print(json.dumps(response, ensure_ascii=False))

    if args.show_snippet or args.interactive:
        print()
        print(snippet)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
