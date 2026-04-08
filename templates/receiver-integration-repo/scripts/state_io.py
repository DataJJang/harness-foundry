#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import tempfile
import time
from contextlib import contextmanager
from pathlib import Path

try:
    import fcntl
except ImportError:  # pragma: no cover - fallback path for non-Unix hosts
    fcntl = None


DEFAULT_LOCK_TIMEOUT_SECONDS = 10.0
DEFAULT_LOCK_POLL_SECONDS = 0.05


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fp:
        return json.load(fp)


def write_text_atomic(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            "w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f"{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as fp:
            fp.write(content)
            temp_path = Path(fp.name)
        os.replace(temp_path, path)
    finally:
        if temp_path and temp_path.exists():
            temp_path.unlink(missing_ok=True)


def save_json(path: Path, payload: dict) -> None:
    write_text_atomic(path, json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


def default_lock_path(anchor_path: Path) -> Path:
    return anchor_path.parent / "coordination.lock"


@contextmanager
def coordination_lock(
    lock_path: Path,
    timeout_seconds: float = DEFAULT_LOCK_TIMEOUT_SECONDS,
    poll_seconds: float = DEFAULT_LOCK_POLL_SECONDS,
):
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    if fcntl is not None:
        with lock_path.open("a+", encoding="utf-8") as lock_file:
            deadline = time.monotonic() + timeout_seconds
            while True:
                try:
                    fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                    break
                except BlockingIOError:
                    if time.monotonic() >= deadline:
                        raise TimeoutError(f"Timed out waiting for coordination lock: {lock_path}")
                    time.sleep(poll_seconds)
            lock_file.seek(0)
            lock_file.truncate()
            lock_file.write(f"pid={os.getpid()} acquired={time.strftime('%Y-%m-%dT%H:%M:%S')}\n")
            lock_file.flush()
            try:
                yield
            finally:
                lock_file.seek(0)
                lock_file.truncate()
                lock_file.flush()
                fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)
        return

    # Fallback path for environments without fcntl.
    deadline = time.monotonic() + timeout_seconds
    fd: int | None = None
    while True:
        try:
            fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, f"pid={os.getpid()} acquired={time.strftime('%Y-%m-%dT%H:%M:%S')}\n".encode("utf-8"))
            break
        except FileExistsError:
            if time.monotonic() >= deadline:
                raise TimeoutError(f"Timed out waiting for coordination lock: {lock_path}")
            time.sleep(poll_seconds)

    try:
        yield
    finally:
        if fd is not None:
            os.close(fd)
        lock_path.unlink(missing_ok=True)
