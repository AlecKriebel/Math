#!/usr/bin/env python3
"""Execute an authenticated checker with assertions enabled and isolated imports."""
import json
import runpy
import sys
from pathlib import Path


def main():
    if sys.flags.optimize != 0 or sys.flags.isolated != 1:
        raise RuntimeError('Checker requires isolated nonoptimized Python')
    if len(sys.argv) < 2:
        raise RuntimeError('Missing checker path')
    script = Path(sys.argv[1]).absolute()
    print(json.dumps({'execution_guard': 'PASS', 'child_optimization': 0,
                      'child_isolated': 1, 'checker': script.name}), file=sys.stderr)
    sys.argv = [str(script), *sys.argv[2:]]
    runpy.run_path(str(script), run_name='__main__')


if __name__ == '__main__':
    main()
