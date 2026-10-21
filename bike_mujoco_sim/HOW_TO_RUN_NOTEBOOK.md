# Run notebooks on a local server

Requirements: **Python 3.10 or 3.11**, Tk, a desktop display, and internet access for the first installation.

## 1. Open the simulation folder

Run this from the repository root:

```bash
# Open the simulation folder.
cd bike_mujoco_sim
```

## 2. Create and activate an environment

Choose one option below, or activate an existing Python 3.10/3.11 environment.

### Conda — macOS, Windows, or Linux

```bash
# Create the workshop environment with Python and Tk.
conda create -n bike-workshop python=3.11 tk
# Activate the workshop environment.
conda activate bike-workshop
```

### venv — macOS or Linux

Use a Python installation with Tk; Homebrew users need the matching `python-tk` package, and Linux users need `python3-tk`.

```bash
# Create a virtual environment.
python3.11 -m venv .venv
# Activate the virtual environment.
source .venv/bin/activate
```

### venv — Windows PowerShell

```powershell
# Create a virtual environment.
py -3.11 -m venv .venv
# Activate the virtual environment.
.\.venv\Scripts\Activate.ps1
```

## 3. Install and start

```bash
# Install dependencies and prepare the notebook kernel.
python tutorials/setup_env.py
# Start JupyterLab in your browser.
python start_notebooks.py
```

## 4. Run the lessons

1. Open the local URL printed in the terminal if JupyterLab does not open automatically.
2. Open `tutorials/00_setup_and_install.ipynb`, then continue through the lessons in order.
3. Select **Bike MuJoCo sim** as the kernel for each notebook.
4. Run each notebook's cells from top to bottom.
5. Close the MuJoCo window to finish a window demonstration.
6. Use the mouse stick, arrow keys, **Reset bike**, and **Push sideways** for Lesson 4.
7. Press **Control+C** in the server terminal to stop JupyterLab.

## Later sessions

Activate the same environment, then run these commands from the repository root:

```bash
# Open the simulation folder.
cd bike_mujoco_sim
# Start JupyterLab.
python start_notebooks.py
```

## Optional checks

```bash
# Check the environment and kernel setup.
python start_notebooks.py --check
# Start JupyterLab on port 8889 if port 8888 is occupied.
python start_notebooks.py --port 8889
```

Run this inside a macOS notebook:

```python
# Check that the kernel uses mjpython; the result should be True.
from mujoco import viewer
print(viewer._MJPYTHON is not None)
```

## VS Code

Connect to the existing server URL printed in the terminal and select **Bike MuJoCo sim** as the kernel.

## Google Colab

Use the notebooks' Colab setup cells instead of this local setup.
