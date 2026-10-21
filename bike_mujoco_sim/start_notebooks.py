#!/usr/bin/env python3
"""Start local JupyterLab with this environment's platform-correct bike kernel."""
from __future__ import annotations

import argparse
import os
import sys

from tutorials.setup_env import ROOT, prepare_kernel, server_environment


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-browser", action="store_true")
    parser.add_argument("--port", type=int, default=8888)
    parser.add_argument("--check", action="store_true", help="Check setup without starting a server")
    args = parser.parse_args()
    try:
        data_dir = prepare_kernel()
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(f"Notebook kernel: {data_dir / 'kernels' / 'bike-mujoco-sim' / 'kernel.json'}", flush=True)
    if args.check:
        print("Ready. Run `python start_notebooks.py` to open JupyterLab.")
        return 0
    command = [
        sys.executable, "-m", "jupyterlab", f"--ServerApp.root_dir={ROOT}",
        "--ServerApp.ip=127.0.0.1", f"--ServerApp.port={args.port}",
    ]
    if args.no_browser:
        command.append("--no-browser")
    os.execve(sys.executable, command, server_environment(data_dir))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
