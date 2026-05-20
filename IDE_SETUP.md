# IDE Configuration for ChromaGoggles

## Overview
Your IDE (PyCharm/JetBrains) may show import errors because it's not configured to use the Poetry virtual environment. The code itself is correct and works (all tests pass), but the IDE needs to be pointed to the right Python interpreter.

## Finding Your Poetry Virtual Environment

Run this command to find the Python interpreter path:

```bash
cd /home/baer/Documents/GitHub/ChromaGoggles
poetry env info --path
```

This will output something like:
```
/home/baer/.cache/pypoetry/virtualenvs/chromagoggles-XXXXXXX-py3.13
```

The actual Python executable will be at:
```
/home/baer/.cache/pypoetry/virtualenvs/chromagoggles-XXXXXXX-py3.13/bin/python
```

## Configuring PyCharm/JetBrains IDE

### Method 1: Automatic Detection
1. Open the project in PyCharm
2. PyCharm should detect the Poetry environment automatically
3. Look for a notification banner at the top suggesting to configure Poetry
4. Click "Configure" or "Use Poetry Interpreter"

### Method 2: Manual Configuration
1. Open **Settings/Preferences** (Ctrl+Alt+S on Linux)
2. Navigate to **Project: ChromaGoggles** → **Python Interpreter**
3. Click the gear icon ⚙️ → **Add...**
4. Select **Poetry Environment**
5. PyCharm will detect the existing environment
6. Click **OK**

### Method 3: Direct Path Configuration
1. Open **Settings/Preferences** (Ctrl+Alt+S on Linux)
2. Navigate to **Project: ChromaGoggles** → **Python Interpreter**
3. Click the gear icon ⚙️ → **Add...**
4. Select **Existing Environment**
5. Browse to the path from `poetry env info --path` + `/bin/python`
6. Click **OK**

## Verifying Configuration

After configuration, you should:
1. See no import errors in the IDE
2. Have autocomplete working for numpy, cv2, PIL, etc.
3. Be able to run files directly from the IDE

## Alternative: Use Terminal

If you don't want to configure the IDE, you can always run from terminal:

```bash
# Activate the Poetry shell
poetry shell

# Then run any command
python test_basic.py
streamlit run main.py
```

Or run directly with Poetry:

```bash
poetry run python test_basic.py
poetry run streamlit run main.py
```

## Checking Dependencies Are Installed

Verify all packages are available:

```bash
cd /home/baer/Documents/GitHub/ChromaGoggles
poetry run python -c "import numpy, cv2, PIL, skimage, matplotlib, seaborn, streamlit; print('All imports successful!')"
```

If this prints "All imports successful!" then everything is installed correctly and it's just an IDE configuration issue.

## Current Status

✅ All dependencies are installed in the Poetry environment
✅ All tests pass when run via `poetry run`
✅ Code is correct and functional
⚠️  IDE needs to be pointed to the Poetry virtual environment

## Quick Test

To verify everything works without IDE configuration:

```bash
cd /home/baer/Documents/GitHub/ChromaGoggles
poetry run python test_basic.py
```

This should show all tests passing.

## Need Help?

If you continue to have issues:
1. Try `poetry install --sync` to refresh the environment
2. Try `poetry env remove python` followed by `poetry install` to recreate
3. Check that Poetry itself is properly installed: `poetry --version`

