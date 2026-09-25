# MathLang Setup Guide

This guide describes how to set up, run, and test the MathLang compiler in a clean Python environment.

---

## 1. Requirements
- Python 3.11+
- pip (Python package installer)
- Git (optional)

---

## 2. Clone the Repository
Clone or navigate to the compiler directory:
```bash
git clone <repository-url>
cd MathLang
```

---

## 3. Create a Virtual Environment (Optional but Recommended)
### Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

### Linux/macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 4. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 5. Run the Test Suite
Ensure that all compiler phases are functional:
```bash
python -m pytest
```

---

## 6. Running the Compiler
Compile and execute the basic example:
```bash
python main.py examples/01_basic.math
```

---

## 7. Running Individual Compiler Phases
To demonstrate individual phases, run:
- **Tokens**: `python main.py examples/01_basic.math --tokens`
- **AST**: `python main.py examples/01_basic.math --ast`
- **Symbol Table**: `python main.py examples/01_basic.math --symbols`
- **Intermediate Code**: `python main.py examples/01_basic.math --ir`
- **Optimized Code**: `python main.py examples/01_basic.math --optimized-ir`
- **Generated Code**: `python main.py examples/01_basic.math --code`
- **Educational Debug Pipeline**: `python main.py examples/01_basic.math --debug`

---

## 8. Common Troubleshooting

### 'python' or 'python3' is not recognized
- **Cause**: Python is not installed or not added to your system PATH.
- **Fix**: Reinstall Python and check the box **"Add Python to PATH"** in the installer, or manually configure it in environment variables.

### 'pip' is not recognized
- **Cause**: pip is not installed or PATH is not configured.
- **Fix**: Try running `python -m pip` instead of raw `pip` commands, e.g., `python -m pip install -r requirements.txt`.

### ModuleNotFoundError: No module named 'src'
- **Cause**: Python is not evaluating the execution path correctly.
- **Fix**: Run commands from the root directory `MathLang/` (not inside `src/` or `examples/`).

### Permission Problems
- **Cause**: Running pip globally inside system directories.
- **Fix**: Use a Python virtual environment (recommended above) or install package locally with `python -m pip install --user -r requirements.txt`.

### Virtual Environment Activation Issues
- **Cause**: Execution Policies in Windows PowerShell block script execution.
- **Fix**: Run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process` in PowerShell, then run `venv\Scripts\activate`.
