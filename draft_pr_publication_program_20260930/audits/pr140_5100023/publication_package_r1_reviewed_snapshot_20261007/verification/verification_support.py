"""Small standard-library CLI and receipt helpers; no proof file is required."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import platform
import sys

def options(description, negative_controls):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--output', type=Path, help='JSON result path; default: stdout only')
    parser.add_argument('--proof', type=Path, help='Optional proof/manuscript file to hash; no lookup occurs without this option')
    parser.add_argument('--negative-control', choices=negative_controls,
                        help='Deliberately fail a production check; expected exit is nonzero in normal and -O modes')
    args = parser.parse_args()
    if args.output is not None and args.output.exists():
        parser.error('Output already exists; choose a fresh path to preserve prior results')
    if args.proof is not None and not args.proof.is_file():
        parser.error('The explicitly selected proof file does not exist')
    return args

def emit(result, args, verifier_file, dependencies=None):
    result.update({
        'UTC': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'actual_PID': os.getpid(),
        'mode': 'optimized' if sys.flags.optimize else 'normal',
        'python': platform.python_version(),
        'python_implementation': platform.python_implementation(),
        'dependencies': dependencies or {},
        'verifier_sha256': hashlib.sha256(Path(verifier_file).read_bytes()).hexdigest(),
        'proof_sha256': hashlib.sha256(args.proof.read_bytes()).hexdigest() if args.proof else None,
        'proof_hash_requested': args.proof is not None,
    })
    body = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open('x', encoding='utf-8') as handle:
            handle.write(body)
    print(body, end='')
