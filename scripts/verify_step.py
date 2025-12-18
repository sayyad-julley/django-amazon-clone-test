#!/usr/bin/env python3

import argparse
import sys
import os
import py_compile

def verify_step_1():
    """
    Verification function for step_1: Update find_test_files
    """
    # Add any specific verification logic for find_test_files here
    return True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--step", required=True, help="Step description")
    parser.add_argument("--file", help="Target file to verify")
    args = parser.parse_args()

    print(f"Verifying step: {args.step}")

    # 1. File Existence
    if args.file:
        if not os.path.exists(args.file):
            print(f"FAIL: Target file {args.file} does not exist")
            sys.exit(1)
        print(f"OK: File {args.file} exists")
        
        # 2. Syntax Check
        if args.file.endswith(".py"):
            try:
                py_compile.compile(args.file, doraise=True)
                print(f"OK: Syntax check passed for {args.file}")
            except py_compile.PyCompileError as e:
                print(f"FAIL: Syntax error in {args.file}: {e}")
                sys.exit(1)

    # Specific step verification
    if args.step == 'step_1' or 'step_1' in args.step:
        # Check if it was meant to be step_1
        result = verify_step_1()
        if not result:
            sys.exit(1)
    
    print("VERIFICATION PASSED")
    sys.exit(0)

if __name__ == '__main__':
    main()