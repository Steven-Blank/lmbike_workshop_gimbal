"""Regression checks for portable kernel setup and joystick input transport."""
from __future__ import annotations

import json
from types import SimpleNamespace

import pytest

from tutorials import setup_env
from sim.joystick import StickInput, _apply_window_event
from sim.joystick_ui import ForwardingStick
from sim import viewer as bike_viewer


def test_kernel_uses_this_environment_on_mac_and_other_platforms(tmp_path):
    python = tmp_path / "student env with spaces" / "bin" / "python"
    python.parent.mkdir(parents=True)
    python.touch()
    python.with_name("mjpython").touch()
    mac = setup_env.kernel_spec(python, "darwin")
    linux = setup_env.kernel_spec(python, "linux")
    assert mac["argv"] == [str(python), str(python.with_name("mjpython")), "-m", "ipykernel_launcher", "-f", "{connection_file}"]
    assert linux["argv"][0] == str(python)
    python.with_name("mjpython").unlink()
    with pytest.raises(RuntimeError, match="mjpython was not found"):
        setup_env.kernel_spec(python, "darwin")


def test_unsupported_python_fails_before_install(monkeypatch):
    monkeypatch.setattr(setup_env.sys, "version_info", (3, 14, 0))
    with pytest.raises(RuntimeError, match="Python 3.10 or 3.11"):
        setup_env.check_python()


def test_project_kernel_search_path_precedes_existing_data(monkeypatch, tmp_path):
    import os
    monkeypatch.setenv("JUPYTER_PATH", str(tmp_path / "old-data"))
    env = setup_env.server_environment(tmp_path / "student-checkout" / ".jupyter")
    assert env["JUPYTER_PATH"].split(os.pathsep) == [
        str(tmp_path / "student-checkout" / ".jupyter"), str(tmp_path / "old-data")
    ]


def test_all_notebooks_select_the_portable_kernel():
    for path in (setup_env.ROOT / "tutorials").glob("*.ipynb"):
        nb = json.loads(path.read_text(encoding="utf-8"))
        assert nb["metadata"]["kernelspec"]["name"] == setup_env.KERNEL_NAME, path


def test_mouse_keys_push_and_reset_survive_json_pipe(capsys):
    ui = ForwardingStick()
    sim = StickInput()

    def transfer():
        for line in capsys.readouterr().out.splitlines():
            _apply_window_event(sim, json.loads(line))

    ui.set_mouse(0.7, -0.2, True)
    transfer()
    assert sim.axes() == (0.7, -0.2)
    ui.set_mouse(0.0, 0.0, False)
    ui.set_key("left", True)
    transfer()
    sim.advance_keys(0.05)
    assert sim.axes()[0] > 0
    ui.request_push(0.8)
    transfer()
    assert sim.consume_push() == 0.8
    assert sim.consume_push() is None
    ui.request_reset()
    transfer()
    assert sim.consume_reset()
    assert not sim.consume_reset()
    assert sim.axes() == (0.0, 0.0)


def test_repeated_viewer_waits_for_native_teardown(monkeypatch):
    from mujoco import viewer
    calls = []
    handle = SimpleNamespace(close=lambda: None)

    def launch(*args, **kwargs):
        calls.append(True)
        if len(calls) < 3:
            raise RuntimeError("another MuJoCo viewer is already open")
        return handle

    monkeypatch.setattr(viewer, "launch_passive", launch)
    monkeypatch.setattr(bike_viewer.sys, "platform", "darwin")
    sim = SimpleNamespace(model=None, data=None, mode="speed-schedule")
    actual, window = bike_viewer._open_windows(sim, StickInput(), SimpleNamespace(close=lambda: None), None)
    assert actual is handle and window is None
    assert len(calls) == 3


def test_joystick_startup_error_closes_viewer_and_hardware(monkeypatch):
    from mujoco import viewer
    closed = []
    handle = SimpleNamespace(close=lambda: closed.append("viewer"))

    class BrokenWindow:
        def __init__(self, stick):
            pass
        def start(self):
            raise RuntimeError("Tk is missing")
        def close(self):
            closed.append("joystick")

    monkeypatch.setattr(viewer, "launch_passive", lambda *a, **kw: handle)
    monkeypatch.setattr(bike_viewer, "JoystickWindow", BrokenWindow)
    sim = SimpleNamespace(model=None, data=None, mode="remote")
    hardware = SimpleNamespace(close=lambda: closed.append("hardware"))
    with pytest.raises(RuntimeError, match="Tk is missing"):
        bike_viewer._open_windows(sim, StickInput(), hardware, None)
    assert closed == ["joystick", "hardware", "viewer"]
