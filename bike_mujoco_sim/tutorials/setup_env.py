#!/usr/bin/env python3
"""Install local notebook dependencies and prepare this checkout's kernel."""
from __future__ import annotations

import argparse
import importlib.metadata
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
KERNEL_NAME = "bike-mujoco-sim"
KERNEL_DISPLAY_NAME = "Bike MuJoCo sim"


def check_python() -> None:
    if sys.version_info[:2] not in ((3, 10), (3, 11)):
        raise RuntimeError(
            "Use Python 3.10 or 3.11 for this workshop. Activate its venv or "
            "Conda environment, then run this command again."
        )


def in_project_environment() -> bool:
    return sys.prefix != sys.base_prefix or (Path(sys.prefix) / "conda-meta").is_dir()


def missing_requirements() -> list[str]:
    try:
        from packaging.requirements import Requirement
    except ImportError:
        return ["local notebook dependencies"]
    missing = []
    for filename in ("requirements.txt", "requirements-jupyter.txt"):
        for line in (ROOT / filename).read_text(encoding="utf-8").splitlines():
            line = line.split("#", 1)[0].strip()
            if not line:
                continue
            requirement = Requirement(line)
            if requirement.marker and not requirement.marker.evaluate():
                continue
            try:
                version = importlib.metadata.version(requirement.name)
            except importlib.metadata.PackageNotFoundError:
                missing.append(line)
                continue
            if version not in requirement.specifier:
                missing.append(line)
    return missing


def kernel_spec(python: str | Path, platform: str) -> dict:
    python = Path(python).absolute()
    command = [str(python)]
    if platform == "darwin":
        launcher = python.with_name("mjpython")
        if not launcher.is_file():
            raise RuntimeError(
                f"mjpython was not found beside {python}. Run "
                "`python tutorials/setup_env.py` in your workshop environment."
            )
        # MuJoCo ships a Python script whose installed shebang can contain
        # spaces (or exceed the OS length limit). Execute that script with
        # this Python explicitly; it then execs MuJoCo's native launcher.
        command.append(str(launcher))
    return {
        "argv": command + ["-m", "ipykernel_launcher", "-f", "{connection_file}"],
        "display_name": KERNEL_DISPLAY_NAME,
        "language": "python",
    }


def prepare_kernel(root: Path = ROOT) -> Path:
    check_python()
    if not in_project_environment():
        raise RuntimeError("Activate a Python 3.10/3.11 venv or Conda environment first.")
    missing = missing_requirements()
    if missing:
        raise RuntimeError(
            "Missing or incompatible packages: " + ", ".join(missing)
            + ". Run `python tutorials/setup_env.py` first."
        )
    if sys.platform == "darwin" and importlib.util.find_spec("_tkinter") is None:
        raise RuntimeError(
            "This Python has no Tk support for the joystick. With Conda, install "
            "`conda install tk`; with Homebrew, install the python-tk package for "
            "your Python version, or use a Python installer that includes Tk."
        )
    data_dir = root / ".jupyter"
    destination = data_dir / "kernels" / KERNEL_NAME / "kernel.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(kernel_spec(sys.executable, sys.platform), indent=2) + "\n",
        encoding="utf-8",
    )
    return data_dir


def server_environment(data_dir: Path) -> dict[str, str]:
    env = os.environ.copy()
    existing = env.get("JUPYTER_PATH")
    env["JUPYTER_PATH"] = str(data_dir) + (os.pathsep + existing if existing else "")
    return env


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skip-install", action="store_true", help="Only check packages and prepare the kernel")
    args = parser.parse_args()
    try:
        check_python()
        if not in_project_environment():
            raise RuntimeError("Create or activate a venv or Conda environment before installing packages.")
        if not args.skip_install and missing_requirements():
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "--no-user", "-r", str(ROOT / "requirements.txt"),
                 "-r", str(ROOT / "requirements-jupyter.txt")], check=True,
            )
        data_dir = prepare_kernel()
        print(f"Python: {sys.executable}")
        print(f"Prepared {KERNEL_DISPLAY_NAME}: {data_dir / 'kernels' / KERNEL_NAME}")
        print("Start the local server with: python start_notebooks.py")
        return 0
    except (RuntimeError, subprocess.CalledProcessError) as exc:
        print(f"Setup failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
