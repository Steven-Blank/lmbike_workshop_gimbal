# Run the lessons on a local Jupyter server

Use **Python 3.10 or 3.11** in a venv or Conda environment. The commands below
work from your own checkout; no paths or kernel files from another student's
computer are needed. The first setup needs internet access to install packages.

## macOS: first setup

Open a terminal in the repository, then run:

```bash
cd bike_mujoco_sim
python3.11 -m venv .venv
source .venv/bin/activate
python tutorials/setup_env.py
python start_notebooks.py
```

Use `python3.10` instead if that is the version you installed. Install a Python
build that includes Tk, such as the python.org installer, for the floating
joystick window. Homebrew users need the matching `python-tk` package too.

**If you already have a Conda environment**, activate it instead of creating a
venv. For example, a new environment can be created with:

```bash
conda create -n bike-workshop python=3.11 tk
conda activate bike-workshop
cd path/to/lmbike_workshop_gimbal/bike_mujoco_sim
python tutorials/setup_env.py
python start_notebooks.py
```

An existing Python 3.10/3.11 Conda environment is fine. The setup script checks
the installed requirements and installs packages only when something is missing
or incompatible. Simulation dependencies and local Jupyter dependencies stay
in their separate requirements files so Google Colab is unaffected.

## Open the lessons

1. The launcher opens JupyterLab in your browser. If it does not, open the local
   URL printed in the terminal, including its token.
2. Open `tutorials/00_setup_and_install.ipynb`, then the lessons in order.
3. In each notebook, select **Bike MuJoCo sim** as the kernel. If prompted for a
   replacement kernel, choose that name. Do not choose a generic Python kernel
   on macOS for the window demonstrations.
4. Run cells from top to bottom. A window cell waits until you close its MuJoCo
   window. Reaching the configured duration restarts the speed-schedule ride;
   it does not close the window automatically.
5. In Lesson 4 the separate **Bike joystick** window supports the mouse stick,
   Reset bike, and Push sideways. Close the MuJoCo window to finish the cell;
   the joystick closes with it. The MuJoCo window also accepts the arrow keys.
6. Stop the local server with Control+C in its terminal when you finish.

The windows appear on the computer running the server. Use this workflow on
your Mac's desktop, rather than on a headless SSH server.

## Every later session

Activate the same environment, then:

```bash
cd path/to/lmbike_workshop_gimbal/bike_mujoco_sim
python start_notebooks.py
```

The launcher recreates the project-local kernel definition in `.jupyter/`
using the active environment. That generated directory is ignored by Git.
Moving the checkout or recreating the environment is handled on the next launch.
There is no need to install a shared, per-user kernel by hand.

## Check the macOS kernel

For a setup check without opening a server:

```bash
python start_notebooks.py --check
```

Inside a notebook, this should print `True` on macOS:

```python
from mujoco import viewer
print(viewer._MJPYTHON is not None)
```

The launcher starts JupyterLab with ordinary Python, but configures the **kernel
process** to start with this environment's `mjpython`. This is the process that
executes the cells. Starting only the server with `mjpython -m jupyter lab`
does not change the interpreter in a generic Python kernelspec.

MuJoCo's [macOS passive-viewer requirement](https://mujoco.readthedocs.io/en/stable/python.html#passive-viewer)
and Jupyter's [kernel launch configuration](https://jupyter-client.readthedocs.io/en/stable/kernels.html#kernel-specs)
explain the two processes. On macOS the Tk joystick runs in a separate ordinary
Python process so that Tk and MuJoCo do not compete for the same native GUI loop.

## VS Code or another editor

You can use JupyterLab in the browser, or connect your editor to the **existing
server URL** printed by `python start_notebooks.py`, then choose **Bike MuJoCo
sim**. Selecting the environment's raw Python interpreter instead bypasses the
project-local macOS kernel configuration.

## Windows and Linux

The same setup script and launcher use ordinary Python kernels on these systems.

Windows PowerShell:

```powershell
cd bike_mujoco_sim
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python tutorials/setup_env.py
python start_notebooks.py
```

Linux desktop:

```bash
cd bike_mujoco_sim
python3.11 -m venv .venv
source .venv/bin/activate
python tutorials/setup_env.py
python start_notebooks.py
```

For the Linux floating joystick, install your distribution's matching
`python3-tk` package if Tk is missing. A desktop display is required for windows.

## Common problems

| Message or symptom | What to do |
| --- | --- |
| Python 3.14 or another unsupported version | Activate Python 3.10/3.11, then run setup again. |
| Missing or incompatible packages | Run `python tutorials/setup_env.py` in that environment. |
| `No such kernel named bike-mujoco-sim` | Start with `python start_notebooks.py`; its server discovers the generated kernel. |
| macOS says to use mjpython | Choose **Bike MuJoCo sim**, restart that kernel, and run from the top. |
| Window cell appears busy | Close the MuJoCo window to finish it. |
| A notebook cannot find the project | Open the notebook through the server started by this launcher. |
| Port 8888 is occupied | Use `python start_notebooks.py --port 8889`. |

For terminal simulation on macOS, use `mjpython run_sim.py ...` for a GUI and
`python run_sim.py --headless ...` without one. The launcher and local notebook
requirements are not needed on Google Colab; use the lessons' existing Colab cells.
