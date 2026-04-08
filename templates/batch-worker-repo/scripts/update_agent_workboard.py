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
    parser.add_argument(
        "--finalize-design-freeze",
        action="store_true",
        help="Complete the design-freeze lane and generate a deterministic execution handoff packet",
    )
    parser.add_argument("--target-lane", help="Target lane id for the guided design-freeze handoff")
    parser.add_argument("--activate-target", action="store_true", help="Mark the target lane as in-progress")
    parser.add_argument("--append-handoff", action="store_true", help="Append a handoff entry to agent-handoff-log.md")
    parser.add_argument("--handoff-from", help="Sender for the handoff entry")
    parser.add_argument("--handoff-to", help="Receiver for the handoff entry")
    parser.add_argument("--handoff-summary", help="Summary for the handoff entry")
    parser.add_argument("--handoff-packet-path", help="Path to a deterministic handoff packet markdown file")
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


def repo_root_from_workboard_path(workboard_path: Path) -> Path:
    return workboard_path.parent.parent if workboard_path.parent.name == ".agent-base" else workboard_path.parent


def resolve_shared_path(workboard: dict, workboard_path: Path, shared_key: str) -> Path | None:
    shared_path = workboard.get("sharedContext", {}).get(shared_key)
    if not shared_path:
        return None
    path = Path(shared_path)
    if not path.is_absolute():
        path = (repo_root_from_workboard_path(workboard_path) / path).resolve()
    return path


def relative_to_repo(path: Path, repo_root: Path) -> str:
    try:
        return str(path.relative_to(repo_root))
    except ValueError:
        return str(path)


def merge_unique(*values: list[str]) -> list[str]:
    merged: list[str] = []
    for items in values:
        for item in items:
            if item and item not in merged:
                merged.append(item)
    return merged


def load_refinement_status(workboard: dict, workboard_path: Path) -> dict | None:
    refinement_path = resolve_shared_path(workboard, workboard_path, "refinementStatusPath")
    if not refinement_path or not refinement_path.exists():
        return None
    return load_json(refinement_path)


def sync_design_state(workboard: dict, workboard_path: Path) -> None:
    refinement_path = resolve_shared_path(workboard, workboard_path, "refinementStatusPath")
    if not refinement_path:
        recompute_agent_workboard_summary(workboard)
        return

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
        if lane.get("latestPacketPath"):
            print(f"  packet: {lane['latestPacketPath']}")


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
    handoff_packet_path: str | None,
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
        f"- Packet path: `{handoff_packet_path or lane.get('latestPacketPath') or '-'}`",
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


def default_packet_path(workboard: dict, workboard_path: Path, source_lane: dict, target_lane: dict) -> tuple[Path, str]:
    repo_root = repo_root_from_workboard_path(workboard_path)
    packet_dir = workboard.get("sharedContext", {}).get("handoffPacketDirectoryPath") or "docs/ai/handoff-packets"
    relative_path = f"{packet_dir}/{source_lane['id']}-to-{target_lane['id']}.md"
    absolute_path = (repo_root / relative_path).resolve()
    return absolute_path, relative_path


def choose_target_lane(workboard: dict, lane_id: str | None) -> dict:
    if lane_id:
        lane = find_lane(workboard, lane_id)
        if lane["id"] == "design-freeze":
            raise SystemExit("Target lane cannot be design-freeze.")
        if lane["status"] == "completed":
            raise SystemExit(f"Target lane is already completed: {lane['id']}")
        if lane["status"] == "blocked":
            raise SystemExit(f"Target lane is blocked and cannot receive the design-freeze handoff: {lane['id']}")
        return lane

    for lane in workboard["workLanes"]:
        if lane["id"] == "design-freeze":
            continue
        if lane["status"] in {"pending", "in-progress"}:
            return lane
    raise SystemExit("No execution lane is available for the design-freeze handoff.")


def render_handoff_packet(
    workboard: dict,
    source_lane: dict,
    target_lane: dict,
    refinement_status: dict | None,
    packet_path: str,
    handoff_summary: str,
    handoff_open_questions: list[str],
    handoff_verification: str,
) -> str:
    shared = workboard.get("sharedContext", {})
    blocking = workboard["summary"]["blockingHighPriorityModuleIds"]
    open_questions = merge_unique(list(target_lane["openQuestions"]), handoff_open_questions)
    shared_inputs = merge_unique(
        [shared.get("workboardPath", "")],
        [shared.get("refinementStatusPath", "")],
        [shared.get("repoLocalOverridesPath", "")],
        [shared.get("commandCatalogPath", "")],
        [shared.get("architectureMapPath", "")],
        list(shared.get("fastPathDocs", [])),
    )
    timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    lines = [
        "# Active Agent Handoff Packet",
        "",
        "이 문서는 planning에서 execution으로 넘어갈 때 현재 실행 계약을 고정한다.",
        "",
        f"- Generated at: `{timestamp}`",
        f"- Packet path: `{packet_path}`",
        f"- From lane: `{source_lane['id']}` (`{source_lane['currentOwner'] or source_lane['role']}`)",
        f"- To lane: `{target_lane['id']}` (`{target_lane['currentOwner'] or target_lane['role']}`)",
        f"- Design ready: `{'yes' if workboard['summary']['designReady'] else 'no'}`",
        f"- Blocking high-priority modules: `{', '.join(blocking) if blocking else 'none'}`",
        "",
        "## Frozen Summary",
        "",
        f"- {handoff_summary}",
        "",
        "## Shared Inputs To Read First",
    ]
    for path in shared_inputs:
        lines.append(f"- `{path}`")

    lines.extend(
        [
            "",
            "## Target Lane Contract",
            "",
            f"- Role: `{target_lane['role']}`",
            f"- Objective: {target_lane['objective']}",
            f"- Scope: {target_lane['scopeSummary']}",
            f"- Depends on: `{', '.join(target_lane['dependsOn']) if target_lane['dependsOn'] else '-'}`",
            f"- Next handoff target: `{target_lane['nextHandoffTarget'] or '-'}`",
            f"- Verification starting point: `{handoff_verification}`",
            "",
            "Owned paths:",
        ]
    )
    for path in target_lane["ownedPaths"]:
        lines.append(f"- {path}")
    lines.extend(["", "Required inputs:"])
    for item in target_lane["requiredInputs"]:
        lines.append(f"- {item}")
    lines.extend(["", "Expected outputs:"])
    for item in target_lane["expectedOutputs"]:
        lines.append(f"- {item}")
    lines.extend(["", "Done when:"])
    for item in target_lane["doneWhen"]:
        lines.append(f"- {item}")
    lines.extend(["", "Open questions:"])
    if open_questions:
        for item in open_questions:
            lines.append(f"- {item}")
    else:
        lines.append("- 없음")
    lines.extend(["", "Existing blockers:"])
    if target_lane["blockers"]:
        for item in target_lane["blockers"]:
            lines.append(f"- {item}")
    else:
        lines.append("- 없음")

    if refinement_status:
        lines.extend(["", "## High-Priority Refinement Snapshot"])
        high_priority_modules = [module for module in refinement_status["modules"] if module["priority"] == "high"]
        if not high_priority_modules:
            lines.extend(["", "- 없음"])
        for module in high_priority_modules:
            lines.extend(
                [
                    "",
                    f"### {module['title']} `{module['id']}`",
                    "",
                    f"- Status: `{module['status']}`",
                    f"- Resolver: `{module['resolver'] or '-'}`",
                    f"- Notes: {module['notes'] or '-'}",
                ]
            )
            if module["status"] == "deferred":
                lines.append(f"- Deferred reason: {module['deferredReason'] or '-'}")

    lines.extend(["", "## Coordination Rules"])
    for rule in workboard.get("coordinationRules", []):
        lines.append(f"- {rule}")

    lines.extend(
        [
            "",
            "## Escalate Back To Design Freeze When",
            "",
            "- 새로운 schema, auth, rollout, environment 판단이 현재 packet 범위를 넘어서기 시작할 때",
            "- target lane의 owned path 밖으로 write scope가 넓어질 때",
            "- high-priority refinement module을 다시 여는 blocker가 생길 때",
            "- verification boundary나 rollback note가 바뀌어 기존 handoff를 믿기 어려워질 때",
        ]
    )
    return "\n".join(lines)


def finalize_design_freeze(
    workboard: dict,
    workboard_path: Path,
    target_lane_id: str | None,
    activate_target: bool,
    summary_text: str | None,
    notes_text: str | None,
    owner: str | None,
    next_handoff: str | None,
    verification_status: str | None,
    extra_open_questions: list[str],
    packet_path_arg: str | None,
) -> tuple[dict, dict, Path, str, str]:
    blocking = list(workboard["summary"]["blockingHighPriorityModuleIds"])
    if blocking:
        raise SystemExit(
            "Cannot finalize design-freeze while high-priority refinement blockers remain: "
            + ", ".join(blocking)
        )
    design_lane = find_lane(workboard, "design-freeze")
    target_lane = choose_target_lane(workboard, target_lane_id)
    repo_root = repo_root_from_workboard_path(workboard_path)

    if packet_path_arg:
        packet_path = Path(packet_path_arg)
        if not packet_path.is_absolute():
            packet_path = (repo_root / packet_path).resolve()
        packet_path_display = relative_to_repo(packet_path, repo_root)
    else:
        packet_path, packet_path_display = default_packet_path(workboard, workboard_path, design_lane, target_lane)

    handoff_summary = summary_text or design_lane["latestSummary"] or (
        f"Design freeze complete. Execution scope is frozen for `{target_lane['id']}`."
    )
    handoff_verification = verification_status or "design-ready"
    shared_open_questions = merge_unique(list(design_lane["openQuestions"]), list(target_lane["openQuestions"]), extra_open_questions)
    target_owner = target_lane["currentOwner"] or target_lane["role"]

    update_lane(
        lane=design_lane,
        new_status="completed",
        owner=owner or design_lane["currentOwner"],
        summary=handoff_summary,
        notes=notes_text if notes_text is not None else design_lane["notes"],
        next_handoff=next_handoff or target_owner,
        verification_status=handoff_verification,
        blockers=[],
        clear_blockers=True,
        open_questions=shared_open_questions,
        clear_open_questions=True,
    )

    target_lane["latestPacketPath"] = packet_path_display
    target_lane["lastUpdated"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    target_lane["openQuestions"] = shared_open_questions
    if not target_lane["latestSummary"]:
        target_lane["latestSummary"] = f"Ready to start from `{packet_path_display}`."
    if activate_target:
        target_lane["status"] = "in-progress"
    design_lane["latestPacketPath"] = packet_path_display

    recompute_agent_workboard_summary(workboard)
    refinement_status = load_refinement_status(workboard, workboard_path)
    packet = render_handoff_packet(
        workboard=workboard,
        source_lane=design_lane,
        target_lane=target_lane,
        refinement_status=refinement_status,
        packet_path=packet_path_display,
        handoff_summary=handoff_summary,
        handoff_open_questions=shared_open_questions,
        handoff_verification=handoff_verification,
    )
    return design_lane, target_lane, packet_path, packet_path_display, packet


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
        target_lane: dict | None = None
        packet_path_display: str | None = None
        packet_text: str | None = None
        if args.interactive:
            updated_lane = interactive_update(workboard)
            if updated_lane is None:
                return 0
        elif args.finalize_design_freeze:
            updated_lane, target_lane, packet_path, packet_path_display, packet_text = finalize_design_freeze(
                workboard=workboard,
                workboard_path=workboard_path,
                target_lane_id=args.target_lane,
                activate_target=args.activate_target,
                summary_text=args.handoff_summary or args.summary,
                notes_text=args.notes,
                owner=args.owner,
                next_handoff=args.handoff_to or args.next_handoff,
                verification_status=args.handoff_verification or args.verification_status,
                extra_open_questions=merge_unique(args.open_question, args.handoff_open_question),
                packet_path_arg=args.handoff_packet_path,
            )
            packet_path.parent.mkdir(parents=True, exist_ok=True)
            write_text_atomic(packet_path, packet_text)
        else:
            if not args.lane:
                raise SystemExit("Use --interactive, --finalize-design-freeze, or provide --lane.")
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
        if args.append_handoff or args.finalize_design_freeze:
            entry = render_handoff_entry(
                lane=updated_lane,
                handoff_from=args.handoff_from,
                handoff_to=args.handoff_to or (target_lane["currentOwner"] if target_lane else None),
                handoff_summary=args.handoff_summary or args.summary,
                handoff_packet_path=packet_path_display or args.handoff_packet_path,
                handoff_files=args.handoff_file or (list(target_lane["ownedPaths"]) if target_lane else []),
                handoff_outputs=args.handoff_output or (list(target_lane["expectedOutputs"]) if target_lane else []),
                handoff_open_questions=args.handoff_open_question or (list(target_lane["openQuestions"]) if target_lane else []),
                handoff_verification=args.handoff_verification or args.verification_status,
            )
            append_handoff_log(handoff_log_path, entry)

    response = {
        "updatedLane": updated_lane["id"],
        "targetLane": target_lane["id"] if target_lane else None,
        "workboardPath": str(workboard_path),
        "handoffLogPath": str(handoff_log_path),
        "lockPath": str(lock_path),
        "packetPath": packet_path_display,
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
