#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from generate_project import COORDINATION_MODE_LABELS
from state_io import load_json


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONTEXT_PATH = REPO_ROOT / ".agent-base" / "context-manifest.json"
DEFAULT_REFINEMENT_STATUS_PATH = REPO_ROOT / ".agent-base" / "refinement-status.json"
DEFAULT_WORKBOARD_PATH = REPO_ROOT / ".agent-base" / "agent-workboard.json"
DEFAULT_GENERATION_MANIFEST_PATH = REPO_ROOT / ".agent-base" / "generation-manifest.json"

ESCALATION_HINTS = {
    "lite": "shared ownership, data/security coordination, or release risk becomes part of the normal path.",
    "coordinated": "production/release ownership, monorepo or multi-repo planning, or always-on side-lane coordination becomes the default.",
    "full": "the repo no longer needs heavy DB, security, release, or multi-lane coordination as part of everyday execution.",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Show the current mode-aware starter path for a generated repository."
    )
    parser.add_argument(
        "--context-manifest-path",
        default=str(DEFAULT_CONTEXT_PATH),
        help="Path to context-manifest.json",
    )
    parser.add_argument(
        "--refinement-status-path",
        default=str(DEFAULT_REFINEMENT_STATUS_PATH),
        help="Path to refinement-status.json",
    )
    parser.add_argument(
        "--workboard-path",
        default=str(DEFAULT_WORKBOARD_PATH),
        help="Path to agent-workboard.json",
    )
    parser.add_argument(
        "--generation-manifest-path",
        default=str(DEFAULT_GENERATION_MANIFEST_PATH),
        help="Path to generation-manifest.json",
    )
    parser.add_argument("--json", action="store_true", help="Print the starter path as JSON")
    return parser.parse_args()


def load_optional_json(path: Path) -> dict | None:
    if not path.exists():
        return None
    return load_json(path)


def relative_to_repo(path: Path, repo_root: Path) -> str:
    try:
        return str(path.relative_to(repo_root))
    except ValueError:
        return str(path)


def resolve_repo_root(context_path: Path) -> Path:
    if context_path.parent.name == ".agent-base":
        return context_path.parent.parent
    return context_path.parent


def find_lane(workboard: dict | None, lane_id: str) -> dict | None:
    if not workboard:
        return None
    for lane in workboard.get("workLanes", []):
        if lane.get("id") == lane_id:
            return lane
    return None


def latest_packet_path(workboard: dict | None) -> str:
    if not workboard:
        return ""
    design_lane = find_lane(workboard, "design-freeze")
    if design_lane and design_lane.get("latestPacketPath"):
        return design_lane["latestPacketPath"]
    for lane in workboard.get("workLanes", []):
        if lane.get("latestPacketPath"):
            return lane["latestPacketPath"]
    return ""


def minimal_entry_files(mode: str) -> list[str]:
    if mode == "lite":
        return [
            "AGENTS.md",
            ".agent-base/context-manifest.json",
            "docs/ai/command-catalog.md",
        ]
    if mode == "coordinated":
        return [
            "AGENTS.md",
            ".agent-base/context-manifest.json",
            ".agent-base/refinement-manifest.json",
            ".agent-base/agent-workboard.json",
        ]
    return [
        "AGENTS.md",
        ".agent-base/context-manifest.json",
        ".agent-base/agent-role-plan.json",
        ".agent-base/agent-workboard.json",
    ]


def make_action(
    title: str,
    why: str,
    *,
    files: list[str] | None = None,
    command: str | None = None,
    note: str | None = None,
) -> dict:
    return {
        "title": title,
        "why": why,
        "files": list(files or []),
        "command": command or "",
        "note": note or "",
    }


def build_actions(mode: str, state: dict) -> list[dict]:
    actions = [
        make_action(
            "Review the minimal entry files",
            "Start from the lightest doc set that still matches the current coordination cost.",
            files=minimal_entry_files(mode),
        )
    ]

    blocking = list(state["blockingHighPriorityModules"])
    next_lane = state["nextSuggestedLaneId"]
    latest_packet = state["latestPacketPath"]
    design_lane_status = state["designFreezeStatus"]

    if blocking:
        actions.append(
            make_action(
                "Resolve the blocking refinement modules",
                "High-priority refinement should be cleared before widening implementation scope.",
                files=[
                    ".agent-base/refinement-manifest.json",
                    ".agent-base/refinement-status.json",
                    "docs/ai/repo-local-overrides.md",
                ],
                command="python3 scripts/update_refinement_status.py --interactive --append-to-overrides",
                note="Pending high-priority modules: " + ", ".join(blocking),
            )
        )
        if mode == "lite":
            actions.append(
                make_action(
                    "Align commands and prove the first runnable path",
                    "Lite mode should validate a real build/test/smoke path before opening heavier coordination flow.",
                    files=[
                        "docs/ai/command-catalog.md",
                        ".agent-base/pre-commit-config.json",
                        "docs/ai/repo-local-overrides.md",
                    ],
                    note="Use the real repository build/test/smoke commands from docs/ai/command-catalog.md.",
                )
            )
        elif mode == "coordinated":
            actions.append(
                make_action(
                    "Prepare the first execution lane while blockers are clearing",
                    "Keep the next lane boundary stable so `--finalize-design-freeze` is a small step after refinement closes.",
                    files=[
                        ".agent-base/agent-workboard.json",
                        "docs/ai/architecture-map.md",
                        "docs/ai/command-catalog.md",
                    ],
                    note=f"Current next suggested lane: {next_lane or 'none yet'}.",
                )
            )
        else:
            actions.append(
                make_action(
                    "Confirm role boundaries before shared execution widens",
                    "Full mode depends on explicit owners, owned paths, and delivery expectations before work spreads out.",
                    files=[
                        ".agent-base/agent-role-plan.json",
                        ".agent-base/agent-workboard.json",
                        "docs/ai/repo-local-overrides.md",
                    ],
                    note=f"Current next suggested lane: {next_lane or 'none yet'}.",
                )
            )
        return actions

    if mode == "lite":
        actions.append(
            make_action(
                "Align the repo-local command and hook settings",
                "The first runnable path should be reflected in command-catalog and pre-commit before deeper coordination appears.",
                files=[
                    "docs/ai/command-catalog.md",
                    ".agent-base/pre-commit-config.json",
                    "docs/ai/repo-local-overrides.md",
                ],
            )
        )
        actions.append(
            make_action(
                "Run the first build, test, or smoke validation",
                "Lite mode is ready once the repository can prove one real validation path and capture any remaining gap.",
                files=[
                    "docs/ai/command-catalog.md",
                    "checklists/project-creation.md",
                    "checklists/first-delivery.md",
                ],
                note="If DB/security/shared ownership appears during validation, move up to Coordinated.",
            )
        )
        return actions

    if design_lane_status != "completed":
        actions.append(
            make_action(
                "Freeze the first execution handoff",
                "With blockers cleared, the next useful step is a deterministic packet for the first runner.",
                files=[
                    ".agent-base/agent-workboard.json",
                    "docs/ai/agent-handoff-log.md",
                    "docs/ai/handoff-packets",
                ],
                command="python3 scripts/update_agent_workboard.py --finalize-design-freeze",
                note=f"Target lane: {next_lane or 'runtime-implementation'}",
            )
        )
        actions.append(
            make_action(
                "Validate packet freshness before shared execution",
                "The first shared runner should start from a fresh packet, not from stale planning notes.",
                files=[
                    ".agent-base/agent-workboard.json",
                    "docs/ai/agent-handoff-log.md",
                ],
                command="python3 scripts/update_agent_workboard.py --check-packets --strict",
                note=(
                    f"Current packet path: {latest_packet}."
                    if latest_packet
                    else "Run this right after `--finalize-design-freeze` creates the first packet."
                ),
            )
        )
        return actions

    actions.append(
        make_action(
            "Validate packet freshness",
            "Keep the current execution contract fresh before the next owner or lane starts from it.",
            files=[
                ".agent-base/agent-workboard.json",
                "docs/ai/agent-handoff-log.md",
            ],
            command="python3 scripts/update_agent_workboard.py --check-packets --strict",
            note=f"Current packet path: {latest_packet or '-'}",
        )
    )

    if mode == "coordinated":
        actions.append(
            make_action(
                "Start the next lane from the packet and keep baton history current",
                "Coordinated mode keeps one shared contract and only adds handoff history when scope or owner changes.",
                files=[
                    latest_packet or ".agent-base/agent-workboard.json",
                    ".agent-base/agent-workboard.json",
                    "docs/ai/agent-handoff-log.md",
                ],
                command="python3 scripts/update_agent_workboard.py --interactive --append-handoff",
                note=f"Suggested lane: {next_lane or 'review agent-workboard summary'}.",
            )
        )
    else:
        actions.append(
            make_action(
                "Keep lane state, handoff notes, and release-facing docs in sync",
                "Full mode should treat shared execution state as a living contract while implementation starts.",
                files=[
                    latest_packet or ".agent-base/agent-workboard.json",
                    ".agent-base/agent-role-plan.json",
                    "docs/ai/agent-handoff-log.md",
                    "docs/ai/repo-local-overrides.md",
                ],
                command="python3 scripts/update_agent_workboard.py --interactive --append-handoff",
                note=f"Suggested lane: {next_lane or 'review agent-workboard summary'}.",
            )
        )
    return actions


def build_report(
    repo_root: Path,
    context_manifest: dict,
    refinement_status: dict | None,
    workboard: dict | None,
    generation_manifest: dict | None,
) -> dict:
    mode = context_manifest.get("recommendedCoordinationMode") or (
        generation_manifest or {}
    ).get("recommendedCoordinationMode", "lite")
    summary = context_manifest.get("coordinationModeSummary") or (
        generation_manifest or {}
    ).get("coordinationModeSummary", "")
    reasons = list(context_manifest.get("coordinationModeReasons", [])) or list(
        (generation_manifest or {}).get("coordinationModeReasons", [])
    )

    blocking = []
    if refinement_status:
        blocking = list(refinement_status.get("summary", {}).get("highPriorityPendingModuleIds", []))
    elif workboard:
        blocking = list(workboard.get("summary", {}).get("blockingHighPriorityModuleIds", []))
    elif generation_manifest:
        blocking = list(generation_manifest.get("highPriorityRefinementModuleIds", []))

    design_lane = find_lane(workboard, "design-freeze")
    next_lane = None
    design_ready = not blocking
    if workboard:
        design_ready = bool(workboard.get("summary", {}).get("designReady", design_ready))
        next_lane = workboard.get("summary", {}).get("nextSuggestedLaneId")

    state = {
        "repoRoot": relative_to_repo(repo_root, repo_root),
        "blockingHighPriorityModules": blocking,
        "designReady": design_ready,
        "designFreezeStatus": design_lane.get("status", "-") if design_lane else "-",
        "nextSuggestedLaneId": next_lane or "",
        "latestPacketPath": latest_packet_path(workboard),
    }

    return {
        "mode": mode,
        "label": COORDINATION_MODE_LABELS.get(mode, mode),
        "summary": summary,
        "reasons": reasons,
        "state": state,
        "actions": build_actions(mode, state),
        "escalateWhen": ESCALATION_HINTS.get(mode, ""),
    }


def print_report(report: dict) -> None:
    print("Starter Path")
    print(f"- Mode: {report['label']}")
    print(f"- Summary: {report['summary']}")
    print(
        "- Blocking high-priority refinement modules: "
        + (", ".join(report["state"]["blockingHighPriorityModules"]) or "none")
    )
    print(f"- Design ready: {'yes' if report['state']['designReady'] else 'no'}")
    print(f"- Design-freeze status: {report['state']['designFreezeStatus']}")
    print(f"- Next suggested lane: {report['state']['nextSuggestedLaneId'] or '-'}")
    print(f"- Latest packet path: {report['state']['latestPacketPath'] or '-'}")
    if report["reasons"]:
        print()
        print("Why this mode:")
        for reason in report["reasons"]:
            print(f"- {reason}")
    print()
    print("Top 3 actions:")
    for index, action in enumerate(report["actions"][:3], start=1):
        print(f"{index}. {action['title']}")
        print(f"   Why: {action['why']}")
        if action["command"]:
            print(f"   Command: {action['command']}")
        if action["files"]:
            print("   Files:")
            for path in action["files"]:
                print(f"   - {path}")
        if action["note"]:
            print(f"   Note: {action['note']}")
    if report["escalateWhen"]:
        print()
        print(f"Escalate only when: {report['escalateWhen']}")


def main() -> int:
    args = parse_args()
    context_path = Path(args.context_manifest_path).expanduser().resolve()
    if not context_path.exists():
        raise SystemExit(
            f"Context manifest not found: {context_path}\n"
            "Run this inside a generated repository, or pass --context-manifest-path."
        )

    repo_root = resolve_repo_root(context_path)
    context_manifest = load_json(context_path)
    refinement_status = load_optional_json(Path(args.refinement_status_path).expanduser().resolve())
    workboard = load_optional_json(Path(args.workboard_path).expanduser().resolve())
    generation_manifest = load_optional_json(Path(args.generation_manifest_path).expanduser().resolve())

    report = build_report(repo_root, context_manifest, refinement_status, workboard, generation_manifest)
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 0

    print_report(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
