#!/usr/bin/env python3
import sys
sys.dont_write_bytecode = True
import argparse
import json
from common import inventory, binding_check

def main():
    p = argparse.ArgumentParser(description="Read-only package and optional/required external binding verification")
    p.add_argument("--binding")
    p.add_argument("--require-binding", action="store_true")
    args = p.parse_args()
    result = inventory()
    result.pop("metadata")
    result["binding"] = binding_check(args.binding, args.require_binding)
    result["status"] = "PASS"
    print(json.dumps(result, sort_keys=True))

if __name__ == "__main__":
    main()
