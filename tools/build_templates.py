#!/usr/bin/env python3
from __future__ import annotations

import argparse
import fnmatch
import json
import shutil
import sys
import tempfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = REPO_ROOT / "template-build.json"
OVERLAYS_DIR = REPO_ROOT / "template_overlays"


def load_config() -> dict:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def should_exclude(rel_path: str, exclude_globs: list[str]) -> bool:
    normalized = rel_path.replace("\\", "/")
    for pattern in exclude_globs:
        if fnmatch.fnmatch(normalized, pattern):
            return True
    return False


def copy_tree_filtered(src: Path, dst: Path, exclude_globs: list[str]) -> None:
    for path in sorted(src.rglob("*")):
        rel = path.relative_to(src)
        rel_str = rel.as_posix()
        if should_exclude(rel_str, exclude_globs):
            continue
        target = dst / rel
        if path.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)


def prune_directory_to_keep(dir_path: Path, keep_names: list[str]) -> None:
    if not dir_path.exists():
        return
    keep = set(keep_names)
    for child in dir_path.iterdir():
        if child.is_file() and child.name not in keep:
            child.unlink()


def copy_overlay(template_name: str, dst: Path) -> None:
    overlay_dir = OVERLAYS_DIR / template_name
    if not overlay_dir.exists():
        return
    for path in sorted(overlay_dir.rglob("*")):
        rel = path.relative_to(overlay_dir)
        target = dst / rel
        if path.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)


def dirs_equal(left: Path, right: Path) -> tuple[bool, list[str]]:
    left_files = sorted(
        str(p.relative_to(left)) for p in left.rglob("*") if p.is_file()
    )
    right_files = sorted(
        str(p.relative_to(right)) for p in right.rglob("*") if p.is_file()
    )
    diffs: list[str] = []
    if left_files != right_files:
        left_set = set(left_files)
        right_set = set(right_files)
        for rel in sorted(left_set - right_set):
            diffs.append(f"only-in-generated {rel}")
        for rel in sorted(right_set - left_set):
            diffs.append(f"only-in-template {rel}")
    for rel in sorted(set(left_files) & set(right_files)):
        if (left / rel).read_bytes() != (right / rel).read_bytes():
            diffs.append(f"content-diff {rel}")
    return (len(diffs) == 0, diffs)


def build_template(
    source_dir: Path,
    output_dir: Path,
    template_name: str,
    template_cfg: dict,
    exclude_globs: list[str],
    check_only: bool,
) -> tuple[bool, list[str]]:
    with tempfile.TemporaryDirectory(prefix=f"harness-foundry_{template_name}_") as tmpdir:
        tmp_root = Path(tmpdir) / template_name
        tmp_root.mkdir(parents=True, exist_ok=True)
        copy_tree_filtered(source_dir, tmp_root, exclude_globs)
        prune_directory_to_keep(
            tmp_root / ".cursor" / "rules",
            template_cfg.get("keep_cursor_rules", []),
        )
        prune_directory_to_keep(
            tmp_root / ".github" / "instructions",
            template_cfg.get("keep_github_instructions", []),
        )
        copy_overlay(template_name, tmp_root)

        existing = output_dir / template_name
        if check_only:
            if not existing.exists():
                return False, [f"missing-template {template_name}"]
            return dirs_equal(tmp_root, existing)

        if existing.exists():
            shutil.rmtree(existing)
        shutil.copytree(tmp_root, existing)
        return True, []


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Rebuild templates/* from source/ + template-build.json"
    )
    parser.add_argument(
        "--template",
        action="append",
        dest="templates",
        help="build only the specified template name (repeatable)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify templates match generated output without rewriting",
    )
    args = parser.parse_args()

    config = load_config()
    source_dir = REPO_ROOT / config["base_source_dir"]
    output_dir = REPO_ROOT / config["template_output_dir"]
    exclude_globs = config["exclude_globs"]
    templates: dict[str, dict] = config["templates"]

    selected = set(args.templates or templates.keys())
    unknown = sorted(selected - set(templates.keys()))
    if unknown:
        print(f"unknown templates: {', '.join(unknown)}", file=sys.stderr)
        return 2

    failed = False
    for template_name in sorted(selected):
        ok, diffs = build_template(
            source_dir=source_dir,
            output_dir=output_dir,
            template_name=template_name,
            template_cfg=templates[template_name],
            exclude_globs=exclude_globs,
            check_only=args.check,
        )
        if args.check:
            if ok:
                print(f"[OK] {template_name}")
            else:
                failed = True
                print(f"[DIFF] {template_name}")
                for diff in diffs[:40]:
                    print(f"  - {diff}")
                if len(diffs) > 40:
                    print(f"  - ... {len(diffs) - 40} more")
        else:
            print(f"[BUILT] {template_name}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
