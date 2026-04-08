#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

from generate_project import recompute_agent_workboard_summary, sync_agent_workboard_with_refinement
from state_io import coordination_lock, default_lock_path, load_json, save_json, write_text_atomic


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_WORKBOARD_PATH = REPO_ROOT / ".agent-base" / "agent-workboard.json"
DEFAULT_HANDOFF_LOG_PATH = REPO_ROOT / "docs" / "ai" / "agent-handoff-log.md"
DEFAULT_LOCK_PATH = default_lock_path(DEFAULT_WORKBOARD_PATH)

STATUS_CHOICES = ["pending", "in-progress", "blocked", "completed"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Update the shared agent workboard and append handoff logs.")
    parser.add_argument("--workboard-path", default=str(DEFAULT_WORKBOARD_PATH), help="Path to agent-workboard.json")
    parser.add_argument("--handoff-log-path", default=str(DEFAULT_HANDOFF_LOG_PATH), help="Path to agent-handoff-log.md")
    parser.add_argument("--lock-path", default=str(DEFAULT_LOCK_PATH), help="Path to the shared coordination lock file")
    parser.add_argument("--lock-timeout-seconds", type=float, default=10.0, help="How long to wait for the coordination lock")
    parser.add_argument("--lane", help="Lane id to update")
    parser.add_argument("--status", choices=STATUS_CHOICES, help="New lane status")
    parser.add_argument("--owner", help="Current owner for the lane")
    parser.add_argument("--summary", help="Latest short summary for this lane")
    parser.add_argument("--notes", help="Notes for this lane")
    parser.add_argument("--next-handoff", help="Next handoff target")
    parser.add_argument("--verification-status", help="Current verification state")
    parser.add_argument("--blocker", action="append", default=[], help="Blocker to add to the lane")
    parser.add_argument("--clear-blockers", action="store_true", help="Clear all lane blockers")
    parser.add_argument("--open-question", action="append", default=[], help="Open question to add to the lane")
    parser.add_argument("--clear-open-questions", action="store_true", help="Clear all lane open questions")
    parser.add_argument("--list", action="store_true", help="List current work lanes and exit")
    parser.add_argument("--interactive", action="store_true", help="Prompt for the next suggested lane interactively")
    parser.add_argument("--append-handoff", action="store_true", help="Append a handoff entry to agent-handoff-log.md")
    parser.add_argument("--handoff-from", help="Sender for the handoff entry")
    parser.add_argument("--handoff-to", help="Receiver for the handoff entry")
    parser.add_argument("--handoff-summary", help="Summary for the handoff entry")
    parser.add_argument("--handoff-file", action="append", default=[], help="File or path in scope for the handoff")
    parser.add_argument("--handoff-output", action="append", default=[], help="Expected output for the handoff")
    parser.add_argument("--handoff-open-question", action="append", default=[], help="Open question for the handoff entry")
    parser.add_argument("--handoff-verification", help="Verification state for the handoff entry")
    return parser.parse_args()


def find_lane(workboard: dict, lane_id: str) -> dict:
    for lane in workboard["workLanes"]:
        if lane["id"] == lane_id:
            return lane
    raise SystemExit(f"Unknown lane id: {lane_id}")


def sync_design_state(workboard: dict, workboard_path: Path) -> None:
    shared = workboard.get("sharedContext", {})
    refinement_path_str = shared.get("refinementStatusPath")
    if not refinement_path_str:
        recompute_agent_workboard_summary(workboard)
        return

    repo_root = workboard_path.parent.parent if workboard_path.parent.name == ".agent-base" else workboard_path.parent
    refinement_path = Path(refinement_path_str)
    if not refinement_path.is_absolute():
        refinement_path = (repo_root / refinement_path).resolve()
    if refinement_path.exists():
        refinement_status = load_json(refinement_path)
        sync_agent_workboard_with_refinement(workboard, refinement_status)
        return
    recompute_agent_workboard_summary(workboard)


def list_lanes(workboard: dict) -> None:
    print("Agent work lanes:")
    print(
        f"- design-ready={workboard['summary']['designReady']} "
        f"next={workboard['summary']['nextSuggestedLaneId'] or '-'}"
    )
    blocking = workboard["summary"]["blockingHighPriorityModuleIds"]
    print(f"- blocking-high-priority={', '.join(blocking) if blocking else 'none'}")
    for lane in workboard["workLanes"]:
        print(
            f"- {lane['id']} [{lane['phase']}] "
            f"status={lane['status']} owner={lane['currentOwner']} next={lane['nextHandoffTarget'] or '-'}"
        )
        print(f"  objective: {lane['objective']}")
        print(f"  scope: {lane['scopeSummary']}")


def ask(prompt: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    raw = input(f"{prompt}{suffix}: ").strip()
    return raw or default


def prompt_status(current: str) -> str:
    print("Select lane status:")
    print("1. pending")
    print("2. in-progress")
    print("3. blocked")
    print("4. completed")
    mapping = {
        "1": "pending",
        "2": "in-progress",
        "3": "blocked",
        "4": "completed",
        "pending": "pending",
        "in-progress": "in-progress",
        "blocked": "blocked",
        "completed": "completed",
    }
    while True:
        choice = ask("Status", current or "pending").lower()
        if choice in mapping:
            return mapping[choice]
        print("Choose one of: pending, in-progress, blocked, completed")


def next_suggested_lane(workboard: dict) -> dict | None:
    lane_id = workboard["summary"].get("nextSuggestedLaneId")
    if not lane_id:
        return None
    return find_lane(workboard, lane_id)


def update_lane(
    lane: dict,
    new_status: str | None,
    owner: str | None,
    summary: str | None,
    notes: str | None,
    next_handoff: str | None,
    verification_status: str | None,
    blockers: list[str],
    clear_blockers: bool,
    open_questions: list[str],
    clear_open_questions: bool,
) -> None:
    if new_status:
        lane["status"] = new_status
    if owner:
        lane["currentOwner"] = owner
    if summary is not None:
        lane["latestSummary"] = summary
    if notes is not None:
        lane["notes"] = notes
    if next_handoff is not None:
        lane["nextHandoffTarget"] = next_handoff
    if verification_status is not None:
        lane["verificationStatus"] = verification_status
    if clear_blockers:
        lane["blockers"] = []
    if blockers:
        existing = list(lane["blockers"])
        for blocker in blockers:
            if blocker not in existing:
                existing.append(blocker)
        lane["blockers"] = existing
    if clear_open_questions:
        lane["openQuestions"] = []
    if open_questions:
        existing_questions = list(lane["openQuestions"])
        for question in open_questions:
            if question not in existing_questions:
                existing_questions.append(question)
        lane["openQuestions"] = existing_questions
    lane["lastUpdated"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def interactive_update(workboard: dict) -> dict | None:
    lane = next_suggested_lane(workboard)
    if not lane:
        print("No suggested pending lane remains.")
        return None

    print(f"Next lane: {lane['id']} [{lane['phase']}] {lane['title']}")
    print(f"Objective: {lane['objective']}")
    print(f"Scope: {lane['scopeSummary']}")
    if lane["dependsOn"]:
        print(f"Depends on: {', '.join(lane['dependsOn'])}")
    print("Owned paths:")
    for path in lane["ownedPaths"]:
        print(f"- {path}")
    print("Expected outputs:")
    for output in lane["expectedOutputs"]:
        print(f"- {output}")

    new_status = prompt_status(lane["status"])
    owner = ask("Current owner", lane["currentOwner"])
    summary = ask("Latest summary", lane["latestSummary"])
    notes = ask("Notes", lane["notes"])
    next_handoff = ask("Next handoff target", lane["nextHandoffTarget"])
    verification = ask("Verification status", lane["verificationStatus"])
    blocker = ""
    if new_status == "blocked":
        blocker = ask("Blocker", "")
    question = ask("Open question", "")

    update_lane(
        lane=lane,
        new_status=new_status,
        owner=owner,
        summary=summary,
        notes=notes,
        next_handoff=next_handoff,
        verification_status=verification,
        blockers=[blocker] if blocker else [],
        clear_blockers=False,
        open_questions=[question] if question else [],
        clear_open_questions=False,
    )
    return lane


def render_handoff_entry(
    lane: dict,
    handoff_from: str | None,
    handoff_to: str | None,
    handoff_summary: str | None,
    handoff_files: list[str],
    handoff_outputs: list[str],
    handoff_open_questions: list[str],
    handoff_verification: str | None,
) -> str:
    timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    files = handoff_files or list(lane["ownedPaths"])
    outputs = handoff_outputs or list(lane["expectedOutputs"])
    open_questions = handoff_open_questions or list(lane["openQuestions"])
    verification = handoff_verification or lane["verificationStatus"] or "not-started"
    lines = [
        f"### Handoff `{lane['id']}` {timestamp}",
        "",
        f"- From: `{handoff_from or lane['currentOwner'] or lane['role']}`",
        f"- To: `{handoff_to or lane['nextHandoffTarget'] or '-'}`",
        f"- Lane status: `{lane['status']}`",
        f"- Summary: {handoff_summary or lane['latestSummary'] or lane['objective']}",
        f"- Verification status: `{verification}`",
        "",
        "Files in scope:",
    ]
    for path in files:
        lines.append(f"- {path}")
    lines.extend(["", "Expected outputs:"])
    for output in outputs:
        lines.append(f"- {output}")
    lines.extend(["", "Open questions:"])
    if open_questions:
        for question in open_questions:
            lines.append(f"- {question}")
    else:
        lines.append("- 없음")
    return "\n".join(lines)


def append_handoff_log(path: Path, entry: str) -> None:
    if path.exists():
        text = path.read_text(encoding="utf-8")
        placeholder = "\n- 아직 기록 없음\n"
        if placeholder in text:
            updated = text.replace(placeholder, "\n" + entry + "\n", 1)
        else:
            suffix = "" if text.endswith("\n") else "\n"
            updated = text + suffix + "\n" + entry + "\n"
    else:
        updated = "# Agent Handoff Log\n\n## Chronological Handoffs\n\n" + entry + "\n"
    write_text_atomic(path, updated)


def main() -> int:
    args = parse_args()
    workboard_path = Path(args.workboard_path).expanduser().resolve()
    handoff_log_path = Path(args.handoff_log_path).expanduser().resolve()
    lock_path = Path(args.lock_path).expanduser().resolve()

    with coordination_lock(lock_path, timeout_seconds=args.lock_timeout_seconds):
        workboard = load_json(workboard_path)
        sync_design_state(workboard, workboard_path)

        if args.list:
            list_lanes(workboard)
            return 0

        updated_lane: dict | None = None
        if args.interactive:
            updated_lane = interactive_update(workboard)
            if updated_lane is None:
                return 0
        else:
            if not args.lane:
                raise SystemExit("Use --interactive or provide --lane.")
            lane = find_lane(workboard, args.lane)
            update_lane(
                lane=lane,
                new_status=args.status,
                owner=args.owner,
                summary=args.summary,
                notes=args.notes,
                next_handoff=args.next_handoff,
                verification_status=args.verification_status,
                blockers=args.blocker,
                clear_blockers=args.clear_blockers,
                open_questions=args.open_question,
                clear_open_questions=args.clear_open_questions,
            )
            updated_lane = lane

        recompute_agent_workboard_summary(workboard)
        save_json(workboard_path, workboard)

        entry = None
        if args.append_handoff:
            entry = render_handoff_entry(
                lane=updated_lane,
                handoff_from=args.handoff_from,
                handoff_to=args.handoff_to,
                handoff_summary=args.handoff_summary,
                handoff_files=args.handoff_file,
                handoff_outputs=args.handoff_output,
                handoff_open_questions=args.handoff_open_question,
                handoff_verification=args.handoff_verification,
            )
            append_handoff_log(handoff_log_path, entry)

    response = {
        "updatedLane": updated_lane["id"],
        "workboardPath": str(workboard_path),
        "handoffLogPath": str(handoff_log_path),
        "lockPath": str(lock_path),
        "handoffWritten": bool(entry),
        "laneStatus": updated_lane["status"],
        "currentOwner": updated_lane["currentOwner"],
        "nextSuggestedLaneId": workboard["summary"]["nextSuggestedLaneId"],
        "blockingHighPriorityModuleIds": workboard["summary"]["blockingHighPriorityModuleIds"],
    }
    print(json.dumps(response, ensure_ascii=False))
    if entry:
        print()
        print(entry)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
