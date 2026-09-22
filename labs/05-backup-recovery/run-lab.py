#!/usr/bin/env python3
"""Measure restore time and data loss for a synthetic SQLite HTTP service."""
import json
from contextlib import closing
import shutil
import socket
import sqlite3
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from http.client import HTTPException
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen

SERVICE = Path(__file__).with_name("service.py")


def utc():
    return datetime.now(timezone.utc)


def request(port, path, value=None):
    body = None if value is None else json.dumps({"value": value}).encode()
    req = Request(
        f"http://127.0.0.1:{port}{path}",
        data=body,
        headers={"Content-Type": "application/json"} if body else {},
        method="POST" if body else "GET",
    )
    with urlopen(req, timeout=1) as response:
        return json.load(response)


def start(db, port):
    process = subprocess.Popen(
        [sys.executable, str(SERVICE), "--db", str(db), "--port", str(port)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    deadline = time.monotonic() + 5
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError("service exited before health check")
        try:
            if request(port, "/health")["ok"]:
                return process
        except (URLError, TimeoutError, HTTPException):
            time.sleep(0.05)
    process.terminate()
    process.wait(timeout=3)
    raise TimeoutError("service did not start within five seconds")


def stop(process):
    if process and process.poll() is None:
        process.terminate()
        try:
            process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=3)


def main():
    with tempfile.TemporaryDirectory(prefix="lab05-recovery-") as work:
        root = Path(work)
        db = root / "primary.sqlite3"
        backup = root / "snapshot.sqlite3"
        with socket.socket() as sock:
            sock.bind(("127.0.0.1", 0))
            port = sock.getsockname()[1]
        process = None
        try:
            process = start(db, port)
            for n in range(1, 4):
                assert request(port, "/events", f"baseline-{n}")["seq"] == n
            before = request(port, "/health")
            with closing(sqlite3.connect(db)) as source, closing(sqlite3.connect(backup)) as target:
                source.backup(target)
            backup_at = utc()
            for n in range(4, 6):
                assert request(port, "/events", f"after-backup-{n}")["seq"] == n
            pre_failure = request(port, "/health")
            failure_at = utc()
            failure_start = time.monotonic()
            stop(process)
            process = None
            db.unlink()
            outage_confirmed = False
            try:
                request(port, "/health")
            except (URLError, TimeoutError, HTTPException):
                outage_confirmed = True
            if not outage_confirmed:
                raise AssertionError("service outage was not observed")
            bad_restore_rejected = False
            try:
                shutil.copyfile(root / "missing-snapshot.sqlite3", db)
            except FileNotFoundError:
                bad_restore_rejected = True
            shutil.copyfile(backup, db)
            process = start(db, port)
            after = request(port, "/health")
            rto_seconds = round(time.monotonic() - failure_start, 3)
            lost_events = pre_failure["count"] - after["count"]
            if not (before["count"] == 3 and pre_failure["count"] == 5
                    and after["count"] == 3 and after["last_seq"] == 3
                    and lost_events == 2 and outage_confirmed and bad_restore_rejected):
                raise AssertionError("unexpected backup or recovery result")
            result = {
                "status": "pass",
                "at_utc": utc().isoformat(),
                "baseline_events": before["count"],
                "events_before_failure": pre_failure["count"],
                "events_after_restore": after["count"],
                "lost_events": lost_events,
                "backup_to_failure_seconds": round((failure_at - backup_at).total_seconds(), 3),
                "rto_seconds": rto_seconds,
                "outage_observed": outage_confirmed,
                "missing_backup_rejected": bad_restore_rejected,
                "storage": "temporary local SQLite; deleted after run",
            }
            print(json.dumps(result, ensure_ascii=False, indent=2))
        finally:
            stop(process)


if __name__ == "__main__":
    main()
