"""Tk joystick subprocess. Its main thread owns all Tk objects on macOS."""
from __future__ import annotations

import json
import queue
import sys
import threading
import time

from .joystick import StickInput, _TkJoystickWindow


def send(event: dict) -> None:
    print(json.dumps(event), flush=True)


class ForwardingStick(StickInput):
    def set_mouse(self, x: float, y: float, down: bool) -> None:
        super().set_mouse(x, y, down)
        send({"event": "mouse", "x": x, "y": y, "down": down})

    def set_key(self, name: str, pressed: bool) -> None:
        super().set_key(name, pressed)
        send({"event": "key", "name": name, "pressed": pressed})

    def request_reset(self) -> None:
        super().request_reset()
        send({"event": "reset"})

    def request_push(self, speed_m_s: float = 0.8) -> None:
        super().request_push(speed_m_s)
        send({"event": "push", "speed": speed_m_s})


def main() -> None:
    commands: queue.Queue = queue.Queue()

    def receive() -> None:
        try:
            for line in sys.stdin:
                commands.put(json.loads(line))
        finally:
            commands.put({"command": "close"})

    threading.Thread(target=receive, daemon=True).start()
    stick = ForwardingStick()
    window = _TkJoystickWindow(stick)
    try:
        window.start()
        send({"event": "ready"})
        while window._root is not None:
            while True:
                try:
                    command = commands.get_nowait()
                except queue.Empty:
                    break
                if command.get("command") == "close":
                    return
                if command.get("command") == "status":
                    stick.set_hardware(*command["axes"])
                    window.set_fallen(bool(command["fallen"]))
            window.poll()
            time.sleep(1.0 / 60.0)
    finally:
        window.close()
        send({"event": "closed"})


if __name__ == "__main__":
    main()
