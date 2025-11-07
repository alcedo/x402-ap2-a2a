#!/usr/bin/env python3
"""Type checking script for Hello World Web Application.

This script runs mypy type checking on all Python files in the project
and provides clear feedback on type checking results.
"""

import subprocess
import sys
from pathlib import Path
from typing import List, Tuple


def run_mypy_check() -> Tuple[bool, str]:
    """
    Run mypy type checking on the project.
    
    Returns:
        Tuple[bool, str]: (success, output) where success indicates if type checking passed
    """
    try:
        # Run mypy on the main application files
        result = subprocess.run(
            ["mypy", "app.py", "config.py", "run.py", "tests/"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent
        )
        
        return result.returncode == 0, result.stdout + result.stderr
        
    except FileNotFoundError:
        return False, "mypy not found. Please install mypy: pip install mypy"
    except Exception as e:
        return False, f"Error running mypy: {e}"


def main() -> None:
    """Main function to run type checking and report results."""
    print("=" * 60)
    print("Hello World Web Application - Type Checking")
    print("=" * 60)
    
    print("Running mypy type checking...")
    success, output = run_mypy_check()
    
    if success:
        print("✅ Type checking passed!")
        print("\nAll functions have proper type annotations.")
        print("No type errors found.")
    else:
        print("❌ Type checking failed!")
        print("\nType checking output:")
        print("-" * 40)
        print(output)
        print("-" * 40)
        sys.exit(1)
    
    if output.strip():
        print("\nType checker output:")
        print(output)


if __name__ == "__main__":
    main()