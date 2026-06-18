#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Run enterprise UI test suite")
    parser.add_argument("--env", default="staging", choices=["dev", "staging", "prod"])
    parser.add_argument("--markers", default="", help="Pytest marker expression")
    parser.add_argument("--parallel", action="store_true", help="Enable pytest-xdist")
    parser.add_argument("--workers", default="auto", help="Number of xdist workers")
    parser.add_argument("--headed", action="store_true", help="Run browser in headed mode")
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parents[1]
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        f"--env={args.env}",
    ]

    if args.markers:
        cmd.extend(["-m", args.markers])
    if args.parallel:
        cmd.extend(["-n", args.workers])

    env = {}
    if args.headed:
        env["HEADLESS"] = "false"

    completed = subprocess.run(cmd, cwd=project_root, env={**os.environ, **env})
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
