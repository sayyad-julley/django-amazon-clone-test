#!/usr/bin/env python3
import subprocess
import sys
import os

def verify():
    # Use the same working directory for the test command
    cwd = 'repos/django-amazon-clone-test'
    test_cmd = 'python3.11 manage.py test products.tests.StockValidationTests'
    
    print(f"🧪 Running verification command: {test_cmd}")
    
    result = subprocess.run(
        test_cmd,
        shell=True,
        capture_output=True,
        text=True,
        cwd=cwd
    )
    
    if result.returncode == 0:
        print("✅ PASS: All tests passed")
        return 0
    else:
        print("❌ FAIL: Tests failed")
        if result.stderr:
            print("--- STDERR ---")
            print(result.stderr)
        if result.stdout:
            print("--- STDOUT ---")
            print(result.stdout)
        return 1

if __name__ == "__main__":
    sys.exit(verify())
