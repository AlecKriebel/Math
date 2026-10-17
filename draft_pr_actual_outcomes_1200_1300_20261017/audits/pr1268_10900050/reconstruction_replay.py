#!/usr/bin/env python3
"""Corrected entry point for the immutable source-reconstruction audit.

Resolves source/scratch/output before the sealed orchestrator changes cwd.
The original audit_checks.py and all sealed results stay byte-identical.
Use --worker for its write-free independent arithmetic diagnostics.
"""
import argparse
import importlib.util
import json
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--worker', action='store_true')
    parser.add_argument('--source', type=Path)
    parser.add_argument('--scratch', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if args.worker and args.output is not None:
        parser.error('--worker emits only to stdout; --output is unavailable')
    here = Path(__file__).resolve().parent
    spec = importlib.util.spec_from_file_location(
        'sealed_reconstruction_audit', here / 'reviews/reconstruction_adversary/audit_checks.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if args.worker:
        result = module.independent_worker()
    else:
        if args.source is None or args.scratch is None:
            parser.error('--source and --scratch are required except with --worker')
        source, scratch = args.source.resolve(), args.scratch.resolve()
        if scratch == source or source in scratch.parents or scratch in source.parents:
            raise RuntimeError('Scratch and sealed source must be disjoint directories')
        result = module.orchestrate(source, scratch)
    text = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if args.output is None:
        print(text, end='')
    else:
        output = args.output.resolve()
        if not args.worker and (output == source or source in output.parents):
            raise RuntimeError('Output cannot overwrite a sealed source member')
        output.write_text(text)

if __name__ == '__main__':
    main()
