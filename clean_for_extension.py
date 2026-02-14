"""
=====================================================================
Code Artifact:   clean_for_extension.py
Description:     Utility script to remove __pycache__ and .pytest_cache
                 directories from the GoPhishFree extension folder.
                 Chrome Manifest V3 rejects extensions containing
                 directories whose names start with underscores.
                 Run this before loading/reloading the extension if
                 Python scripts have been executed in the project.

Programmers:     Ty Farrington
Created:         2026-02-05
Revised:
  2026-02-05 — Initial version to fix extension loading errors
               caused by __pycache__ directories (Ty Farrington)

Preconditions:
  - Python 3.7+ installed
  - Script must be located in the extension root directory

Acceptable Input:   None (no arguments required)
Unacceptable Input: N/A

Postconditions:
  - All __pycache__ and .pytest_cache directories removed recursively
  - Extension folder is loadable by Chrome

Return Values:
  - Exit code 0 on success
  - Console output listing removed directories

Error Handling:
  - shutil.rmtree with ignore_errors=True (non-fatal on permission issues)

Side Effects:
  - Deletes __pycache__ and .pytest_cache directories and their contents

Invariants:     Only directories named __pycache__ or .pytest_cache are removed
Known Faults:   Script's own execution may create a new __pycache__ (handled)

Usage:
    python clean_for_extension.py
=====================================================================
"""
import os
import shutil

BASE = os.path.dirname(os.path.abspath(__file__))


def main():
    removed = []
    for root, dirs, _ in os.walk(BASE, topdown=False):
        for d in dirs:
            if d in ('__pycache__', '.pytest_cache'):
                path = os.path.join(root, d)
                if os.path.isdir(path):
                    shutil.rmtree(path, ignore_errors=True)
                    removed.append(os.path.relpath(path, BASE))
    # Also remove __pycache__ that Python may have created during this script's run
    pc = os.path.join(BASE, '__pycache__')
    if os.path.isdir(pc):
        shutil.rmtree(pc, ignore_errors=True)
        if '__pycache__' not in removed:
            removed.append('__pycache__')

    if removed:
        print(f"Removed: {', '.join(removed)}")
    else:
        print("No cache directories found.")
    print("Extension folder is clean. Reload in chrome://extensions")


if __name__ == '__main__':
    main()
