#!/usr/bin/env python3
"""Replay frozen author scripts, without changing author outputs or certificates."""
import json
import os
from pathlib import Path
import subprocess
import sys

packet = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
results = []
for turn in range(1,6):
    result = subprocess.run([sys.executable, '-B', str(packet/f'check_turn_{turn}.py')],
                            cwd=packet, capture_output=True, text=True,
                            env={**os.environ, 'PYTHONDONTWRITEBYTECODE':'1'})
    if result.returncode:
        raise RuntimeError(f'Turn {turn} failed: {result.stderr}')
    if json.loads(result.stdout) != json.loads((packet/f'TURN_{turn}_CHECKS.json').read_text()):
        raise AssertionError(f'Turn {turn} differs from saved JSON')
    results.append({'turn':turn, 'exit_code':result.returncode, 'matches_saved_json':True})
print(json.dumps(results,indent=2))
